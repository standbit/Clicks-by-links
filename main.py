from email.policy import default
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
    bitlink = response.json()["link"]
    return bitlink


def main():
    token = "Bearer 460748298a0b18b03b167966218c85ceac477e41"
    url = input("Введите ссылку, которую хотите сократить: ")
    default_url = "https://www.kinopoisk.ru/film/1320623/"
    try:
        bitlink = shorten_link(token, url)
    except requests.exceptions.HTTPError as err:
        print("General Error, incorrect link\n", str(err))
        print("Use default link: ", default_url)
        bitlink = shorten_link(token, default_url)
    except requests.ConnectionError as err:
        print("Connection Error. Check Internet connection.\n", str(err))
    print('Битлинк', bitlink)


if __name__ == "__main__":
    main()
