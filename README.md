# simple-zip-deploy

![Upload Python Package](https://github.com/hgross/simple-zip-deploy/workflows/Upload%20Python%20Package/badge.svg)
[![PyPI version](https://badge.fury.io/py/simple-zip-deploy.svg)](https://badge.fury.io/py/simple-zip-deploy)

Provides an easy way to fetch contents from a remote ZIP files and sync/extract them to a local destination dir.
Note that during download and extraction the contents will not be consistent.
Not thread-safe - so take care and check the documentation.

## Installation
```
pip install simple-zip-deploy
```

## Usage
```
Windows CLI:

# Executes the check every 15 seconds
zip-deploy.exe --content-url "http://your-url.domain/movies.zip" --content-destination "./movies" --update-interval 15
```

Unix cli:
```
# Executes the check every 15 seconds
zip-deploy --content-url "http://your-url.domain/movies.zip" --content-destination "./movies" --update-interval 15
```

As python module:
````
python -m zipdeploy.zipdeploy http://your-url.domain/movies.zip /dev/shm/your/target/destination
````

In your own code (no periodic checks included, threading is your job):
```
from zipdeploy.zipdeploy import ZipDeploy

zd = ZipDeploy("http://your-url.domain/movies.zip", "/dev/shm/your/target/destination")
zd.download_if_required()
```