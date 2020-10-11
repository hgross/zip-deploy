# simple-zip-deploy
Provides an easy way to fetch contents from a remote ZIP files and sync/extract them to a local destination dir.

## Usage

As python module:
````
python -m zipdeploy.zipdeploy http://your-url.domain /dev/shm/your/target/destination
````

As installed console script (pip):
````
zip-deploy http://your-url.domain /dev/shm/your/target/destination
````