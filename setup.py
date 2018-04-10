# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_newsblog import __version__

REQUIREMENTS = [
    'Django>=1.8,<2.0',
    'python-dateutil',
    'aldryn-apphooks-config>=0.4.0',
    'aldryn-boilerplates>=0.7.2',
    'aldryn-categories>=1.1.0',
    'aldryn-common>=0.1.3',
    'aldryn-people>=1.1.0',
    'aldryn-translation-tools>=0.2.0',
    'backport_collections==0.1',
    'django-appdata>=0.1.4',
    'django-cms>=3.4',
    'djangocms-text-ckeditor',
    'django-filer>=0.9.9',
    'django-parler>=1.8.1',
    'django-sortedm2m>=1.2.2,!=1.3.0,!=1.3.1',
    'django-taggit',
    'lxml',
    'pytz',
    'six',
    'python-dateutil',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
    'Framework :: Django :: 1.10',
    'Framework :: Django :: 1.11',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-newsblog',
    version=__version__,
    description='Adds blogging and newsing capabilities to django CMS',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-newsblog',
    packages=find_packages(),
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    long_description=open('README.rst').read(),
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
