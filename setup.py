import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


setup(
    name='django-fsm-widget',
    version='0.0.4',

    description='A filtered select multiple widget that allows for lazy '
                'loading.',
    long_description=README,

    packages=find_packages(exclude=('example', )),
    include_package_data=True,
    install_requires = [
        'django>=1.9'
    ],

    author='Ashley Mathew',
    author_email='ashley@directemployersfoundation.org',

    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],

    zip_safe=False,
)
