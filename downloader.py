import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from reportlab.pdfgen import canvas
import re


def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)


def download_chapter_images(chapter_number, base_url, save_directory):
    chapter_url = f"{base_url}{chapter_number}/"
    response = requests.get(chapter_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    chapter_save_directory = os.path.join(
        save_directory, f"Chapter_{chapter_number}")
    if not os.path.exists(chapter_save_directory):
        os.makedirs(chapter_save_directory)

    image_elements = soup.find_all('img', {'class': 'ts-main-image'})
    for i, img in enumerate(image_elements, start=1):
        image_url = img['src'].strip()
        save_path = os.path.join(chapter_save_directory, f"{i}.jpg")
        download_image(image_url, save_path)
        print(f"Downloaded {save_path}")


def numerical_sort(value):
    """
    Extracts the number from the filename and returns it for sorting.
    """
    numbers = re.findall(r'\d+', value)
    return int(numbers[0]) if numbers else 0


def images_to_pdf(chapter_path, output_pdf_path):
    # List comprehension to get full paths of image files
    image_files = [os.path.join(chapter_path, f) for f in os.listdir(
        chapter_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Sort files based on their numeric value extracted from the filename
    image_files.sort(key=lambda x: int(
        os.path.splitext(os.path.basename(x))[0]))

    if not image_files:
        print(f"No images found in {chapter_path}")
        return

    c = canvas.Canvas(output_pdf_path)

    for image_path in image_files:
        img = Image.open(image_path)
        img_width, img_height = img.size
        c.setPageSize((img_width, img_height))
        c.drawImage(image_path, 0, 0, width=img_width, height=img_height)
        c.showPage()

    c.save()
    print(f"PDF saved to {output_pdf_path}")


def main():
    base_url = "https://asuratoon.com/4631981187-solo-leveling-chapter-"
    save_directory = "solo_leveling"
    pdf_directory = os.path.join(
        save_directory, "PDFs")  # New directory for PDFs

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    if not os.path.exists(pdf_directory):  # Ensure the PDF directory exists
        os.makedirs(pdf_directory)

    for chapter in range(45, 48):  # Adjust the range as necessary
        download_chapter_images(chapter, base_url, save_directory)
        chapter_path = os.path.join(save_directory, f"Chapter_{chapter}")
        # Save PDFs in the new directory
        output_pdf_path = os.path.join(pdf_directory, f"Chapter_{chapter}.pdf")
        images_to_pdf(chapter_path, output_pdf_path)


if __name__ == "__main__":
    main()
