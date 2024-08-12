""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import date
import os
import image_lib
import sqlite3
import apod_api
import re
import sys

# Full paths of the image cache folder and database
# - The image cache directory is a subdirectory of the specified parent directory.
# - The image cache database is a sqlite database located in the image cache directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')
image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()   

    # Initialize the image cache
    init_apod_cache()

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # TODO: Complete function body
    # Hint: The following line of code shows how to convert and ISO-formatted date string to a date object
    if len(sys.argv) > 1:
        try:
            apod_date = date.fromisoformat(sys.argv[1])
            if apod_date < date(1995, 6, 16) or apod_date > date.today():
                raise ValueError("Date out of range")
        except ValueError:
            print("Error: Invalid date format or date out of range. Please use YYYY-MM-DD.")
            sys.exit(1)
    else:
        apod_date = date.today()

    return apod_date

def init_apod_cache():
    """Initializes the image cache by:
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    """
    # TODO: Create the image cache directory if it does not already exist
    # TODO: Create the DB if it does not already exist
    if not os.path.exists(image_cache_dir):
        os.makedirs(image_cache_dir)
    if not os.path.exists(image_cache_db):
        conn = sqlite3.connect(image_cache_db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS apod_cache
                     (id INTEGER PRIMARY KEY, title TEXT, explanation TEXT, file_path TEXT, sha256 TEXT)''')
        conn.commit()
        conn.close()
    return

def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    apod_info = apod_api.get_apod_info(apod_date)
    if apod_info:
        apod_id = get_apod_id_from_db(apod_info['sha256'])
        if apod_id == 0:
            file_path = determine_apod_file_path(apod_info['title'], apod_info['url'])
            image_lib.download_image(apod_info['url'], file_path)
            apod_id = add_apod_to_db(apod_info['title'], apod_info['explanation'], file_path, apod_info['sha256'])
        return apod_id
    return 0

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful. Zero, if unsuccessful       
    """
    # TODO: Complete function body
    conn = sqlite3.connect(image_cache_db)
    c = conn.cursor()
    c.execute("INSERT INTO apod_cache (title, explanation, file_path, sha256) VALUES (?, ?, ?, ?)",
              (title, explanation, file_path, sha256))
    apod_id = c.lastrowid
    conn.commit()
    conn.close()
    return apod_id

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    conn = sqlite3.connect(image_cache_db)
    c = conn.cursor()
    c.execute("SELECT id FROM apod_cache WHERE sha256=?", (image_sha256,))
    apod_id = c.fetchone()
    conn.close()
    if apod_id:
        return apod_id[0]
    return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    # Hint: Use regex and/or str class methods to determine the filename.
    file_name = re.sub(r'[^a-zA-Z0-9_]+', '_', image_title.strip()).strip('_')
    file_extension = os.path.splitext(image_url)[1]
    return os.path.join(image_cache_dir, file_name + file_extension)

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    # TODO: Put information into a dictionary
    conn = sqlite3.connect(image_cache_db)
    c = conn.cursor()
    c.execute("SELECT title, explanation, file_path FROM apod_cache WHERE id=?", (image_id,))
    row = c.fetchone()
    conn.close()
    if row:
        apod_info = {
            'title': row[0],
            'explanation': row[1],
            'file_path': row[2],
        }
    else:
        apod_info = {}
    return apod_info
    

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    conn = sqlite3.connect(image_cache_db)
    c = conn.cursor()
    c.execute("SELECT title FROM apod_cache")
    apod_titles = [row[0] for row in c.fetchall()]
    conn.close()
    return apod_titles

if __name__ == '__main__':
    main()