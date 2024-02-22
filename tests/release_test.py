import datetime
from typing import List
from unittest import TestCase
from release import parse_release, FileHashInfo


class ReleaseTests(TestCase):
    def setUp(self):
        with open('test_data/Release', 'r') as fp:
            self.content = fp.read()

    def test_headers_parsed(self):
        release = parse_release(self.content)

        self.assertEqual('Debian', release.origin)
        self.assertEqual('Debian', release.label)
        self.assertEqual('stable', release.suite)
        self.assertEqual('12.5', release.version)
        self.assertEqual('bookworm', release.codename)
        self.assertEqual('https://metadata.ftp-master.debian.org/changelogs/@CHANGEPATH@_changelog', release.changelogs)
        self.assertEqual(datetime.datetime(day=10, month=2, year=2024, hour=11, minute=7, second=25), release.date)
        self.assertEqual(True, release.acquire_by_hash)
        self.assertEqual('Packages', release.no_support_for_architecture_all)
        self.assertCountEqual(
            ['all', 'amd64', 'arm64', 'armel', 'armhf', 'i386', 'mips64el', 'mipsel', 'ppc64el', 's390x'],
            release.architectures)
        self.assertCountEqual(['main', 'contrib', 'non-free-firmware', 'non-free'], release.components)
        self.assertEqual('Debian 12.5 Released 10 February 2024', release.description)

    def test_hashsums_parsed(self):
        release = parse_release(self.content)

        self.assertTrue(len(release.files_by_hash) == 2, 'Expected exactly 2 elements')

        expected_hashes: List[FileHashInfo] = [
            FileHashInfo(hashsum='0ed6d4c8891eb86358b94bb35d9e4da4', filesize=1484322, filepath='contrib/Contents-all'),
            FileHashInfo(hashsum='d0a0325a97c42fd5f66a8c3e29bcea64', filesize=98581,
                         filepath='contrib/Contents-all.gz'),
            FileHashInfo(hashsum='58f32d515c66daafcdac2595fc984814', filesize=840179,
                         filepath='contrib/Contents-amd64'),
        ]
        self.assertCountEqual(expected_hashes, release.files_by_hash['MD5Sum'])

        expected_hashes: List[FileHashInfo] = [
            FileHashInfo(hashsum='d6c9c82f4e61b4662f9ba16b9ebb379c57b4943f8b7813091d1f637325ddfb79', filesize=1484322,
                         filepath='contrib/Contents-all'),
            FileHashInfo(hashsum='c22d03bdd4c7619e1e39e73b4a7b9dfdf1cc1141ed9b10913fbcac58b3a943d0', filesize=98581,
                         filepath='contrib/Contents-all.gz'),
            FileHashInfo(hashsum='301791ff5d830c6e9cda34c4de6d4207c1e07e910c176bd35978d315dbd251bc', filesize=840179,
                         filepath='contrib/Contents-amd64'),
        ]
        self.assertCountEqual(expected_hashes, release.files_by_hash['SHA256'])
