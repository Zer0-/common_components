import os
from setuptools import setup, find_packages

requires = [
    'pyramid_bricks',
    'psycopg2',
]

links = [
    'git+https://github.com/Zer0-/pyramid_bricks.git#egg=pyramid_bricks',
]

setup(
    name='common_components',
    version='0.0',
    description='bard',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    keywords='web',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    dependency_links=links,
)
