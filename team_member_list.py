from library import UserDataSaver, get_config, ApiClient, decoder, get_token


def main():
    
    profile_list = {
        '86270534',
    }
    failing_list = []
    saving_folder = UserDataSaver("bosses")
    cfg = get_config(65)
    for item in profile_list:
        with ApiClient(cfg) as client:
            try:
                resp = client.get_large_json(cfg.TEAM_MEMBERS_URL, token="9a0167060529d6d3f8f5d259982107e6",
                data={
                                    "size": 8000,
                                    "currentNum": 1,
                                    "entity": {
                                        "userId": "65199054",
                                        "teamLevel": 0
                                    }
                                })
                
                saving_folder.save_user_csv(f'65-88888801', resp.json().get("row"), "team_members")
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
