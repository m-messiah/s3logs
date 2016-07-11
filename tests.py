#!/usr/bin/python
from unittest import TestCase
from s3logs import S3Pusher
__author__ = 'm_messiah'


class TestS3Pusher(TestCase):
    def test_read_config(self):
        s3pusher = S3Pusher("test.conf")
        self.assertEqual(7, s3pusher.depth)
        self.assertEqual("test_bucket", s3pusher.bucket_name)
        self.assertEqual(31337, s3pusher.chunk_size)
