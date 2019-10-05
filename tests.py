#!/usr/bin/python
from datetime import timedelta
from unittest import TestCase

from s3logs import S3Pusher

__author__ = 'm_messiah'


class TestS3Pusher(TestCase):
    def setUp(self):
        self.s3pusher = S3Pusher("test.conf")

    def compare_index(self, index, is_ok=True):
        if is_ok:
            etalon = (self.s3pusher.today - timedelta(days=index + 1)).isoformat() + self.s3pusher.key_suffix
        else:
            etalon = None
        self.assertEqual(
            etalon,
            self.s3pusher.get_dest_suffix('nginx.access.log.%s.gz' % index),
        )

    def compare_dateext(self, index, is_ok=True):
        day = (self.s3pusher.today - timedelta(days=index)).isoformat()
        etalon = day + self.s3pusher.key_suffix if is_ok else None
        self.assertEqual(
            etalon,
            self.s3pusher.get_dest_suffix('nginx.access.log.%s.gz' % day),
        )

    def test_read_config(self):
        self.assertEqual(7, self.s3pusher.depth)
        self.assertEqual("test_bucket", self.s3pusher.bucket_name)
        self.assertEqual(31337, self.s3pusher.chunk_size)

    def test_index_filename(self):
        # Basic case
        self.compare_index(0)
        # Corner case
        self.compare_index(self.s3pusher.depth)
        # More than depth
        self.compare_index(self.s3pusher.depth + 1, is_ok=False)
        self.compare_index(-1, is_ok=False)

    def test_dateext_filename_today(self):
        self.compare_dateext(0)

    def test_dateext_filename_yesterday(self):
        self.compare_dateext(1)

    def test_dateext_filename_too_old(self):
        self.compare_dateext(self.s3pusher.depth + 1, is_ok=False)

    def test_dateext_filename_full_datetime(self):
        day = (self.s3pusher.today - timedelta(days=1)).isoformat()
        self.assertEqual(
            day + 'T23:55:01' + self.s3pusher.key_suffix,
            self.s3pusher.get_dest_suffix('nginx.access.log.%sT23:55:01.gz' % day),
        )
