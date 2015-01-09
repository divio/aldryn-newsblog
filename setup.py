from setuptools import setup, find_packages
from aldryn_newsblog import __version__

REQUIREMENTS = [
    'django-parler',
    'django-filer',
    'aldryn-common',
    'django-appdata',
    'django-cms',
    'aldryn-people',
    'django-reversion>=1.8.2,<1.9',
    'django>=1.6,<1.7',
    'aldryn-apphooks-config',
    'django-reversion>=1.8.2,<1.9',
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
    dependency_links=[
        ('git+http://github.com/yakky/django-cms/@feature/appspaced_apphooks'
         '#egg=django-cms'),
        ('git+http://github.com/aldryn/aldryn-apphooks-config'
         '#egg=aldryn-apphooks-config'),
    ],
)
