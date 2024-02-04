import requests
import shutil
import sys
import os
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}


def illegal_characters(str, img):
    """Filter out illegal characters, replace them with a blank string if not a image, otherwise a dash.

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


def packageWebpage(argv):
    URL = argv[1]
    # Ensure that it is a reddit link, and if using www, convert to old
    if "https://www.reddit" in URL:
        URL = URL.replace("www.reddit", "old.reddit")
    if "https://old.reddit" not in URL:
        print("Please provide a valid reddit link.")
        sys.exit(0)
    htmlPage = requests.get(URL, timeout=10, headers=headers)
    # print(htmlPage.text)
    parsedHTML = BeautifulSoup(htmlPage.text, "html.parser")
    # print(parsedHTML.prettify())
    # print(parsedHTML.title.string)
    title = parsedHTML.title.string
    title = illegal_characters(title, 0)
    # Grab the post images
    imgURLS = []
    for imgLink in parsedHTML.find_all("a", "post-link"):
        imgURLS.append(imgLink.get("href"))
    # Create directory to store backups
    if not os.path.exists("backups"):
        try:
            os.makedirs("backups")
        except:
            print("Error creating directory.")
    if not os.path.exists("backups\\" + title):
        try:
            os.makedirs("backups\\" + title)
            filename = title + ".html"
            new_HTML = os.open(
                os.path.join("backups\\" + title, filename), os.O_RDWR | os.O_CREAT
            )
            os.write(new_HTML, str(parsedHTML.prettify).encode())
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
        except:
            print("Error creating directory - check your URL.")
    else:
        print("Directory already exists.")


def main(argv):
    # Ensure we have at least one argument
    if len(argv) > 1:
        packageWebpage(argv)
    else:
        print("Please provide a URL to archive as the first argument.")


if __name__ == "__main__":
    main(sys.argv)
