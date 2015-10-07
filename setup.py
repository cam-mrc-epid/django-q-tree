import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-q-tree',
    version='0.1',
    packages=['q_tree'],
    include_package_data=True,
    install_requires = ['django-mptt', 'django-polymorphic',
                        'django-polymorphic-tree', 'beautifulsoup4',
                        ],
    dependency_links = ['https://github.com/davidgillies/xml-objectifier'],
    license='',  # example license
    description='Forms System XML editor.',
    long_description=README,
    url='http://github.com/davidgillies/q_tree',
    author='David Gillies',
    author_email='dg467@cam.ac.uk',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
