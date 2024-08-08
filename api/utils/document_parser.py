import fitz  # PyMuPDF
from docx import Document
from PIL import Image, ImageDraw, ImageFont
import os


def pdf_to_images(pdf_path, output_folder, zoom=2.0, rotation=0):
    """
    将PDF的每一页转换为图像并保存到指定文件夹。

    参数:
        pdf_path (str): PDF 文件路径。
        output_folder (str): 输出图像文件夹路径。
        zoom (float): 缩放比例。
        rotation (int): 旋转角度。

    返回:
        list: 保存的图像文件路径列表。
    """
    try:
        # 打开PDF文件
        document = fitz.open(pdf_path)

        # 检查输出文件夹是否存在，不存在则创建
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 保存的图像文件路径列表
        image_paths = []

        # 循环处理每页
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # 将pix转换为Pillow图像对象
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            if rotation != 0:
                img = img.rotate(rotation, expand=True)

            image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
            img.save(image_path, format="PNG")
            image_paths.append(image_path)
            print(f"Saved page {page_num + 1} as {image_path}")

        return image_paths
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []


def word_to_images(word_path, output_folder):
    """
    将Word文档的每一页转换为图像并保存到指定文件夹。

    参数:
        word_path (str): Word 文件路径。
        output_folder (str): 输出图像文件夹路径。

    返回:
        list: 保存的图像文件路径列表。
    """
    try:
        # 打开Word文件
        document = Document(word_path)

        # 初始化字体（请确保系统中安装了支持中文的字体）
        font_path = "C:/Windows/Fonts/simhei.ttf"  # Windows 示例
        try:
            font = ImageFont.truetype(font_path, 15)
        except IOError:
            font = ImageFont.load_default()

        # 保存的图像文件路径列表
        image_paths = []

        # 循环处理每个段落（简单模拟分页处理）
        for i, para in enumerate(document.paragraphs):
            text = para.text
            # 创建一个白色背景的图像
            image = Image.new("RGB", (800, 100), "white")
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), text, font=font, fill="black")

            image_path = os.path.join(output_folder, f"word_page_{i + 1}.png")
            image.save(image_path)
            image_paths.append(image_path)

        return image_paths
    except Exception as e:
        print(f"Error converting Word to images: {e}")
        return []


def create_analysis_report_md(content, output_folder):
    # 检查并创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 完整的文件路径
    markdown_file_path = os.path.join(output_folder, "简历分析报告.md")

    # 将内容写入Markdown文件
    with open(markdown_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return markdown_file_path
