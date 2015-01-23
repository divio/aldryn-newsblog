from setuptools import setup, find_packages
from aldryn_newsblog import __version__

REQUIREMENTS = [
    'django-parler',
    'django-filer',
    'aldryn-common',
    'django-appdata',
    'django-cms>=3.0.90a1',
    'aldryn-people',
    'django-reversion>=1.8.2,<1.9',
    'django>=1.6,<1.7',
    'aldryn-apphooks-config>=0.1.0',
    'django-reversion>=1.8.2,<1.9',
    'django-taggit',
    'aldryn-categories',
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
    dependency_links=[
        'git+https://github.com/yakky/django-cms@future/integration#egg=django-cms-3.0.90a3',
        'git+https://github.com/aldryn/aldryn-apphooks-config#egg=aldryn-apphooks-config-0.1.0',
    ],
)
