from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zip-deploy',
    version='0.1.5',
    packages=find_packages(),
    url='https://github.com/hgross/zip-deploy',
    license='MIT',
    author='Henning Gross',
    author_email='mail.to@henning-gross.de',
    description='Provides an easy way to fetch contents from a remote ZIP files and sync/extract them to a local destination dir.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'zip-deploy = zipdeploy.zipdeploy:main_func'
        ]
    },
    console=[
        'zipdeploy/zipdeploy.py'
    ],
    keywords=[
        'zip', 'deploy', 'cache'
    ],
    python_requires='>=3.6',
)
