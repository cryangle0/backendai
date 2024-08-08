import requests
import fitz  # PyMuPDF
from typing import List
from io import BytesIO
import os

# 设置 API 的基本 URL
BASE_URL = "http://154.201.92.211:8001"


def convert_pdf_to_images(pdf_bytes: bytes) -> List[str]:
    """
    将 PDF 文件中的所有页面转换为图像，并返回图像文件路径列表。
    :param pdf_bytes: PDF 文件的二进制数据
    :return: 图像文件路径列表
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    image_paths = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = f"page_{page_num + 1}.png"
        pix.save(image_path)
        image_paths.append(image_path)

    return image_paths


def generate_completion(prompt: str) -> str:
    url = f"{BASE_URL}/gmini-completion"
    payload = {
        "prompt": prompt
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("text", "")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling generate_completion API: {str(e)}")


def generate_with_images(prompt: str, pdf_bytes: bytes) -> str:
    url = f"{BASE_URL}/generate-with-images"

    # 将PDF文件的二进制数据转换为图像
    image_paths = convert_pdf_to_images(pdf_bytes)

    # 打开图像文件
    files = [("files", (open(image_path, "rb"))) for image_path in image_paths]

    payload = {
        "prompt": prompt
    }

    try:
        response = requests.post(url, data=payload, files=files)
        response.raise_for_status()
        result = response.json()
        return result.get("text", "")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling generate_with_images API: {str(e)}")
    finally:
        # 清理生成的图像文件
        for image_path in image_paths:
            os.remove(image_path)