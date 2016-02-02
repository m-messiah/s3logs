S3 Logs Pusher
==============

.. image:: https://img.shields.io/pypi/v/s3logs.svg?style=flat-square
    :target: https://pypi.python.org/pypi/s3logs



.. image:: https://img.shields.io/pypi/dm/s3logs.svg?style=flat-square
        :target: https://pypi.python.org/pypi/s3logs

Get files from directory by mask and push them to S3

Install
-------

.. code:: bash

    pip install s3logs

Usage
-----

.. code:: bash

    s3logs config.conf

Where config.conf can use that structure:

.. code:: ini

    [S3]
    access_key = <S3_KEY>
    secret_key = <S3_SECRET_KEY>
    host = <s3.example.com>
    bucket = <bucket_name>
    chunk_size = <bytes, default=52428800>

    [logs]

    suffix = .gz
    key_suffix = .gz
    directory = /var/log/nginx/
    depth = 30

    [map]

    example.com-access.log = example/access
    example.com-error.log = example/error
    mysite.me.access.log = mysite/access

When it used with that config, script takes all files in directory `/var/log/nginx/`, filter only those, which ends with `.gz` and send it to S3, according to map.

For example, /var/log/nginx now consists of:

.. code::

    example.com-access.log
    example.com-access.log.0.gz
    example.com-access.log.1.gz
    example.com-error.log
    example.com-error.log.0.gz
    example.com-error.log.1.gz
    mysite.me.access.log
    mysite.me.access.log.0.gz
    mysite.me.error.log
    mysite.me.error.log.0.gz

So, if today is 9 December 2015, and your hostname is node1, on your S3 `<bucket_name>` would be those keys:

.. code::

    node1/example/access/2015-12-09.gz
    node1/example/access/2015-12-08.gz
    node1/example/error/2015-12-09.gz
    node1/example/error/2015-12-08.gz
    node1/mysite/access/2015-12-09.gz

Because we have not explain how maps mysite.me.error.log.0.gz - it would be skipped.

Script also checks whether file exists in S3 and push only those, which are not.

Parameter `depth` stops pushing, if filename is older, than `.<depth>.gz`
