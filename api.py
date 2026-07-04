import requests

API_KEY = "goldapi-9620881c114b8d52ed6a5ce4fffd7196-io"

def get_gold_rate():
    url = "https://www.goldapi.io/api/XAU/INR"

    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # Price per gram
            gold_rate = round(data["price"] / 31.1035, 2)

            return gold_rate

        else:
            print(response.text)
            return None

    except Exception as e:
        print(e)
        return None
    
def get_silver_rate():

    url = "https://www.goldapi.io/api/XAG/INR"

    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # Price per gram
            silver_rate = round(data["price"] / 31.1035, 2)

            return silver_rate

        return None

    except:
        return None