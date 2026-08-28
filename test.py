from library import UserDataSaver, get_config, ApiClient, parse_phone



cfg = get_config(852)
saving_folder = UserDataSaver("testing")



with ApiClient(cfg) as client:
    try:
        token = client.login(53139343, "827867")
        if token is not None:
            json = client.get_single_json(cfg.USER_INFO_URL, token=token)
            saving_folder.save_user_csv("53139343", json.get("row"), "user_info")
            saving_folder.download_option_picture(json.get("row"), "avatar", "53139343")
            json = client.get_single_json(cfg.AUTH_CHECK_URL, token=token)
            saving_folder.save_user_csv("53139343", json.get("row"), "Invest_Auth")
            saving_folder.download_option_picture(json.get("row"), "sfz1", "53139343")
            saving_folder.download_option_picture(json.get("row"), "sfz2", "53139343")
    except AssertionError as e:
        print(e)
