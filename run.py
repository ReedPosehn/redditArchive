import sys
from src.archive import *


def main(argv):
    # Ensure we have at least one argument
    if len(argv) > 1:
        package_web_page(argv)
    else:
        print("Please provide a URL to archive as the first argument.")


if __name__ == "__main__":
    main(sys.argv)
