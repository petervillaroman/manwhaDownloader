import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO
from reportlab.pdfgen import canvas


def download_image_to_memory(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        return BytesIO(response.content)
    return None


def images_to_pdf(images, output_pdf_path):
    if not images:
        print("No images to add to PDF")
        return

    c = canvas.Canvas(output_pdf_path)

    for image_data in images:
        img = Image.open(image_data)
        img_width, img_height = img.size
        c.setPageSize((img_width, img_height))
        c.drawInlineImage(img, 0, 0, width=img_width, height=img_height)
        c.showPage()

    c.save()
    print(f"PDF saved to {output_pdf_path}")


def download_chapter_to_pdf(chapter_number, base_url, pdf_directory):
    chapter_url = f"{base_url}{chapter_number}/"
    response = requests.get(chapter_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    images_data = []

    if chapter_number < 110:
        image_elements = soup.find_all('img', {'class': 'ts-main-image'})
    else:
        # Adapt to the new structure after chapter 110
        image_elements = soup.find_all(
            'img', src=True, alt="asura scans manhwa comic")

    for img in image_elements:
        image_url = img['src'].strip()
        image_data = download_image_to_memory(image_url)
        if image_data:
            images_data.append(image_data)

    if images_data:
        output_pdf_path = os.path.join(
            pdf_directory, f"Chapter_{chapter_number}.pdf")
        images_to_pdf(images_data, output_pdf_path)


def main():
    base_url = "https://asuratoon.com/4631981187-solo-leveling-chapter-"
    save_directory = "solo_leveling"
    pdf_directory = os.path.join(save_directory, "PDFs")

    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    for chapter in range(110, 115):  # Adjust as necessary
        download_chapter_to_pdf(chapter, base_url, pdf_directory)


if __name__ == "__main__":
    main()
