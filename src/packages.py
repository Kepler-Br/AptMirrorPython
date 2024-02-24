from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Tuple

from pydantic import BaseModel


class Package(BaseModel):
    package: str
    version: str
    installed_size: Optional[int] = None
    maintainer: Optional[str] = None
    architecture: str
    depends: Optional[List[str]] = None
    pre_depends: Optional[List[str]] = None
    description: Optional[str] = None
    homepage: Optional[str] = None
    description_md5: Optional[str] = None
    tag: Optional[List[str]] = None
    section: Optional[str] = None
    priority: Optional[str] = None
    filename: str
    size: int
    hashes: Dict[str, str]
    suggests: Optional[List[str]] = None
    source: Optional[str] = None
    replaces: Optional[List[str]] = None
    breaks: Optional[List[str]] = None
    recommends: Optional[List[str]] = None
    provides: Optional[List[str]] = None
    conflicts: Optional[List[str]] = None
    enhances: Optional[List[str]] = None
    built_using: Optional[List[str]] = None
    multiarch: Optional[str] = None
    ghc_package: Optional[str] = None
    ruby_versions: Optional[str] = None
    python_egg_name: Optional[str] = None
    essential: Optional[bool] = None
    build_essential: Optional[bool] = None
    build_ids: Optional[List[str]] = None
    static_built_using: Optional[List[str]] = None
    unknown_headers: List[Tuple[str, str]] = None


class AbstractParserState(ABC):
    @abstractmethod
    def parse_line(self, line: str) -> None:
        pass

    @abstractmethod
    def should_switch_to_next_state(self, line: str) -> bool:
        pass


class PackageParser(AbstractParserState):
    def __init__(self):
        self.package: Optional[str] = None
        self.version: Optional[str] = None
        self.installed_size: Optional[int] = None
        self.maintainer: Optional[str] = None
        self.architecture: Optional[str] = None
        self.depends: Optional[List[str]] = None
        self.pre_depends: Optional[List[str]] = None
        self.description: Optional[str] = None
        self.homepage: Optional[str] = None
        self.description_md5: Optional[str] = None
        self.tag: Optional[List[str]] = None
        self.section: Optional[str] = None
        self.priority: Optional[str] = None
        self.filename: Optional[str] = None
        self.suggests: Optional[List[str]] = None
        self.size: Optional[int] = None
        self.hashes: Dict[str, str] = {}
        self.architecture: Optional[str] = None
        self.source: Optional[str] = None
        self.replaces: Optional[str] = None
        self.breaks: Optional[List[str]] = None
        self.recommends: Optional[List[str]] = None
        self.ghc_package: Optional[str] = None
        self.multiarch: Optional[str] = None
        self.provides: Optional[List[str]] = None
        self.conflicts: Optional[List[str]] = None
        self.enhances: Optional[List[str]] = None
        self.built_using: Optional[List[str]] = None
        self.ruby_versions: Optional[str] = None
        self.python_egg_name: Optional[str] = None
        self.essential: Optional[bool] = None
        self.build_essential: Optional[bool] = None
        self.build_ids: Optional[List[str]] = None
        self.ongoing_header_value: Optional[List[str]] = None
        self.static_built_using: Optional[List[str]] = None
        self.ongoing_header_key: Optional[str] = None
        self.unknown_headers: List[Tuple[str, str]] = []

    def set_field_by_header_key(self, header_key: str, value: str) -> None:
        if header_key == 'Package':
            self.package = value
        elif header_key == 'Version':
            self.version = value
        elif header_key == 'Installed-Size':
            self.installed_size = value
        elif header_key == 'Maintainer':
            self.maintainer = value
        elif header_key == 'Architecture':
            self.architecture = value
        elif header_key == 'Depends':
            self.depends = value.split(', ')
        elif header_key == 'Pre-Depends':
            self.pre_depends = value.split(', ')
        elif header_key == 'Description':
            self.description = value
        elif header_key == 'Homepage':
            self.homepage = value
        elif header_key == 'Description-md5':
            self.description_md5 = value
        elif header_key == 'Tag':
            self.tag = value.split(', ')
        elif header_key == 'Section':
            self.section = value
        elif header_key == 'Priority':
            self.priority = value
        elif header_key == 'Filename':
            self.filename = value
        elif header_key == 'Size':
            self.size = int(value)
        elif header_key == 'Suggests':
            self.suggests = value.split(', ')
        elif header_key == 'Source':
            self.source = value
        elif header_key == 'Replaces':
            self.replaces = value.split(', ')
        elif header_key == 'Breaks':
            self.breaks = value.split(', ')
        elif header_key == 'Recommends':
            self.recommends = value.split(', ')
        elif header_key == 'Multi-Arch':
            self.multiarch = value
        elif header_key == 'Provides':
            self.provides = value.split(', ')
        elif header_key == 'Conflicts':
            self.conflicts = value.split(', ')
        elif header_key == 'Enhances':
            self.conflicts = value.split(', ')
        # elif header_key == 'Built-Using':
        #     self.built_using = value.split(', ')
        # elif header_key == 'Static-Built-Using':
        #     self.static_built_using = value.split(', ')
        # elif header_key == 'Ghc-Package':
        #     self.ghc_package = value
        # elif header_key == 'Ruby-Versions':
        #     self.ruby_versions = value
        # elif header_key == 'Python-Egg-Name':
        #     self.python_egg_name = value
        # elif header_key == 'Build-Ids':
        #     self.build_ids = value.split(' ')
        # elif header_key == 'Original-Maintainer':
        #     pass
        # elif header_key == 'Important':
        #     pass
        # elif header_key == 'Protected':
        #     pass
        # elif header_key == 'Go-Import-Path':
        #     pass
        # elif header_key == 'Efi-Vendor':
        #     pass
        # elif header_key == 'Gstreamer-Decoders':
        #     pass
        # elif header_key == 'Gstreamer-Elements':
        #     pass
        # elif header_key == 'Gstreamer-Encoders':
        #     pass
        # elif header_key == 'Gstreamer-Version':
        #     pass
        # elif header_key == 'Gstreamer-Uri-Sinks':
        #     pass
        # elif header_key == 'Gstreamer-Uri-Sources':
        #     pass
        # elif header_key == 'Cnf-Extra-Commands':
        #     pass
        # elif header_key == 'Python-Version':
        #     pass
        # elif header_key == 'Lua-Versions':
        #     pass
        # elif header_key == 'X-Cargo-Built-Using':
        #     pass
        # elif header_key == 'Javascript-Built-Using':
        #     pass
        # elif header_key == 'Essential':
        #     if value == 'yes':
        #         self.essential = True
        #     elif value == 'no':
        #         self.essential = False
        #     else:
        #         raise ValueError(f'Unrecognized essential value: {value}')
        # elif header_key == 'Build-Essential':
        #     if value == 'yes':
        #         self.build_essential = True
        #     elif value == 'no':
        #         self.build_essential = False
        #     else:
        #         raise ValueError(f'Unrecognized build_essential value: {value}')
        # Hashes
        else:
            if header_key == 'MD5sum':
                assert self.hashes.get(header_key) is None, f'{header_key} already present in hashes dict'
                self.hashes[header_key] = value
            elif header_key == 'SHA256':
                assert self.hashes.get(header_key) is None, f'{header_key} already present in hashes dict'
                self.hashes[header_key] = value
            else:
                # Give up
                self.unknown_headers.append((header_key, value))
            # print(f'Unrecognized header key: {header_key}')
            # raise ValueError(f'Unrecognized header key: {header_key}')

    def parse_line(self, line: str) -> None:
        # line that starts with space is probably continuation of list
        if line.startswith(' '):
            # ongoing_header_* should not be None because list has been already started
            assert self.ongoing_header_key is not None or self.ongoing_header_value is not None
            self.ongoing_header_value.append(line)
        else:
            # If previous header exists, push it to object field
            if self.ongoing_header_value is not None or self.ongoing_header_key is not None:
                # Sanity check. Both should not be None
                assert self.ongoing_header_key is not None or self.ongoing_header_value is not None
                self.set_field_by_header_key(self.ongoing_header_key, ''.join(self.ongoing_header_value))
                self.ongoing_header_key = None
                self.ongoing_header_value = None
            split = line.split(': ', maxsplit=1)
            self.ongoing_header_key, self.ongoing_header_value = split[0], [split[1]]

    def should_switch_to_next_state(self, line: str) -> bool:
        # Packages are separated by one empty line
        return len(line) == 0

    def assemble_package(self) -> Package:
        # Assign existing values
        if self.ongoing_header_value is not None or self.ongoing_header_key is not None:
            # Sanity check. Both should not be None
            assert self.ongoing_header_key is not None or self.ongoing_header_value is not None
            self.set_field_by_header_key(self.ongoing_header_key, ''.join(self.ongoing_header_value))
            self.ongoing_header_key = None
            self.ongoing_header_value = None

        package = Package(
            package=self.package,
            version=self.version,
            installed_size=self.installed_size,
            maintainer=self.maintainer,
            architecture=self.architecture,
            depends=self.depends,
            pre_depends=self.pre_depends,
            description=self.description,
            homepage=self.homepage,
            description_md5=self.description_md5,
            tag=self.tag,
            section=self.section,
            priority=self.priority,
            filename=self.filename,
            size=self.size,
            hashes=self.hashes,
            suggests=self.suggests,
            source=self.source,
            replaces=self.replaces,
            breaks=self.breaks,
            recommends=self.recommends,
            provides=self.provides,
            multiarch=self.multiarch,
            conflicts=self.conflicts,
            enhances=self.enhances,
            ghc_package=self.ghc_package,
            built_using=self.built_using,
            ruby_versions=self.ruby_versions,
            essential=self.essential,
            build_essential=self.build_essential,
            python_egg_name=self.python_egg_name,
            static_built_using=self.static_built_using,
            build_ids=self.build_ids,
            unknown_headers=self.unknown_headers,
        )

        self.package = None
        self.version = None
        self.installed_size = None
        self.maintainer = None
        self.architecture = None
        self.depends = None
        self.pre_depends = None
        self.description = None
        self.homepage = None
        self.description_md5 = None
        self.tag = None
        self.section = None
        self.priority = None
        self.filename = None
        self.size = None
        self.hashes = {}
        self.ongoing_header_key = None
        self.ongoing_header_value = None
        self.suggests = None
        self.source = None
        self.replaces = None
        self.breaks = None
        self.provides = None
        self.recommends = None
        self.multiarch = None
        self.enhances = None
        self.conflicts = None
        self.ghc_package = None
        self.built_using = None
        self.ruby_versions = None
        self.essential = None
        self.build_essential = None
        self.python_egg_name = None
        self.build_ids = None
        self.static_built_using = None
        self.unknown_headers = []

        return package

    def is_empty(self) -> bool:
        return self.package is None and \
            self.version is None and \
            self.installed_size is None and \
            self.maintainer is None and \
            self.architecture is None and \
            self.depends is None and \
            self.pre_depends is None and \
            self.description is None and \
            self.homepage is None and \
            self.description_md5 is None and \
            self.tag is None and \
            self.section is None and \
            self.priority is None and \
            self.filename is None and \
            self.size is None and \
            len(self.hashes) == 0 and \
            self.architecture is None and \
            self.source is None and \
            self.replaces is None and \
            self.breaks is None and \
            self.recommends is None and \
            self.multiarch is None and \
            self.provides is None and \
            self.ongoing_header_key is None and \
            self.ongoing_header_value is None and \
            self.conflicts is None and \
            self.enhances is None and \
            self.built_using is None and \
            self.ghc_package is None and \
            self.ruby_versions is None and \
            self.essential is None and \
            self.build_essential is None and \
            self.build_ids is None and \
            self.static_built_using is None and \
            self.python_egg_name is None and \
            len(self.unknown_headers) == 0 and \
            self.suggests is None


def parse_package(content: str) -> List[Package]:
    packages: List[Package] = []
    parser = PackageParser()

    for line in content.splitlines():
        if parser.should_switch_to_next_state(line):
            if not parser.is_empty():
                packages.append(parser.assemble_package())
        else:
            parser.parse_line(line)

    if not parser.is_empty():
        packages.append(parser.assemble_package())

    return packages


def package_difference_diff(first: List[Package], second: List[Package]) -> List[Package]:
    diff_packages: List[Package] = []
    second_name_to_package: Dict[str, Package] = {}

    for it in second:
        assert it.package not in second_name_to_package, f'Duplicate package {it.package}'
        second_name_to_package[it.package] = it
    for it in first:
        if it.package not in second_name_to_package:
            diff_packages.append(it)

    return diff_packages
