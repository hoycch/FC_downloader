from library import get_config, ApiClient, decoder

def main():
    
    register_list = [
        {'area_code': 852, 'username': '88888888'},
        {'area_code': 852, 'username': '28795450'},
        {'area_code': 852, 'username': '69030025'},
        {'area_code': 852, 'username': '86553782'},
        {'area_code': 852, 'username': '85486468'},
        {'area_code': 852, 'username': '98853629'},
        {'area_code': 852, 'username': '14402953'},
        {'area_code': 852, 'username': '13329254'},
        {'area_code': 852, 'username': '34605159'},
        {'area_code': 853, 'username': '85486468'},
        {'area_code': 853, 'username': '70925799'},
        {'area_code': 65, 'username': '65199054'},
        {'area_code': 65, 'username': '77193005'},
        {'area_code': 65, 'username': '19826891'},
        {'area_code': 65, 'username': '38719392'},
        {'area_code': 65, 'username': '22360788'},
        {'area_code': 65, 'username': '81144275'},
        {'area_code': 65, 'username': '15873350'},

    ]
    failing_list = []

    for item in register_list:
        

        cfg = get_config(item["area_code"])
        
        with ApiClient(cfg) as client:

            resp = client.get(cfg.BASE_URL + "/api/kaptcha/captcha")
            captcha_data = resp.json()['row']

            # Decode the captcha image
            captcha_image = decoder.data_url_to_image(captcha_data)

            captcha_image.show()  # Display the captcha image for manual solving
            captcha_code = input("Enter the48 captcha code: ")
                    # Generic


        try:
            resp = client.post(cfg.BASE_URL + "/api/user/register", 
                data={
                    "areaCode": f"+{item['area_code']}",            
                    "username": "010" + item["username"],
                    "invitees": item["username"],
                    "password": "donthack",
                    "captchaCode": f"{captcha_code}",
                })
            # Test 1: item must be an integer
            print(resp.json()['info'])
            if resp.json()['info'] == "成功":
                raise AssertionError(f"{item['username']}: {resp.json()['info']}")
            
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


        # # Per-request extras
        # resp = client.login(
        #     "user", "pass",
        #     extra_headers={"x-request-id": "123"},
        #     extra_fields={"captcha": "xyz"},
        # )

if __name__ == "__main__":
    main()