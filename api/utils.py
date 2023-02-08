import os
import hashlib


def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files.

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    # allowed extensions detailed on views.py
    allow_ext = {".png", ".jpg", ".jpeg", ".gif"}
    # split input filename and check if it's allowed
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext in allow_ext:
        return True
    else:
        return False


def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # hash filename string
    file_hash = hashlib.md5(file.read()).hexdigest()
    # split input filename
    _, ext = os.path.splitext(file.filename)
    # extension to lowercase
    ext = ext.lower()
    # concatenate hash with extension
    hashed_filename = f"{file_hash}{ext}"
    # cursor back to read it later
    file.seek(0)
    return hashed_filename
