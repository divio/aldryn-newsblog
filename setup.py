# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from aldryn_newsblog import __version__


REQUIREMENTS = [
    'Django>=1.11',
    'python-dateutil',
    'aldryn-apphooks-config>=0.5.2',
    'aldryn-boilerplates>=0.8.0',
    'aldryn-categories>=1.2.0',
    'aldryn-common>=1.0.5',
    'aldryn-people>=2.2.0',
    'aldryn-translation-tools>=0.3.0',
    'backport_collections==0.1',
    'django-appdata>=0.2.1',
    'django-cms>=3.4.5',
    'djangocms-text-ckeditor>=3.7.0',
    'django-filer>=1.4.2',
    'django-parler',
    'django-sortedm2m',
    'django-taggit>=0.23.0',
    'lxml',
    'pytz',
    'six',
    'python-dateutil',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 1.11',
    'Framework :: Django :: 2.0',
    'Framework :: Django :: 2.1',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-newsblog',
    version=__version__,
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-newsblog',
    license='BSD',
    description='Adds blogging and newsing capabilities to django CMS',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite="test_settings.run",
)
