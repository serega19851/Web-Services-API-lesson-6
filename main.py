from pathlib import Path
import os
import requests
import random
import pathlib
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv


def get_url_server(token):
    params = {
        "access_token": token,
        "v": "5.131",
        "group_id": "217042661",
    }
    response = requests.post(
        "https://api.vk.com/method/photos.getWallUploadServer", params=params
    )
    response.raise_for_status()
    return response.json()


def gets_random_url_comic():
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    random_number = random.randint(1, response.json()["num"])
    random_response = requests.get(
        f"https://xkcd.com/{random_number}/info.0.json"
    )
    random_response.raise_for_status()
    return random_response.json()


def get_name_file(url):
    comic_url = unquote(url, encoding="utf-8", errors="replace")
    url_component = urlparse(comic_url).path
    return pathlib.PurePath(url_component).name


def save_file_comic(url):
    directory_path = os.path.join(os.path.dirname(__file__), "images/")
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    name_file = get_name_file(url)
    response = requests.get(url)
    response.raise_for_status()
    with open(f"{directory_path}{name_file}", "wb") as file:
        file.write(response.content)


def uploading_server_comic(token):
    name_file = os.listdir("images/")[-1]
    with open(f"images/{name_file}", "rb") as file:
        server_url = get_url_server(token)["response"]["upload_url"]
        file = {'photo': file}
        response = requests.post(server_url, files=file)
        response.raise_for_status()
        return response.json()


def saves_photo_server(token):
    decoded_response = uploading_server_comic(token)
    params = {
        "access_token": token,
        "v": "5.131",
        "group_id": "217042661",
        "server": decoded_response["server"],
        "photo": decoded_response["photo"],
        "hash": decoded_response["hash"],
    }
    response = requests.post(
        "https://api.vk.com/method/photos.saveWallPhoto", params=params
    )
    response.raise_for_status()
    return response.json()


def publishes_comic(token):
    alt = gets_random_url_comic()["alt"]
    group_id = -217042661
    owner_id = saves_photo_server(token)["response"][0]["owner_id"]
    media_id = saves_photo_server(token)["response"][0]["id"]
    params = {
        "access_token": token,
        "v": "5.131",
        "message": alt,
        "owner_id": group_id,
        "from_group": 1,
        "media_id": media_id,
        "attachments": f"photo{owner_id}_{media_id}"
    }
    response = requests.post(
        "https://api.vk.com/method/wall.post",
        params=params
    )
    response.raise_for_status()
    for file_comic in os.listdir("images/"):
        os.remove(f"images/{file_comic}")


def main():
    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    comic = gets_random_url_comic()["img"]
    save_file_comic(comic)
    uploading_server_comic(vk_token)
    saves_photo_server(vk_token)
    publishes_comic(vk_token)


if __name__ == '__main__':
    main()
