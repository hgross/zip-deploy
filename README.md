# zip-deploy

[![PyPI version](https://badge.fury.io/py/zip-deploy.svg)](https://badge.fury.io/py/zip-deploy)
![Upload Python Package](https://github.com/hgross/zip-deploy/workflows/Upload%20Python%20Package/badge.svg)
![Docker](https://github.com/hgross/zip-deploy/workflows/Docker/badge.svg)

Provides an easy way to fetch contents from a remote ZIP files and sync/extract them to a local destination dir.
Note that during download and extraction the contents will not be consistent.
Not thread-safe - so take care and check the documentation.
If you use the cli, check the -h option for configurable options.

## Installation
```
pip install zip-deploy
```

## Usage
Windows CLI:
```
# Executes the check every 15 seconds
zip-deploy.exe  --content-destination "./movies" --update-interval 15 "http://your-url.domain/movies.zip"
```

Unix cli:
```
# Executes the check every 15 seconds
zip-deploy  --content-destination "./movies" --update-interval 15 "http://your-url.domain/movies.zip"
```

As python module:
````
python -m zipdeploy.zipdeploy --content-destination /dev/shm/your/target/destination --update-interval 15 http://your-url.domain/movies.zip  
````

In your own code (no periodic checks included, threading is your job):
```
from zipdeploy.zipdeploy import ZipDeploy

zd = ZipDeploy("http://your-url.domain/movies.zip", "/dev/shm/your/target/destination")
zd.download_if_required()
```

Using Docker:
```
# make sure to mount /your/target/destination into the container, if you plan to do something useful ;-)
docker run ghcr.io/hgross/zip-deploy --content-destination /your/target/destination --update-interval 15 http://your-url.domain/movies.zip
```

## Disclaimer
This project is my playground project to get to know GitHub Actions for automated package publishing/Release pipelines on GitHub.
Don't expect maintenance, but feel free to use this tool if it helps you out. 
I created it on a weekend for a friend who set up an [e-ink display project](https://github.com/TomWhitwell/SlowMovie) on his Raspberry Pi.