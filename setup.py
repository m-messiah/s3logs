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
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
