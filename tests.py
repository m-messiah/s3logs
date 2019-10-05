#!/usr/bin/python
from datetime import timedelta
from unittest import TestCase

from s3logs import S3Pusher

__author__ = 'm_messiah'


class TestS3Pusher(TestCase):
    def setUp(self):
        self.s3pusher = S3Pusher("test.conf")

    def test_read_config(self):
        self.assertEqual(7, self.s3pusher.depth)
        self.assertEqual("test_bucket", self.s3pusher.bucket_name)
        self.assertEqual(31337, self.s3pusher.chunk_size)

    def test_index_filename(self):
        # Basic case
        self.assertEqual(
            (self.s3pusher.today - timedelta(days=1)).isoformat() + self.s3pusher.key_suffix,
            self.s3pusher.get_dest_suffix('nginx.access.log.0.gz'),
        )
        # Corner case
        self.assertEqual(
            (self.s3pusher.today - timedelta(days=8)).isoformat() + self.s3pusher.key_suffix,
            self.s3pusher.get_dest_suffix('nginx.access.log.7.gz'),
        )
        # More than depth
        self.assertEqual(None, self.s3pusher.get_dest_suffix('nginx.access.log.8.gz'))
        self.assertEqual(None, self.s3pusher.get_dest_suffix('nginx.access.log.-1.gz'))

    def test_dateext_filename_today(self):
        day = self.s3pusher.today.isoformat()
        self.assertEqual(
            day + self.s3pusher.key_suffix,
            self.s3pusher.get_dest_suffix('nginx.access.log.%s.gz' % day),
        )

    def test_dateext_filename_yesterday(self):
        day = (self.s3pusher.today - timedelta(days=1)).isoformat()
        self.assertEqual(
            day + self.s3pusher.key_suffix,
            self.s3pusher.get_dest_suffix('nginx.access.log.%s.gz' % day),
        )

    def test_dateext_filename_full_datetime(self):
        day = (self.s3pusher.today - timedelta(days=1)).isoformat()
        self.assertEqual(
            day + 'T23:55:01' + self.s3pusher.key_suffix,
            self.s3pusher.get_dest_suffix('nginx.access.log.%sT23:55:01.gz' % day),
        )

    def test_dateext_filename_too_old(self):
        day = (self.s3pusher.today - timedelta(days=self.s3pusher.depth + 1)).isoformat()
        self.assertEqual(
            None,
            self.s3pusher.get_dest_suffix('nginx.access.log.%s.gz' % day),
        )

