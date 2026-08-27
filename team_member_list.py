from library import UserDataSaver, get_config, ApiClient, decoder


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
                resp = client.get_large_json(cfg.TEAM_MEMBERS_URL, token="befdcb00d781aad4b4d650b6d741f502",
                data={
                                    "size": 9000,
                                    "currentNum": 1,
                                    "entity": {
                                        "userId": "28795450",
                                        "teamLevel": 0
                                    }
                                })
                
                saving_folder.save_user_json(f'852-62642070', resp.json().get("row"), "team_members")
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
