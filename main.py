import requests


def get_profile():
    url = "https://api-ssl.bitly.com/v4/user"
    headers = {
        "Authorization": "Bearer 460748298a0b18b03b167966218c85ceac477e41"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response


def shorten_link(token, url):
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
    payload = {
        "long_url": url
    }
    headers = {
        "Authorization": token
        }
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["link"]


def main():
    token = "Bearer 460748298a0b18b03b167966218c85ceac477e41"
    url = "https://www.kinopoisk.ru/film/1320623/"
    print('Битлинк', shorten_link(token, url))


if __name__ == "__main__":
    main()
