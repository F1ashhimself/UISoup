#!/usr/bin/env python

from os import path

from pip.req import parse_requirements
from setuptools import setup


def package_env(file_name, strict=False):
    file_path = path.join(path.dirname(__file__), file_name)
    if path.exists(file_path) or strict:
        return open(file_path).read()
    else:
        return ''

if __name__ == '__main__':
    setup(
        name='UISoup',
        version='2.5.3',
        description='Cross Platform GUI Test Automation tool.',
        long_description=package_env('README.rst'),
        author='Max Beloborodko',
        author_email='f1ashhimself@gmail.com',
        packages=['uisoup'],
        include_package_data=True,
        install_requires=[str(ir.req) for ir in
                          parse_requirements('requirements.txt',
                                             session=False)],
        zip_safe=False,
        entry_points={
            'console_scripts': [
                'ui-inspector = uisoup.ui_inspector:main'
            ]
        }
    )
