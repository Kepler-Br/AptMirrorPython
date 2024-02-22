from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any

from pydantic import BaseModel, conlist, field_validator


class FileHashInfo(BaseModel):
    hashsum: str
    filesize: int
    filepath: str


class Release(BaseModel):
    origin: str
    label: str
    suite: str
    version: str
    codename: str
    changelogs: str
    date: datetime
    architectures: conlist(str, min_length=1)
    components: conlist(str, min_length=1)
    description: str
    no_support_for_architecture_all: str
    acquire_by_hash: bool
    files_by_hash: Dict[str, conlist(FileHashInfo, min_length=1)]

    @field_validator("files_by_hash")
    @classmethod
    def files_by_hash_non_empty(cls, files_by_hash: Any) -> Any:
        if len(files_by_hash) == 0:
            raise ValueError('"files_by_hash" is empty')

        return files_by_hash


class AbstractParserState(ABC):
    @abstractmethod
    def parse_line(self, line: str) -> None:
        pass

    @abstractmethod
    def should_switch_to_next_state(self, line: str) -> bool:
        pass


class ReleaseParserHashsumState(AbstractParserState):
    def __init__(self):
        self.current_hash: Optional[str] = None
        self.files_by_hash: Dict[str, List[FileHashInfo]] = {}

    def parse_line(self, line: str) -> None:
        # Hash names are stored as 'MD5Sum:'
        # We are checking that line is hash name
        if line.find(':') == len(line) - 1:
            self.current_hash = line.split(':')[0].strip()
            return
        assert self.current_hash is not None, 'No current hash found'
        assert line.startswith(' '), f'Line not starting with space and is not a hash name: {line}'

        if self.files_by_hash.get(self.current_hash) is None:
            self.files_by_hash[self.current_hash] = []

        split_line: Tuple[str] = *filter(lambda x: len(x) != 0, line.split(' ')),
        hashsum: str
        filesize: str
        filepath: str
        hashsum, filesize, filepath = split_line[0], split_line[1], split_line[2]

        self.files_by_hash[self.current_hash].append(
            FileHashInfo(hashsum=hashsum, filesize=int(filesize), filepath=filepath))

    def should_switch_to_next_state(self, line: str) -> bool:
        # Is the last state.
        return False


class ReleaseParserHeaderState(AbstractParserState):
    def __init__(self):
        self.origin = None
        self.label = None
        self.suite = None
        self.version = None
        self.codename = None
        self.changelogs = None
        self.date = None
        self.architectures = None
        self.components = None
        self.description = None
        self.no_support_for_architecture_all = None
        self.acquire_by_hash = None

    def parse_line(self, line: str) -> None:
        assert line.find(':') != -1, f"Unknown header: {line}"

        if line.startswith('Origin'):
            self.origin = line.split(':', 1)[1].strip()
        elif line.startswith('Label'):
            self.label = line.split(':', 1)[1].strip()
        elif line.startswith('Suite'):
            self.suite = line.split(':', 1)[1].strip()
        elif line.startswith('Version'):
            self.version = line.split(':', 1)[1].strip()
        elif line.startswith('Codename'):
            self.codename = line.split(':', 1)[1].strip()
        elif line.startswith('Changelogs'):
            self.changelogs = line.split(':', 1)[1].strip()
        elif line.startswith('Date'):
            datetime_str = line.split(':', 1)[1].strip()
            # TODO: Parse with timezone. Someday
            self.date = datetime.strptime(datetime_str, '%a, %d %b %Y %H:%M:%S %Z')
        elif line.startswith('Architectures'):
            self.architectures = line.split(':', 1)[1].strip().split(' ')
        elif line.startswith('Components'):
            self.components = line.split(':', 1)[1].strip().split(' ')
        elif line.startswith('Description'):
            self.description = line.split(':', 1)[1].strip()
        elif line.startswith('No-Support-for-Architecture-all'):
            self.no_support_for_architecture_all = line.split(':', 1)[1].strip()
        elif line.startswith('Acquire-By-Hash'):
            acquire_by_hash = line.split(':', 1)[1].strip()
            assert acquire_by_hash == 'yes' or acquire_by_hash == 'no'
            if acquire_by_hash == 'yes':
                self.acquire_by_hash = True
            elif acquire_by_hash == 'no':
                self.acquire_by_hash = False

    def should_switch_to_next_state(self, line: str) -> bool:
        # Headers has two values if split by ':'.
        # if result of a find is equal to line len-1 then it's header without value
        return line.find(':') == len(line) - 1


def parse_release(release_content: str) -> Release:
    header_state = ReleaseParserHeaderState()
    hash_state = ReleaseParserHashsumState()
    current_state: AbstractParserState = header_state
    for line in release_content.splitlines():
        if current_state.should_switch_to_next_state(line):
            current_state = hash_state

        current_state.parse_line(line)

    return Release(
        origin=header_state.origin,
        label=header_state.label,
        suite=header_state.suite,
        version=header_state.version,
        codename=header_state.codename,
        changelogs=header_state.changelogs,
        date=header_state.date,
        architectures=header_state.architectures,
        components=header_state.components,
        description=header_state.description,
        no_support_for_architecture_all=header_state.no_support_for_architecture_all,
        acquire_by_hash=header_state.acquire_by_hash,
        files_by_hash=hash_state.files_by_hash
    )
