# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_newsblog import __version__

REQUIREMENTS = [
    'aldryn-apphooks-config>=0.1.4',
    'aldryn-boilerplates',
    'aldryn-categories',
    'aldryn-common',
    'aldryn-people>=0.4.6',
    'aldryn-reversion>=0.0.2',
    'backport_collections==0.1',
    'django-appdata>=0.1.4',
    'django-cms>=3.0.12',
    'django-filer>=0.9.9,<0.10',
    'django-parler',
    'django-reversion>=1.8.2,<1.9',
    'django-sortedm2m',
    'django-taggit',
    'django>=1.6,<1.8',
    'lxml',
    'pytz',
    'six',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
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
    include_package_data=True,
    zip_safe=False,
    test_suite="test_settings.run",
)
