from setuptools import setup

setup(
    name='simple-zip-deploy',
    version='0.1.0',
    packages=['zipdeploy'],
    url='https://github.com/hgross/simple-zip-deploy',
    license='MIT',
    author='Henning Gross',
    author_email='mail.to@henning-gross.de',
    description='Provides an easy way to fetch contents from a remote ZIP files and sync/extract them to a local destination dir.',
    entry_points={
        'console_scripts': [
            'zip-deploy = zipdeploy:main_func'
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
