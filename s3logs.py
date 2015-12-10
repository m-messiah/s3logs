#!/usr/bin/env python
# coding=utf-8
from boto.exception import S3ResponseError
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from datetime import datetime
from os import listdir, path
from sys import argv
import logging
from ConfigParser import SafeConfigParser, Error as parseError


class S3Pusher(object):
    def __init__(self, config):
        self.suffix = ".0.gz"
        self.directory = "."
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.bucket = None
        self.map = {}
        self.connect(config)

    def connect(self, config):
        configs = SafeConfigParser()
        try:
            configs.read(config)
            logging.debug("conf (%s) parsed" % configs)
            self.directory = configs.get("logs", "directory")
            self.suffix = configs.get("logs", "suffix")
            self.map = dict(configs.items("map"))
            conn = S3Connection(
                aws_access_key_id=configs.get("S3", "access_key"),
                aws_secret_access_key=configs.get("S3", "secret_key"),
                host=configs.get("S3", "host"),
                calling_format=OrdinaryCallingFormat(),
                is_secure=True)
            bucket_name = configs.get("S3", "bucket")
            try:
                bucket = conn.get_bucket(bucket_name)
                self.bucket = bucket
            except S3ResponseError:
                logging.warning("Bucket %s not found. Creating." % bucket_name)
                bucket = conn.create_bucket(bucket_name)
                self.bucket = bucket

            logging.info("Using bucket %s" % self.bucket.name)

        except parseError as e:
            logging.error("Bad config file: %s" % e)
            exit(1)

    def list_candidates(self):
        candidates = [filename for filename in listdir(self.directory)
                      if filename.endswith(self.suffix) and
                      filename[:filename.find(self.suffix)] in self.map]
        logging.info("Found %s candidates at %s"
                     % (len(candidates), self.directory))
        return candidates

    def push_file(self, filename):
        key = self.bucket.new_key(
            path.join(self.map[filename[:filename.find(self.suffix)]],
                      self.date + ".gz")
        )
        key.set_contents_from_filename(
            path.join(self.directory, filename)
        )
        logging.debug("%s uploaded as %s" % (filename, key.name))

    def push_candidates(self):
        for filename in self.list_candidates():
            self.push_file(filename)


if __name__ == '__main__':
    if len(argv) > 1:
        if len(argv) > 2:
            if argv[1] == "-v":
                pusher = S3Pusher(argv[2])
                logging.getLogger().setLevel(logging.DEBUG)
            elif argv[2] == "-v":
                pusher = S3Pusher(argv[1])
                logging.getLogger().setLevel(logging.DEBUG)
            else:
                pusher = None
                logging.error("Usage %s [-v] config_file.conf" % argv[0])
                exit(2)
        else:
            pusher = S3Pusher(argv[1])

        pusher.push_candidates()
    else:
        logging.error("Usage %s [-v] config_file.conf" % argv[0])
        exit(1)
