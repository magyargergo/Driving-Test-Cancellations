import json
import os
import random
import requests
import urllib3

from bs4 import BeautifulSoup


def get_page(url, proxy=None, proxy_auth=None, binary=False, verify=False, timeout=300):
    """Get data of the page (File binary of Response text)"""
    urllib3.disable_warnings()
    proxies = None
    if proxy:
        if proxy_auth:
            proxy = proxy.replace("http://", "")
            username = proxy_auth["username"]
            password = proxy_auth["password"]
            proxies = {
                "http": f"http://{username}:{password}@{proxy}",
                "https": f"http://{username}:{password}@{proxy}",
            }
        else:
            proxies = {"http": proxy, "https": proxy}
    retry = 3  # Retry 3 times
    while retry > 0:
        try:
            with requests.Session() as session:
                response = session.get(
                    url, proxies=proxies, verify=verify, timeout=timeout
                )
                if binary:
                    return response.content
                return response.text
        except requests.exceptions.ConnectionError:
            retry -= 1


def get_proxies():
    """Get free proxy list of https://free-proxy-list.net/"""
    parser = BeautifulSoup(get_page("https://free-proxy-list.net/"), "html.parser")
    proxies = list()
    for element in parser.find("table").find_all("tr")[1:-1]:
        more = element.find_all("td")[:2]
        proxies.append(
            str(more[0]).replace("<td>", "").replace("</td>", "")
            + ":"
            + str(more[1])
            .replace("<td>", "")
            .replace("</td>", "")
            .replace("https://", "")
            .replace("http://", "")
        )
    return proxies


def get_random_proxy():
    """Get random one proxy list"""
    return random.choice(get_proxies())


def fix_exit_type_flag(user_data_dir):
    # fix exit_type flag to prevent tab-restore nag
    try:
        with open(
            os.path.join(user_data_dir, "Default/Preferences"),
            encoding="latin1",
            mode="r+",
        ) as fs:
            config = json.load(fs)
            if config["profile"]["exit_type"] is not None:
                # fixing the restore-tabs-nag
                config["profile"]["exit_type"] = None
            fs.seek(0, 0)
            json.dump(config, fs)
    except Exception as e:
        pass
