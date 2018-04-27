#!/usr/bin/env python

from os import path

from setuptools import setup


def package_env(file_name, strict=False):
    file_path = path.join(path.dirname(__file__), file_name)
    if path.exists(file_path) or strict:
        return open(file_path).read()
    else:
        return ''


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == '__main__':
    setup(
        name='UISoup',
        version='2.5.7',
        description='Cross Platform GUI Test Automation tool.',
        long_description=package_env('README.rst'),
        author='Max Beloborodko',
        author_email='f1ashhimself@gmail.com',
        packages=['uisoup'],
        include_package_data=True,
        install_requires=parse_requirements('requirements.txt'),
        zip_safe=False,
        entry_points={
            'console_scripts': [
                'ui-inspector = uisoup.ui_inspector:main'
            ]
        }
    )
