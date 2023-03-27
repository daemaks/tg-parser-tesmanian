import bs4 as _bs4
import requests as _requests


def _get_soup():
    # Set the headers to include a user-agent, which can help prevent the request from being blocked by the website.
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41"
    }
    url = "https://www.tesmanian.com/"
    response = _requests.get(url=url, headers=headers)
    soup = _bs4.BeautifulSoup(response.content, "html.parser")
    posts = soup.find_all("div", class_="blog-post-card__info")

    return posts


def _get_post_data(post):
    title = post.find("a").text.strip()
    link = f"https://www.tesmanian.com{post.find('a').get('href')}"
    slug = link.split("/")[-1]

    return title, link, slug


def get_news():
    posts = _get_soup()

    # Return a dictionary that maps each post slug to a dictionary containing its title and link.
    # This is done using a dictionary comprehension.
    return {
        slug: {"title": title, "link": link}
        for title, link, slug in [_get_post_data(post) for post in posts]
    }


def check_news(post_slug, old_dict):
    post = _get_soup()[0]
    _, _, slug = _get_post_data(post)

    if post_slug != slug:
        new_dict = get_news()
        new_posts = {}

        for key, value in new_dict.items():
            if key not in old_dict:
                new_posts.update({key: value})

        return new_posts
