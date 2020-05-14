

import hashlib
import logging
log = logging.getLogger("glasswall")
import os
import requests
from typing import Union


def get_file_bytes(file_path: str):
    """ Returns bytes of file at file_path.

    Args:
        file_path (str): The file path.

    Returns:
        file_bytes (bytes): The file bytes.

    Raises:
        FileNotFound: if file_path is not a file
    """
    with open(file_path, "rb") as f:
        return f.read()


def list_file_paths(directory: str, recursive: bool = True, absolute: bool = True):
    """ Returns a list of paths to files in a directory.

    Args:
        directory (str): The directory to retrieve files from.
        recursive (bool): Include subdirectories.
        absolute (bool): Paths as absolute paths.

    Returns:
        files (list): A list of files.
    """
    if not os.path.isdir(directory):
        raise NotADirectoryError(directory)

    if recursive:
        files = [
            os.path.normpath(os.path.join(root, file_))
            for root, dirs, files in os.walk(directory)
            for file_ in files
        ]
    else:
        files = [
            os.path.normpath(os.path.join(directory, file_))
            for file_ in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, file_))
        ]

    if absolute:
        files = [
            os.path.abspath(file_)
            for file_ in files
        ]

    return sorted(files)


def _md5_chunked(file_: bytes, chunk_size: int):
    """ Returns an md5 read in chunk_size bytes. There are 1_048_576 bytes in 1 MB.

    Args:
        file_ (bytes): The file bytes.
        chunk_size (int): The size of chunks to read from file_.

    Returns:
        md5 (hashlib.md5()): A hashlib.md5() object
    """
    md5 = hashlib.md5()
    while True:
        data = file_.read(chunk_size)
        if not data:
            break
        md5.update(data)

    return md5


def get_md5(file_: Union[bytes, str], chunk_size=67_108_864):
    """ Returns the md5 hash of the given file.

    Args:
        file_ (Union[bytes, str]): The file bytes or file path.
        chunk_size (int): The size of chunks to read from file_.

    Returns:
        md5 (str): A string representing an md5 hash.
    """
    if not isinstance(file_, (bytes, str,)):
        raise TypeError(f"file_ must be one of type: {(bytes, str,)} and not {type(file_)}")
    elif isinstance(file_, bytes):
        md5 = hashlib.md5()
        md5.update(file_)
    elif isinstance(file_, str):
        with open(file_, "rb") as f:
            md5 = _md5_chunked(f, chunk_size)

    return md5.hexdigest()


def get_presigned_urls(file_path: str, endpoint_upload: str, endpoint_download: str, api_key: str):
    """ Uploads a file and generates a dictionary containing two presigned urls suitable for the /url endpoint.

    Args:
        file_path (str): The local file path.
        endpoint_upload (str): The API Gateway endpoint to generate presigned urls to upload files.
        endpoint_download (str): The API Gateway endpoint to generate presigned urls to download files.
        api_key (str) The API key used to access the API Gateway.

    Returns:
        dict (dict): A dictionary containing two presigned urls: InputGetUrl, OutputPutUrl
    """
    file_name = os.path.basename(file_path)

    endpoint_upload_response = requests.get(
        url=f"{endpoint_upload}/{file_name}",
        headers={
            "x-api-key": api_key
        }
    ).json()

    upload_url      = endpoint_upload_response.get("PresignedUrl")
    region          = endpoint_upload_response.get("Region")
    bucket          = endpoint_upload_response.get("Bucket")
    object_key      = os.path.dirname(endpoint_upload_response.get("ObjectKey"))
    file_name       = os.path.basename(endpoint_upload_response.get("ObjectKey"))

    # upload the file
    with open(file_path, "rb") as f:
        requests.put(
            url=upload_url,
            data=f,
            headers={
                "x-api-key": api_key,
            }
        )
    log.info(f"File uploaded to: {endpoint_upload_response.get('ObjectKey')}")

    # presigned url to download the file
    InputGetUrl = requests.get(
        url=f"{endpoint_download}?bucketName={bucket}&objectPath={object_key}&region={region}&fileName={file_name}",
        headers={
            "x-api-key": api_key
        }
    ).json().get("PresignedUrl")

    file_name, extension = os.path.splitext(os.path.basename(file_path))
    OutputPutUrl = requests.get(
        url=f"{endpoint_upload}/{file_name}_output{extension}",
        headers={
            "x-api-key": api_key
        }
    ).json().get("PresignedUrl")

    return {
        "InputGetUrl": InputGetUrl,
        "OutputPutUrl": OutputPutUrl
    }
