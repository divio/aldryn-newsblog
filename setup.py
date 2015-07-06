# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_newsblog import __version__

REQUIREMENTS = [
    'Django>=1.6,<1.8',
    'aldryn-apphooks-config>=0.2.4',
    'aldryn-boilerplates',
    'aldryn-categories',
    'aldryn-common>=0.1.3',
    'aldryn-people>=0.5.2',
    'aldryn-reversion>=0.0.2',
    'aldryn-translation-tools',
    'backport_collections==0.1',
    'django-appdata>=0.1.4',
    'django-cms>=3.0.12',
    'django-filer>=0.9.9,<0.10',
    'django-parler>=1.4',
    'django-reversion>=1.8.2,<1.9',
    'django-sortedm2m',
    'django-taggit',
    'lxml',
    'pytz',
    'six',
]

# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.6',
    'Framework :: Django :: 1.7',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
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
