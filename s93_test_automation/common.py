

import os
# import pkg_resources


def get_file_bytes(file_path):
    """ Returns bytes of file at file_path.

    Args:
        file_path (str): The file path.

    Returns:
        file_bytes (bytes): The file bytes.

    Raises:
        FileNotFound: if file_path is not a file
    """
    # return pkg_resources.resource_stream(
    #     "s93_test_automation",
    #     file_path
    # ).read()

    with open(file_path, "rb") as f:
        return f.read()


def list_file_paths(directory, recursive=True, absolute=True):
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
