import oss2
import os

# 配置阿里云OSS
access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
bucket_name = 'shijunyun'
endpoint = 'YOUR_OSS_ENDPOINT'  # 例如 'oss-cn-hangzhou.aliyuncs.com'

# 初始化Bucket
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

def upload_file(file_path: str, directory: str) -> str:
    """
    上传文件到OSS指定目录
    :param file_path: 本地文件路径
    :param directory: OSS中的目录名称，例如 'resume'
    :return: 上传文件的URL
    """
    try:
        # 从文件路径中提取文件名
        file_name = file_path.split('/')[-1]
        # 构造OSS中的对象名称
        object_name = f"{directory}/{file_name}"
        bucket.put_object_from_file(object_name, file_path)
        url = f"https://{bucket_name}.{endpoint}/{object_name}"
        return url
    except oss2.exceptions.OssError as e:
        raise RuntimeError(f"Error uploading file to OSS: {str(e)}")

def delete_file(directory: str, file_name: str):
    """
    从OSS删除文件
    :param directory: OSS中的目录名称，例如 'resume'
    :param file_name: 文件名称，例如 'file.txt'
    """
    try:
        object_name = f"{directory}/{file_name}"
        bucket.delete_object(object_name)
    except oss2.exceptions.OssError as e:
        raise RuntimeError(f"Error deleting file from OSS: {str(e)}")

def get_file_info(directory: str, file_name: str) -> dict:
    """
    获取文件信息
    :param directory: OSS中的目录名称，例如 'resume'
    :param file_name: 文件名称，例如 'file.txt'
    :return: 文件信息字典
    """
    try:
        object_name = f"{directory}/{file_name}"
        head = bucket.head_object(object_name)
        return {
            "content_length": head.content_length,
            "last_modified": head.last_modified,
            "etag": head.etag,
            "content_type": head.content_type,
        }
    except oss2.exceptions.OssError as e:
        raise RuntimeError(f"Error getting file info from OSS: {str(e)}")

def list_files(prefix: str = '') -> list:
    """
    列出Bucket中的文件
    :param prefix: 文件前缀（例如：'resume/'）
    :return: 文件列表
    """
    try:
        files = []
        for obj in oss2.ObjectIterator(bucket, prefix=prefix):
            files.append(obj.key)
        return files
    except oss2.exceptions.OssError as e:
        raise RuntimeError(f"Error listing files in OSS: {str(e)}")

def download_file(directory: str, file_name: str, download_path: str):
    """
    下载文件到本地
    :param directory: OSS中的目录名称，例如 'resume'
    :param file_name: 文件名称，例如 'file.txt'
    :param download_path: 下载到本地的路径
    """
    try:
        object_name = f"{directory}/{file_name}"
        bucket.get_object_to_file(object_name, download_path)
    except oss2.exceptions.OssError as e:
        raise RuntimeError(f"Error downloading file from OSS: {str(e)}")
