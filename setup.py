#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from cmsplugin_footnote import version_string


setup(
    name='cmsplugin-footnote',
    version=version_string,
    author='Bertrand Bordage',
    author_email='bordage.bertrand@gmail.com',
    url='https://github.com/BertrandBordage/cmsplugin-footnote',
    description='A simple plugin allowing to add footnotes in django CMS.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'Django >= 1.10',
        'django-CMS >= 3.4.5',
        'djangocms-text-ckeditor >= 3.3.0'
    ],
    include_package_data=True,
    zip_safe=False,
)
