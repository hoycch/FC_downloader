from library import UserDataSaver, get_config, ApiClient, parse_phone
import profile_downloader



cfg = get_config(852)
saving_folder = UserDataSaver("testing")

login_list = ['53139343']

trying_passwords = ['827867']
profile_downloader.download_boss(login_list, trying_passwords, 852)