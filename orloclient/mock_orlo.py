from __future__ import print_function
from orloclient import OrloClient, Release, Package
import json
import uuid

__author__ = 'alforbes'

"""
A very simple Mock Orlo object for testing in deployment scripts
"""

mock_package_dict = {
    "status": "SUCCESSFUL",
    "name": "package_one",
    "version": "1.2.3",
    "ftime": "2015-11-27T11:32:34Z",
    "stime": "2015-11-27T11:32:34Z",
    "duration": 0,
    "diff_url": None,
    "id": str(uuid.uuid4())
}

mock_release_dict = {
    "platforms": [
        "testplatform"
    ],
    "ftime": "2015-11-27T11:32:34Z",
    "stime": "2015-11-27T11:32:34Z",
    "team": None,
    "duration": 0,
    "references": [],
    "packages": [mock_package_dict],
    "id": str(uuid.uuid4()),
    "user": "testuser",
    "metadata": {"env": "test", "pool": "web"}
}

mock_stats_dict = {
    "global": {
        "releases": {
            "normal": {
                "failed": 1,
                "successful": 10
            },
            "rollback": {
                "failed": 1,
                "successful": 2
            },
            "total": {
                "failed": 2,
                "successful": 12
            }
        }
    }
}


class MockOrloClient(object):
    """
    A mock Orlo Client

    Will return values from the example objects below.
    """
    def __init__(self, uri, verify_ssl=True):
        self.uri = uri
        self.verify_ssl = verify_ssl

        self.mock_release_dict = mock_release_dict
        self.mock_package_dict = mock_package_dict
        self.mock_stats_dict = mock_stats_dict

        self.mock_releases = []
        self._add_mock_release(mock_release_dict)

        self.mock_packages = []
        self._add_mock_package(self.mock_package_dict)

    def _add_mock_release(self, release_dict):
        self.mock_releases.append(
            Release(self, release_dict['id'])
        )

    def _add_mock_package(self, package_dict):
        package = Package(
            mock_release_dict['id'],
            package_dict['id'],
            package_dict['name'],
            package_dict['version'],
        )
        package.stime = package_dict['stime']
        package.ftime = package_dict['ftime']
        self.mock_packages.append(package)

    def ping(self):
        return True

    def get_release(self, release_id):
        return Release(self, release_id)

    def get_release_json(self, release_id):
        return {
            'releases': [self.mock_release_dict]
        }

    def get_releases(self, *args, **kwargs):
        response = {
            'releases': [self.mock_release_dict]
        }
        return json.dumps(response)

    def create_release(self, *args, **kwargs):
        return self.mock_releases[0]

    def create_package(self, *args, **kwargs):
        return self.mock_packages[0]

    @staticmethod
    def get_info(field, name=None, platform=None):
        return {'foo': {'bar': 1}}

    def get_stats(self, field=None, name=None, platform=None, stime=None, ftime=None):
        return json.dumps(self.mock_stats_dict)

    @staticmethod
    def release_stop(release_id):
        return True

    @staticmethod
    def package_start(*args, **kwargs):
        return True

    @staticmethod
    def package_stop(*args, **kwargs):
        return True

    @staticmethod
    def deploy_release(*args, **kwargs):
        return True

    def get_versions(self):
        return {
            self.mock_package_dict['name']:
                self.mock_package_dict['version']
        }
