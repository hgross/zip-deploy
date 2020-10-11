import argparse
import os.path
import pathlib
import shutil
import urllib.request
import zipfile
from pathlib import Path
from time import time, sleep
import re

URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

DEFAULT_DESTINATION_FOLDER = "./content"
DEFAULT_TEMPORARY_DOWNLOAD_FILENAME = "download.zip"
ETAG_FILE_NAME = ".etagfile"


class ZipDeploy:
    """
    Is instantiated with a destination folder to which a remotely hosted (HTTP(s)) ZIP file is extracted.
    The ZIP file and a .etagfile is written to the destination folder.
    The ZIP file exists during download and extraction time.
    The .etagfile contains the an ETag of the ZIP-file request to determine, if a re-download is required.
    Therefore it is written on extraction and cleared on re-download.

    If re-download is called, the contents are removed before the download.
    So keep in mind that during download and extraction no content is available in the destination directory.
    Not thread-safe.
    """

    def __init__(self,
                 content_source,
                 content_destination=DEFAULT_DESTINATION_FOLDER,
                 download_file_name=DEFAULT_TEMPORARY_DOWNLOAD_FILENAME,
                 etag_file_name=ETAG_FILE_NAME):
        """
        :param content_source: An url where to fetch the contents from. Must be a zip file.
        :param content_destination: the directory path where the contents should be extracted to (locally).
        :param download_file_name: the file name of the zip file that is downloaded locally to the destination dir
        :param etag_file_name: the etag file's file name
        """
        self.content_source_url = content_source
        self.content_destination = os.path.abspath(content_destination)
        self.download_file_name = download_file_name
        self.etag_file_name = etag_file_name

    def __repr__(self):
        return 'ZipDeploy(%s, %s, %s, %s)' % (self.content_source_url, self.content_destination, self.download_file_name, self.etag_file_name)

    def __str__(self):
        return self.__repr__()

    def download_content(self, content_download_url=None):
        """
        Downloads the content of "content_url" (ZIP-file) and extracts this content to "unzip_folder".
        Additionally writes a file named ETAG_FILE_NAME to the content directory, containing the ETag of the ZIP-file
        when downloaded.

        :param content_download_url: the url to download the zip file from. If None (default), the content_source url will be used.
        """

        unzip_folder = self.content_destination
        temporary_download_filename = self.download_file_name
        content_url = content_download_url if content_download_url is not None else self.content_source_url

        # ensure destination directory existence
        pathlib.Path(unzip_folder).mkdir(parents=True, exist_ok=True)

        # download the zip file
        download_path = os.path.join(os.path.abspath(unzip_folder), temporary_download_filename)
        local_filename, headers = urllib.request.urlretrieve(content_url, download_path)
        print("Downloaded %s to: %s" % (content_url, download_path))

        # extract
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_folder)
        print("Extracted contents of %s to %s" % (download_path, unzip_folder))

        # extract etag from headers and cache it
        etag_file_location = os.path.join(os.path.abspath(unzip_folder), ETAG_FILE_NAME)
        if 'ETag' in headers:
            e_tag = headers["ETag"]
            with open(etag_file_location, "w") as etag_file:
                etag_file.write(e_tag)
            print("Wrote etag to: %s" % (etag_file_location,))
        else:
            print(
                "Warning: Remote URL %s did not provide an ETag in the headers. No caching will take place (downloading every time).")

        # clean up
        try:
            os.remove(download_path)
            print("Deleted file %s" % (download_path,))
        except OSError as e:
            print.error("Error deleting file: %s : %s" % (download_path, e.strerror))

    def retrieve_etag(self, content_download_url=None):
        """
        Retrieves the ETag from the given "content_download_url" or content_source_url respectively.

        :param content_download_url: if not None (default), will override the content_source_url provided during instance creation
        :return: the ETag (if provided).
        """
        """Retrieves just the ETag from the given url using HTTP GET"""
        url = content_download_url if content_download_url is not None else self.content_source_url

        req = urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method="GET")
        with urllib.request.urlopen(req) as response:
            headers = response.headers

        return headers["ETag"]

    def is_download_required(self, content_download_url=None):
        """
        Checks whether a download is required.
        Based on the cached etag file (if existent).
        If the file doesnt exist, download is assumed to be required.
        If the etag written to the filer differs from the etag of "url", a download is required.

        :param content_download_url: if not None (default), will override the content_source_url provided during instance creation
        :return: True, if a download is required
        """
        url = content_download_url if content_download_url is not None else self.content_source_url
        unzip_folder = self.content_destination
        etag_file_location = os.path.join(os.path.abspath(unzip_folder), ETAG_FILE_NAME)

        if not os.path.isfile(etag_file_location):
            print("ETag file %s does not exist as a file. Download is required." % (etag_file_location,))
            return True

        remote_e_tag = self.retrieve_etag(url)
        local_e_tag = Path(etag_file_location).read_text()

        if remote_e_tag != local_e_tag:
            print("ETags differ. Local ETag: %s, Remote ETag: %s" % (local_e_tag, remote_e_tag))
            print("Content download is required.")
            return True
        print("ETags are identical. Local ETag: %s, Remote ETag: %s" % (local_e_tag, remote_e_tag))
        print("Content download is not required.")
        return False

    def clear_content(self):
        """Deletes the destination folder"""
        try:
            print("Clearing content directory %s ..." % self.content_destination)
            shutil.rmtree(self.content_destination, ignore_errors=True)
            print("Content directory %s cleared." % self.content_destination)
        except OSError as e:
            print.error("Error: %s : %s" % (self.content_destination, e.strerror))

    def download_if_required(self, content_zip_url=None, force_download=False):
        """
            Downloads a zip file from the given 'content_zip_url'.
            Extracts the contents to 'content_destination_directory'.
            Only downloads and extracts the contents, if the ETag provided by the content_zip_url's headers differ from the previously cached ones (if any).


            :param content_zip_url: the url to download from (optional). If not set, the configured source url during instance creation is used.
            :param force_download: Setting "force_download" to True allows to forcefully (re-)download the content. Default is False.
            :return: True if download was required and happened, False if not required
        """
        content_url = content_zip_url if content_zip_url is not None else self.content_source_url

        if force_download:
            self.clear_content()

        if self.is_download_required(content_url):
            print("Download is required. Going to clear content, then download and extract content.")
            self.clear_content()
            print("Downloading and extracting content from %s to %s ..." % (content_url, self.content_destination))
            self.download_content(content_url)
            print("Content at %s was updated sucessfully." % (self.content_destination, ))
            return True
        return False


def main_func():
    """
    The main function to be called from the cli
    :return:
    """
    argParser = argparse.ArgumentParser(description="Starts ZipDeploy with a periodic checking schedule.")
    argParser.add_argument("content_url", type=str, help="Content url to fetch the zip file from")
    argParser.add_argument("--content-destination", type=str, default=DEFAULT_DESTINATION_FOLDER, help="Folder to put the extracted zip file's contents in after the download.")
    argParser.add_argument('--update-interval', default="1800", type=int, help='Update interval in seconds.')
    args = argParser.parse_args()

    # parse and validate args
    content_source = args.content_url
    content_destination = args.content_destination
    update_interval = args.update_interval

    if re.match(URL_REGEX, content_source) is None:
        raise ValueError("%s is not a valid URL" % (content_source))
    if update_interval <= 0:
        raise ValueError("Upate interval is invalid - must be greater than 0")
    if update_interval <= 10:
        print ("Warning: very low update interval (%d seconds) - make sure you really want that." % (update_interval, ))

    zip_deploy = ZipDeploy(content_source=content_source, content_destination=content_destination)

    while True:
        zip_deploy.download_if_required()
        sleep(update_interval)


if __name__ == "__main__":
    main_func()
