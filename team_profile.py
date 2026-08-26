from library import UserDataSaver, get_config, ApiClient, decoder, get_token


def main():
    
    profile_list = {
        '28795450',
    }
    failing_list = []
    saving_folder = UserDataSaver("bosses")
    cfg = get_config(852)
    for item in profile_list:
        with ApiClient(cfg) as client:
            try:
                
                json = client.get_single_json(cfg.TEAM_INFO_URL, token="45e48ed25f19391a551a0c79563faf1b", data={"userId": item})
                saving_folder.save_user_csv(f'82-{json.get("row").get("teamName")}', json.get("row"), "team_info")
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
