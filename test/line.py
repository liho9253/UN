import requests
import time


localtime = time.localtime()
result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
def post_data(message, token):
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        payload = {
            'message': message
        }
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload
        )
        if response.status_code == 200:
            print(f"Success -> {response.text}")
    except Exception as _:
        print(_)

if __name__ == "__main__":
    token = "u6bIfRFdGhcO5ysl7AZwCcDFoYs2AlZvOP98DPNO4Xd" 
    message = "現在時間: "+result
    post_data(message, token)