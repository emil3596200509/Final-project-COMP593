'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
import requests
from datetime import date

def main():
    # TODO: Add code to test the functions in this module
    apod_date = date.today()
    apod_info = get_apod_info(apod_date)
    if apod_info:
        print(f"APOD Info: {apod_info}")
        apod_image_url = get_apod_image_url(apod_info)
        print(f"APOD Image URL: {apod_image_url}")
    else:
        print("Failed to retrieve APOD info.")

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    # TODO: Complete the function body
    # Hint: The APOD API uses query string parameters: https://requests.readthedocs.io/en/latest/user/quickstart/#passing-parameters-in-urls
    # Hint: Set the 'thumbs' parameter to True so the info returned for video APODs will include URL of the video thumbnail image 
    api_key = "kHjw2LOGMfPzY6AVyZuk3sTuHOJNB95IGb1TGpuF"
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": api_key,
        "date": apod_date.isoformat() if isinstance(apod_date, date) else apod_date,
        "thumbs": True
    }
    resp = requests.get(base_url, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        return None

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    # TODO: Complete the function body
    # Hint: The APOD info dictionary includes a key named 'media_type' that indicates whether the APOD is an image or video
    if apod_info_dict["media_type"] == "image":
        return apod_info_dict["hdurl"]
    elif apod_info_dict["media_type"] == "video":
        return apod_info_dict["thumbnail_url"]
    else:
        return print("Media type is unknown ")

if __name__ == '__main__':
    main()