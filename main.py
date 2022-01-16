import requests
from urllib.parse import urlparse


def get_profile():
    url = "https://api-ssl.bitly.com/v4/user"
    headers = {
        "Authorization": "Bearer 460748298a0b18b03b167966218c85ceac477e41"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response


def shorten_link(token, link):
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
    payload = {
        "long_url": link
    }
    headers = {
        "Authorization": token
        }
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(token, link):
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    headers = {
        "Authorization": token
    }
    parsed = urlparse(link)
    bitlink = parsed.netloc + parsed.path
    response = requests.get(bitly_url.format(bitlink=bitlink), headers=headers)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def main():
    token = "Bearer 460748298a0b18b03b167966218c85ceac477e41"
    link = input("Введите ссылку, которую хотите сократить: ")
    default_url = "https://www.kinopoisk.ru/film/1320623/"
    try:
        bitlink = shorten_link(token, link)
        clicks_count = count_clicks(token, bitlink)
    except requests.exceptions.HTTPError as err:
        print("General Error, incorrect link\n", str(err))
    except requests.ConnectionError as err:
        print("Connection Error. Check Internet connection.\n", str(err))
    print("Битлинк:", bitlink)
    print("Количество кликов по ссылке:", clicks_count)


if __name__ == "__main__":
    main()
