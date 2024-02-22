from unittest import TestCase

from packages import parse_package, Package, package_difference_deleted


class PackageTests(TestCase):
    def test_package_difference_deleted(self):
        deleted_package = Package(package='foo2', version='1.0.0', architecture='amd64', filename='pool/main/foo2.deb',
                                  size=123, hashes={})
        first_packages = [
            Package(package='foo', version='1.0.0', architecture='amd64', filename='pool/main/foo.deb', size=123,
                    hashes={}),
            deleted_package,
        ]
        second_packages = [
            Package(package='foo', version='1.0.0', architecture='amd64', filename='pool/main/foo.deb', size=123,
                    hashes={}),
        ]
        diff = package_difference_deleted(first_packages, second_packages)

        self.assertListEqual([deleted_package], diff)

    def test_package_parsed_full(self):
        with open('test_data/Packages', 'r') as fp:
            content = fp.read()
        parse_package(content)

    def test_package_parsed(self):
        with open('test_data/PackagesAbridged', 'r') as fp:
            content = fp.read()

        package_list = parse_package(content)

        package1 = Package(
            package='0ad',
            version='0.0.26-3',
            installed_size=28591,
            maintainer='Debian Games Team <pkg-games-devel@lists.alioth.debian.org>',
            architecture='amd64',
            depends=
            ['0ad-data (>= 0.0.26)', '0ad-data (<= 0.0.26-3)', '0ad-data-common (>= 0.0.26)',
             '0ad-data-common (<= 0.0.26-3)', 'libboost-filesystem1.74.0 (>= 1.74.0)', 'libc6 (>= 2.34)',
             'libcurl3-gnutls (>= 7.32.0)', 'libenet7', 'libfmt9 (>= 9.1.0+ds1)', 'libfreetype6 (>= 2.2.1)',
             'libgcc-s1 (>= 3.4)', 'libgloox18 (>= 1.0.24)', 'libicu72 (>= 72.1~rc-1~)',
             'libminiupnpc17 (>= 1.9.20140610)', 'libopenal1 (>= 1.14)', 'libpng16-16 (>= 1.6.2-1)',
             'libsdl2-2.0-0 (>= 2.0.12)', 'libsodium23 (>= 1.0.14)', 'libstdc++6 (>= 12)', 'libvorbisfile3 (>= 1.1.2)',
             'libwxbase3.2-1 (>= 3.2.1+dfsg)', 'libwxgtk-gl3.2-1 (>= 3.2.1+dfsg)', 'libwxgtk3.2-1 (>= 3.2.1+dfsg-2)',
             'libx11-6', 'libxml2 (>= 2.9.0)', 'zlib1g (>= 1:1.2.0)'],
            pre_depends=['dpkg (>= 1.15.6~)'],
            description='Real-time strategy game of ancient warfare',
            homepage='https://play0ad.com/',
            description_md5='d943033bedada21853d2ae54a2578a7b',
            tag=
            ['game::strategy', 'interface::graphical', 'interface::x11', 'role::program', 'uitoolkit::sdl',
             'uitoolkit::wxwidgets', 'use::gameplaying', 'x11::application'],
            section='games',
            priority='optional',
            filename='pool/main/0/0ad/0ad_0.0.26-3_amd64.deb',
            size=7891488,
            hashes={'MD5sum': '4d471183a39a3a11d00cd35bf9f6803d',
                    'SHA256': '3a2118df47bf3f04285649f0455c2fc6fe2dc7f0b237073038aa00af41f0d5f2'
                    },
            unknown_headers=[]
        )

        package2 = Package(
            package='0ad-data',
            version='0.0.26-1',
            installed_size=3218736,
            maintainer='Debian Games Team <pkg-games-devel@lists.alioth.debian.org>',
            architecture='all',
            pre_depends=['dpkg (>= 1.15.6~)'],
            suggests=['0ad'],
            description='Real-time strategy game of ancient warfare (data files)',
            homepage='https://play0ad.com/',
            description_md5='26581e685027d5ae84824362a4ba59ee',
            tag=['role::app-data'],
            section='games',
            priority='optional',
            filename='pool/main/0/0ad-data/0ad-data_0.0.26-1_all.deb',
            size=1377557908,
            hashes={'MD5sum': 'fc5ed8a20ce1861950c7ed3a5a615be0',
                    'SHA256': '53745ae74d05bccf6783400fa98f3932b21729ab9d2e86151aa2c331c3455178'
                    },
            unknown_headers=[]
        )

        self.assertCountEqual([package1, package2], package_list)
