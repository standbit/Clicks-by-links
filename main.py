import argparse
import os
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv


def shorten_link(token, link):
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
    payload = {
        "long_url": link
    }
    headers = {
        "Authorization": f"Bearer {token}"
        }
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()["link"]
    return bitlink


def count_clicks(token, link):
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"   # Noqa E501
    headers = {
        "Authorization": f"Bearer {token}"
    }
    parsed = urlparse(link)
    bitlink = "{}{}".format(parsed.hostname, parsed.path)
    response = requests.get(
        bitly_url.format(bitlink=bitlink),
        headers=headers)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(link, token):
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    parsed = urlparse(link)
    unknown_link = "{}{}".format(parsed.hostname, parsed.path)
    response = requests.get(
        bitly_url.format(bitlink=unknown_link),
        headers=headers)
    return response.ok


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "link",
        help="""will make bit-link from ordinary link\
            or will count clicks if bitlink inputed""")
    return parser


def main():
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    args = create_parser().parse_args()
    link = args.link
    if is_bitlink(link, token):
        try:
            clicks_count = count_clicks(token, link)
            print("Количество кликов по ссылке:", clicks_count)
        except requests.exceptions.HTTPError as err:
            print("General Error, incorrect link\n", str(err))
        except requests.ConnectionError as err:
            print("Connection Error. Check Internet connection.\n", str(err))
    else:
        try:
            bitlink = shorten_link(token, link)
            print("Битлинк:", bitlink)
        except requests.exceptions.HTTPError as err:
            print("General Error, incorrect link\n", str(err))
        except requests.ConnectionError as err:
            print("Connection Error. Check Internet connection.\n", str(err))


if __name__ == "__main__":
    main()
