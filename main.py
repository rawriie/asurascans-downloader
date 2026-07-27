import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from io import BytesIO
import os
import argparse
import zipfile
parser = argparse.ArgumentParser()

parser.add_argument(
    "-u",
    required=True,
    help="manhwa link",
    
)

parser.add_argument(
    "-f",
    required=True,
    choices=["cbz", "pdf"],
    help="Output format (cbz or pdf)"
)

args = parser.parse_args()


base_url = "https://asurascans.com"
url = args.u

session = requests.Session()


soup = BeautifulSoup(session.get(url).text, "html.parser")

chapter_links = soup.select_one(".divide-y").select("a")

os.makedirs(soup.title.text, exist_ok=True)


def download_image(args):
    image_url, filename = args

    try:
        response = session.get(image_url, timeout=15)

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    except Exception as e:
        print("Failed:", image_url, e)
        return None


def create_cbz(image_files, output):
    with zipfile.ZipFile(f"{soup.title.text}/{output}.cbz", "w", compression=zipfile.ZIP_DEFLATED) as cbz:
        for img in image_files:
            cbz.write(img)

def create_pdf(image_files, output):
    images = []

    for file in image_files:
        img = Image.open(file).convert("RGB")
        images.append(img)

    if images:
        images[0].save(
            f"{soup.title.text}/{output}.pdf",
            save_all=True,
            append_images=images[1:]
        )



for chapter_num, link in enumerate(reversed(chapter_links), start=1):

    chapter_url = base_url + link["href"]
    print("Chapter:", chapter_num)

    page_soup = BeautifulSoup(
        session.get(chapter_url).text,
        "html.parser"
    )

    container = page_soup.select_one(".max-w-full")

    image_links = []

    #get all images
    for div in container.find_all("div"):
        img = div.find("img")

        image_links.append(img["src"])
            

    os.makedirs("temp", exist_ok=True)

    #list all images to download
    tasks = [
        (img, f"temp/{i:03}.webp")
        for i, img in enumerate(image_links, start=1)
    ]

    with ThreadPoolExecutor(max_workers=100) as executor:
        files = list(executor.map(download_image, tasks))


    #remove failed downloads
    files = [f for f in files if f]


    
    file_name = f"chapter_{chapter_num}"

    match args.f:
        case "pdf":
            create_pdf(files, file_name)
        case "cbz":
            create_cbz(files, file_name)

    print("Created:", file_name)


    # Clean temporary images
    for f in files:
        os.remove(f)