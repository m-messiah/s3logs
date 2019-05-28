from setuptools import setup

from os.path import join, dirname

setup(
    name='s3logs',
    version='1.7',
    py_modules=['s3logs'],
    url='https://github.com/m-messiah/s3logs',
    license='MIT',
    author='m_messiah',
    author_email='m.muzafarov@gmail.com',
    description='Push logs to S3',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    scripts=["s3logs"],
    test_suite="tests",
    install_requires=["boto", 'filechunkio'],
    keywords='logs s3 nginx',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
