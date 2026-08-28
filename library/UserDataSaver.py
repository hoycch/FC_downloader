import csv
import inspect
import json
from pathlib import Path
from urllib.parse import urlparse
import requests

class UserDataSaver:
    def __init__(self, folder):
        # Resolve folder relative to the script that creates this instance
        caller_frame = inspect.stack()[1]
        script_dir = Path(caller_frame.filename).resolve().parent
        self.output_dir = script_dir / folder

    def initialize_output_directory(self):
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_user_csv(self, username, data, filename):
        user_dir = self.output_dir / username
        user_dir.mkdir(parents=True, exist_ok=True)

        filepath = user_dir / f"{filename}.csv"

        with filepath.open(
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=data.keys()
            )

            writer.writeheader()
            writer.writerow(data)

    def save_user_json(self, username, data, filename):
        """
        Save a JSON-serializable object (dict, list, etc.) to a .json file
        under output_dir / username / {filename}.json
        """
        user_dir = self.output_dir / username
        user_dir.mkdir(parents=True, exist_ok=True)

        filepath = user_dir / f"{filename}.json"

        with filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_user_binary(self, username, data: bytes, filename: str, extension: str = "jpg"):
        """
        Save binary data (e.g. image bytes) to:
        output_dir / username / {filename}.{extension}
        """
        user_dir = self.output_dir / username
        user_dir.mkdir(parents=True, exist_ok=True)

        filepath = user_dir / f"{filename}.{extension.lstrip('.')}"

        with filepath.open("wb") as f:          # "wb" = write binary
            f.write(data)

    def download_option_picture(
        self,
        json_obj: dict,
        attr_name: str,
        username: str,
        extension: str = "jpg",
        timeout: int = 15
    ):
        url = json_obj.get(attr_name)
        if not url:
            return  # attribute missing or empty → do nothing

        try:
            resp = requests.get(url, timeout=1)
            resp.raise_for_status()          # raise if status is 4xx / 5xx

            self.save_user_binary(
                username=username,
                data=resp.content,
                filename=attr_name,
                extension=extension
            )
        except requests.RequestException as e:
            print(f"Failed to download {attr_name} from {url}: {e}")