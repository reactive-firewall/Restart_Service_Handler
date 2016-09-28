# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='restart_service_handler',
    version='0.9',
    description='Template for restarting nagios like services',
    long_description=readme,
    author='reactive-firewall',
    author_email='reactive-firewall@users.noreply.github.com',
    url='https://github.com/reactive-firewall/restart_service_handler.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

