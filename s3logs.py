#!/usr/bin/env python
# coding=utf-8
from boto.exception import S3ResponseError
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from datetime import datetime
from os import listdir, path


class S3Pusher(object):
    def __init__(self, config):
        self.suffix = ".0.gz"
        self.directory = "."
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.bucket = None
        self.map = {}
        self.connect(config)

    def connect(self, config):
        # TODO: parse config
        access_key = ''
        secret_key = ''
        ceph_host = ''
        bucket_name = ''
        self.suffix = ""
        self.directory = ""
        self.map = {}

        conn = S3Connection(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            host=ceph_host,
            calling_format=OrdinaryCallingFormat(),
            is_secure=True)

        try:
            bucket = conn.get_bucket(bucket_name)
            self.bucket = bucket
        except S3ResponseError:
            bucket = conn.create_bucket(bucket_name)
            self.bucket = bucket

    def list_candidates(self):
        candidates = [filename for filename in listdir(self.directory)
                      if filename.endswith(self.suffix)]
        return candidates

    def push_file(self, filename):
        app = filename[:filename.find(self.suffix)]
        if app in self.map:
            key = self.bucket.new_key(
                path.join(self.map[app], self.date + ".gz")
            )
            key.set_contents_from_filename(
                path.join(self.directory, filename)
            )

    def push_candidates(self):
        for filename in self.list_candidates():
            self.push_file(filename)


if __name__ == '__main__':
    pusher = S3Pusher(None)
    print(pusher.push_candidates())
