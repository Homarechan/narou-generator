import json
import requests
from bs4 import BeautifulSoup

main_url: str = "https://yomou.syosetu.com/rank/genrelist/type/daily_"

type_url = ["101/", "102/", "201/", "202/", "301/", "302/"]

urls = []
for type_ in type_url:
    urls.append(main_url + type_)


def main():
    ua = "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    headers = {"User-Agent": ua}

    soups = [None] * 4
    soups[0] = BeautifulSoup(requests.get(urls[0], headers=headers).text, "html.parser")
    soups[1] = BeautifulSoup(requests.get(urls[1], headers=headers).text, "html.parser")
    soups[2] = BeautifulSoup(requests.get(urls[2], headers=headers).text, "html.parser")
    soups[3] = BeautifulSoup(requests.get(urls[3], headers=headers).text, "html.parser")

    ranking_inbox = map(lambda soup: soup.find("div", class_="ranking_inbox"), soups)
    ranking_list = map(
        lambda soup: soup.find_all("div", class_="ranking_list"), ranking_inbox
    )
    rank_h = map(
        lambda ranking: map(lambda x: x.find("div", class_="rank_h"), ranking),
        ranking_list,
    )
    titles = map(lambda rank: map(lambda x: x.find("a").contents, rank), rank_h)

    title_dict = {}
    title_dict["異世界_恋愛"] = list(titles.__next__())
    title_dict["現実世界_恋愛"] = list(titles.__next__())
    title_dict["ハイファンタジー"] = list(titles.__next__())
    title_dict["ローファンタジー"] = list(titles.__next__())

    with open("title.json", "w") as fp:
        json.dump(title_dict, fp, ensure_ascii=False)


if __name__ == "__main__":
    main()
