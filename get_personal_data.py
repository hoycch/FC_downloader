from library import UserDataSaver, get_config, ApiClient, decoder, get_token


def main():
    
    login_list = [
        {'area_code': 852, 'username': '93727140'},
    ]
    failing_list = []
    saving_folder = UserDataSaver("bosses")
    for item in login_list:
        

        cfg = get_config(item["area_code"])
        
        with ApiClient(cfg) as client:
            for item in login_list:

                try:
                    token = client.login(item['username'], "donthack")
                    if token is not None:
                        json = client.get_single_json(cfg.USER_INFO_URL, token=token)
                        saving_folder.save_user_csv(item['username'], json.get("row"), "user_info")
                        
                        json = client.get_single_json(cfg.TEAM_INFO_URL, token=token)

                except AssertionError as e:
                    failing_list.append({"item":  item['username'], "reason": str(e)})

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
