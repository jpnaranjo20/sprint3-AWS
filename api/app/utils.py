import hashlib
import os


def allowed_file(filename: str):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    # Implement the allowed_file function

    # Return True if the file extension of the filename received is in the set of allowed extensions (".png", ".jpg", ".jpeg", ".gif"), else return False
    return filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))


async def get_file_hash(file):
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
    # Implement the get_file_hash function

    await file.seek(0)
    # Step 1: Read file content. Note: hashlib.md5() requires bytes as input
    file_content = await file.read() # Use await keyword to read file content asynchronously (don't block other code execution while reading)
    
    # Step 2: Generate md5 hash (Check: https://docs.python.org/3/library/hashlib.html#hashlib.md5)
    md5_hash = hashlib.md5(file_content)
    hash_hex = md5_hash.hexdigest() # Call .hexdigest() on the resulting hash object to get a readable string version of the hash.
    
    # Step 3: Return file pointer to the beginning
    # When done reading the file, the file pointer will be at the end.
    # To do further operations on the file (saving or re-reading), we reset it to the beginning.
    await file.seek(0)

    # Step 4: Add original file extension
    original_ext = file.filename.split(".")[-1]
    new_filename = f"{hash_hex}.{original_ext}"

    return new_filename
