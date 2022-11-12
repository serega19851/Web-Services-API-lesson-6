from pathlib import Path
import os
import requests
import random
import pathlib
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv


def get_server_url(token, group_id):
    params = {
        "access_token": token,
        "v": "5.131",
        "group_id": group_id
    }
    response = requests.post(
        "https://api.vk.com/method/photos.getWallUploadServer", params=params
    )
    response.raise_for_status()
    return response.json()


def get_random_comic_url():
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    random_number = random.randint(1, response.json()["num"])
    random_response = requests.get(
        f"https://xkcd.com/{random_number}/info.0.json"
    )
    random_response.raise_for_status()
    return random_response.json()


def get_file_name(url):
    comic_url = unquote(url, encoding="utf-8", errors="replace")
    url_component = urlparse(comic_url).path
    return pathlib.PurePath(url_component).name


def creates_directory():
    directory_path = Path.cwd() / "images"
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def save_comic_file(url, file_name):
    response = requests.get(url["img"])
    response.raise_for_status()
    with open(Path.cwd() / "images" / f"{file_name}", "wb") as file:
        file.write(response.content)


def download_server_comic(server_url):
    name_file = os.listdir("images")[0]
    with open(Path.cwd() / "images" / f"{name_file}", "rb") as file:
        file = {'photo': file}
        response = requests.post(server_url, files=file)
    response.raise_for_status()
    return response.json()


def save_photo_server(token, group_id, decoded_response):
    params = {
        "access_token": token,
        "v": "5.131",
        "group_id": group_id,
        "server": decoded_response["server"],
        "photo": decoded_response["photo"],
        "hash": decoded_response["hash"],
    }
    response = requests.post(
        "https://api.vk.com/method/photos.saveWallPhoto", params=params
    )
    response.raise_for_status()
    return response.json()


def publish_comic(token, group_id, alt, decoded_response):
    params = {
        "access_token": token,
        "v": "5.131",
        "message": alt["alt"],
        "owner_id": f"-{group_id}",
        "from_group": 1,
        "media_id": decoded_response["id"],
        "attachments":
            f"photo" f"{decoded_response['owner_id']}_{decoded_response['id']}"
    }
    response = requests.post(
        "https://api.vk.com/method/wall.post",
        params=params
    )
    response.raise_for_status()


def deletes_file():
    os.remove(Path.cwd() / "images" / os.listdir("images")[0])


def main():
    load_dotenv()
    creates_directory()
    vk_group_id = os.getenv("VK_GROUP_ID")
    vk_token = os.getenv("VK_TOKEN")
    random_comic_response = get_random_comic_url()
    file_name = get_file_name(random_comic_response["img"])
    server_url = get_server_url(vk_token, vk_group_id)["response"][
        "upload_url"]
    try:
        save_comic_file(random_comic_response, file_name)
        server_comic_response = download_server_comic(server_url)
        decoded_response = save_photo_server(
            vk_token, vk_group_id, server_comic_response
        )["response"][0]
        publish_comic(
            vk_token, vk_group_id, random_comic_response, decoded_response
        )
    finally:
        deletes_file()


if __name__ == '__main__':
    main()
