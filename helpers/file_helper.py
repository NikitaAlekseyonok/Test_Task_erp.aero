import io
from typing import Any
from PIL import Image
import PyPDF2
import fitz
import pymupdf
from pyzbar.pyzbar import decode


def extract_text_from_pdf(pdf_file_path: str) -> [str]:
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_text = ''
        reader = PyPDF2.PdfReader(pdf_file, strict=True)

        for page in reader.pages:
            content = page.extract_text()
            pdf_text += content
    return pdf_text


def render_pdf_to_images(pdf_path: str, zoom=2) -> [Any]:
    images = []
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append(img)

    return images


def decode_barcodes(images: [Any]) -> [dict]:
    decoded_barcodes = []
    for img in images:
        decoded_objects = decode(img)
        for obj in decoded_objects:
            try:
                decoded_barcodes.append({
                    "type": obj.type,
                    "data": obj.data.decode("utf-8"),
                    "rect": [obj.rect.left,
                             obj.rect.top,
                             obj.rect.left + obj.rect.width,
                             obj.rect.top + obj.rect.height],
                })
            except (AttributeError, UnicodeDecodeError):
                print("Ошибка! Не получилось декадировть баркод")

    decoded_barcodes.sort(key=lambda x: x["rect"][1])
    return decoded_barcodes


def find_text_coordinates(pdf_file_path: str, search_text: str) -> pymupdf.Rect:
    if len(search_text) == 0:
        return None

    pdf_file = fitz.open(pdf_file_path)
    text_coordinates = []

    for page_num in range(pdf_file.page_count):
        page = pdf_file.load_page(page_num)
        text_instances_on_page = page.search_for(search_text)

        try:
            text_coordinates = [round(text_instances_on_page[0].x0),
                                round(text_instances_on_page[0].y0),
                                round(text_instances_on_page[0].x1),
                                round(text_instances_on_page[0].y1)]
        except IndexError:
            print(f"Ошибка! В файле {pdf_file_path} нет текста {search_text}")

    return text_coordinates
