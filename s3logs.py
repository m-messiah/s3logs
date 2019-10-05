#!/usr/bin/env python
# coding=utf-8
import logging
from datetime import date, timedelta
from math import ceil
from os import listdir, path, stat
from platform import node
from sys import argv

from boto.exception import S3ResponseError
from boto.s3.connection import OrdinaryCallingFormat, S3Connection
from filechunkio import FileChunkIO

try:
    from ConfigParser import (SafeConfigParser as ConfigParser,
                              Error as parseError)
except ImportError:
    from configparser import ConfigParser, Error as parseError


def get_map_key(filename):
    return filename[:filename.rfind('.', 0, filename.rfind('.'))].lower()


class S3Pusher(object):
    def __init__(self, config):
        self.bucket = None
        self.bucket_name = "logs"
        self.chunk_size = 52428800
        self.conn = None
        self.depth = 30
        self.directory = "."
        self.hostname = node()
        self.key_suffix = ".gz"
        self.map = {}
        self.suffix = ".gz"
        self.today = date.today()
        self.read_config(config)
        self.dateext_latest = (
            self.today - timedelta(days=self.depth)
        ).isoformat()

    def get_dest_suffix(self, filename):
        try:
            index_part = filename[
                filename.rfind('.', 0, filename.rfind('.')) + 1:
                filename.rfind('.')
            ]
            index = int(index_part)
        except ValueError:
            if index_part < self.dateext_latest:
                return None
            return index_part + self.key_suffix

        if index < 0:
            return None

        if index > self.depth:
            return None

        return (
            self.today - timedelta(days=1 + index)
        ).isoformat() + self.key_suffix

    def read_config(self, config):
        configs = ConfigParser()
        try:
            configs.read(config)
            logging.debug("conf (%s) parsed" % configs)
            self.directory = configs.get("logs", "directory")
            self.suffix = configs.get("logs", "suffix")
            if configs.has_option("S3", "chunk_size"):
                self.chunk_size = configs.getint("S3", "chunk_size")
            if configs.has_option("logs", "key_suffix"):
                self.key_suffix = configs.get("logs", "key_suffix")
            if configs.has_option("logs", "depth"):
                self.depth = configs.getint("logs", "depth")
            self.map = dict(configs.items("map"))
            self.bucket_name = configs.get("S3", "bucket")
            self.conn = S3Connection(
                aws_access_key_id=configs.get("S3", "access_key"),
                aws_secret_access_key=configs.get("S3", "secret_key"),
                host=configs.get("S3", "host"),
                calling_format=OrdinaryCallingFormat()
            )
        except parseError as e:
            logging.error("Bad config file: %s" % e)
            exit(1)

    def connect(self):
        try:
            bucket = self.conn.get_bucket(self.bucket_name)
            self.bucket = bucket
        except S3ResponseError:
            logging.warning("%s not found. Creating." % self.bucket_name)
            bucket = self.conn.create_bucket(self.bucket_name)
            self.bucket = bucket
        logging.info("Using bucket %s" % self.bucket.name)

    def list_candidates(self):
        candidates = [filename.lower() for filename in listdir(self.directory)
                      if filename.endswith(self.suffix) and
                      get_map_key(filename) in self.map]
        logging.info("Found %s candidates at %s"
                     % (len(candidates), self.directory))
        return candidates

    def push_file(self, filename):
        dest_suffix = self.get_dest_suffix(filename)
        if not dest_suffix:
            return None

        key_name = path.join(
            self.hostname,
            self.map[get_map_key(filename)],
            dest_suffix
        )
        if self.bucket.get_key(key_name):
            logging.debug("%s exists" % filename)
            return None

        key = self.bucket.initiate_multipart_upload(key_name)
        source_path = path.join(self.directory, filename)
        source_size = stat(source_path).st_size
        chunk_count = int(ceil(source_size / float(self.chunk_size)))
        logging.debug("%s uploading as %s. %d chunks"
                      % (filename, key_name, chunk_count))
        for i in range(chunk_count):
            offset = self.chunk_size * i
            amount = min(self.chunk_size, source_size - offset)
            with FileChunkIO(source_path, 'r',
                             offset=offset, bytes=amount) as fp:
                key.upload_part_from_file(fp, part_num=i + 1)

        key.complete_upload()
        logging.debug("%s uploaded" % filename)

    def push_candidates(self):
        self.connect()
        for filename in self.list_candidates():
            self.push_file(filename)


def __main__():
    if len(argv) < 2:
        logging.error("Usage %s [-v] config_file.conf" % argv[0])
        exit(1)

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
        if argv[1] == "-v":
            logging.error("Usage %s [-v] config_file.conf" % argv[0])
            exit(2)
        pusher = S3Pusher(argv[1])

    pusher.push_candidates()
