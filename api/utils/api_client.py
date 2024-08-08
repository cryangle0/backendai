import requests
from typing import List

# 设置 API 的基本 URL
BASE_URL = "http://154.201.92.211:8001"

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

def generate_with_images(prompt: str, file_paths: List[str]) -> str:
    url = f"{BASE_URL}/generate-with-images"
    files = [("files", (open(file_path, "rb"))) for file_path in file_paths]
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
