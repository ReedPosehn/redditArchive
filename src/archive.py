import requests
import shutil
import sys
import os
from bs4 import BeautifulSoup

__author__ = "Reed Posehn"
__version__ = "1.1"
__license__ = "MIT"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


def convert_to_old_reddit(URL):
    """Ensure that it is a reddit link, and if using www, convert to old for consistency

    URL -- The reddit URL we want to archive
    """
    if "https://www.reddit" in URL:
        URL = URL.replace("www.reddit", "old.reddit")
    if "https://old.reddit" not in URL:
        print("Please provide a valid reddit link.")
        sys.exit(0)
    return URL


def illegal_characters(str, img):
    """Filter out illegal characters, replace them with a blank string if not an image, otherwise a dash

    str -- the string to evaluate
    image -- int that describes whether the string should have illegal characters replaced with "" or "-"
    """
    remove_chars = ["*", '"', "/", "\\", "<", ">", ":", "|", "?"]
    for char in remove_chars:
        if img == 0:
            str = str.replace(char, "")
        else:
            str = str.replace(char, "-")
    return str


def create_directory(newDir):
    """Create a new directory

    newDir -- The name of the new directory we want to create
    """
    if not os.path.exists(newDir):
        try:
            os.makedirs(newDir)
        except:
            print("Error creating directory - check your URL.")
    else:
        if newDir != "backups":
            print("Directory already exists.")


def archive_page(title, markup, imgURLS):
    """Archive the desired content in a directory specified by the post title

    title -- The name of the new directory we want to create
    markup -- The name of the new directory we want to create
    imgURLS -- The name of the new directory we want to create
    """
    filename = title + ".html"
    new_HTML = os.open(
        os.path.join("backups\\" + title, filename), os.O_RDWR | os.O_CREAT
    )
    os.write(new_HTML, str(markup.prettify).encode())
    os.close(new_HTML)
    # Images
    for imgLink in imgURLS:
        response = requests.get(imgLink, stream=True)
        with open(
            "backups\\" + title + "\\" + illegal_characters(imgLink, 1), "wb"
        ) as out_file:
            print(out_file)
            shutil.copyfileobj(response.raw, out_file)
        del response
    print("Saved file.")


def package_web_page(argv):
    """Take an argument which should be a reddit URL to archive, and package it

    URL -- The reddit URL we want to archive
    """
    # Ensure the URL is using 'old' then grab the HTML and parse it
    URL = convert_to_old_reddit(argv[1])
    htmlPage = requests.get(URL, timeout=10, headers=headers)
    parsedHTML = BeautifulSoup(htmlPage.text, "html.parser")
    # We want to use the title as the folder name
    title = illegal_characters(parsedHTML.title.string, 0)
    # Grab the post images
    imgURLS = []
    for imgLink in parsedHTML.find_all("a", "post-link"):
        imgURLS.append(imgLink.get("href"))
    # Create directory to store backups
    create_directory("backups")
    # Create a new directory to store the archived reddit post information
    create_directory("backups\\" + title)
    # Place into the new directory the markup and images
    archive_page(title, parsedHTML, imgURLS)
