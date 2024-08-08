import requests
import fitz  # PyMuPDF
from typing import List
from io import BytesIO

# 设置 API 的基本 URL
BASE_URL = "http://154.201.92.211:8001"


def download_pdf(url: str) -> bytes:
    """
    从URL下载PDF文件并返回其二进制内容。
    :param url: PDF文件的URL
    :return: PDF文件的二进制内容
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def convert_pdf_to_images(pdf_bytes: bytes) -> List[BytesIO]:
    """
    将 PDF 文件中的所有页面转换为图像，并返回图像文件的字节流列表。
    :param pdf_bytes: PDF 文件的二进制数据
    :return: 图像文件的字节流列表。
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    image_streams = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_byte_array = BytesIO(pix.tobytes(output="png"))
        img_byte_array.seek(0)
        image_streams.append(img_byte_array)

    return image_streams


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


def generate_with_images(prompt: str, pdf_url: str) -> str:
    url = f"{BASE_URL}/generate-with-images"

    # 下载PDF文件
    pdf_bytes = download_pdf(pdf_url)

    # 将PDF文件的二进制数据转换为图像
    image_streams = convert_pdf_to_images(pdf_bytes)

    # 打开图像文件
    files = [("files", (f"page_{i + 1}.png", img_stream, "image/png")) for i, img_stream in enumerate(image_streams)]

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

# 示例使用
if __name__ == "__main__":
    def test_generate_with_images():
        # 提供PDF文件的URL
        pdf_url = "https://example.com/path/to/your/pdf/file.pdf"

        prompt = "请分析这位求职者的简历与以下职位的匹配度..."

        try:
            result = generate_with_images(prompt, pdf_url)
            print("API Result:\n", result)
        except RuntimeError as e:
            print(e)

    test_generate_with_images()
