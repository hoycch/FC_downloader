import csv
import inspect
from pathlib import Path


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