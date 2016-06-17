from __future__ import print_function
from tests import OrloClientTest
from orloclient.mock_orlo import MockOrloClient
from orloclient import Package, Release
from orloclient.exceptions import OrloClientError
import arrow
import uuid

__author__ = 'alforbes'

client = MockOrloClient('http://dummy.example.com')


class TestPackage(OrloClientTest):
    def setUp(self):
        self.rid = client.mock_releases[0].id
        self.pid = client.mock_packages[0].id
        self.release = Release(client, self.rid)
        self.package = self.release.packages[0]

    def test_package_id(self):
        """
        Test that the package id returned matches the one from the mock and is a UUID
        """
        self.assertIsInstance(self.package.id, uuid.UUID)
        self.assertEqual(self.package.id, uuid.UUID(self.pid))

    def test_package_stime(self):
        """
        Test that stime is cast to an arrow object
        """
        self.assertIsInstance(self.package.stime,
                              arrow.arrow.Arrow)
        self.assertEqual(self.package.stime,
                         arrow.get(client.mock_packages[0].stime))

    def test_package_ftime(self):
        self.assertIsInstance(self.package.ftime,
                              arrow.arrow.Arrow)
        self.assertEqual(self.package.ftime,
                         arrow.get(client.mock_packages[0].ftime))

    def test_package_duration_int(self):
        self.assertIsInstance(self.package.duration, int)
        self.assertEqual(self.package.duration, 0)
