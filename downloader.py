import requests
from bs4 import BeautifulSoup
import os


def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)


def download_chapter_images(chapter_number, base_url, save_directory):
    chapter_url = f"{base_url}{chapter_number}/"
    response = requests.get(chapter_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # This part is hypothetical, as it depends on the actual page structure
    # You would need to inspect the webpage to find the correct way to identify image URLs
    image_elements = soup.find_all('img', {'class': 'ts-main-image'})

    for i, img in enumerate(image_elements, start=1):
        image_url = img['src']
        save_path = os.path.join(
            save_directory, f"Chapter_{chapter_number}-{i}.jpg")
        download_image(image_url, save_path)
        print(f"Downloaded {save_path}")

# def download_chapter_images(chapter_number, base_url, save_directory):
#     chapter_url = f"{base_url}{chapter_number}/"
#     response = requests.get(chapter_url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find all images with the specified class
#     image_elements = soup.find_all('img', {'class': 'ts-main-image'})

#     for i, img in enumerate(image_elements, start=1):
#         image_url = img['src'].strip()  # Ensure there's no leading/trailing whitespace
#         save_path = os.path.join(save_directory, f"Chapter_{chapter_number}-{i}.jpg")
#         download_image(image_url, save_path)
#         print(f"Downloaded {save_path}")


def main():
    base_url = "https://asuratoon.com/4631981187-solo-leveling-chapter-"
    save_directory = "solo_leveling"

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for chapter in range(1, 11):  # Assuming chapters 1 through 200
        download_chapter_images(chapter, base_url, save_directory)


if __name__ == "__main__":
    main()
