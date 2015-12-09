S3 Logs Pusher
==============

Install
-------

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

    [logs]

    suffix = .0.gz
    directory = /var/log/nginx/

    [map]

    example.com-access.log = example/access
    example.com-error.log = example/error
    mysite.me.access.log = mysite/access

When it used with that config, script takes all files in directory `/var/log/nginx/`, filter only those, which ends with `.0.gz` and send it to S3, according to map.

For example, /var/log/nginx now consists of:

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

So, if today is 9 December 2015, on your S3 `<bucket_name>` would be those keys:

    example/access/2015-12-09.gz
    example/error/2015-12-09.gz
    mysite/access/2015-12-09.gz

Because we have not explain how maps mysite.me.error.log.0.gz - it was skipped.