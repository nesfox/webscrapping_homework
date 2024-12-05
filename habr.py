import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


def find_articles_with_keywords(url):
    """
    The function returns a list with the date, title and link to the article
    param: url - link to resource
    return: relevant_articles - a list with the date, title and link to the article
    """
    # Send a get request to the specified page with headers
    response = requests.get(url, headers=HEADERS)

    # Checking the success of the response
    if response.status_code == 200:
        # Parsing HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding all article blocks
        articles = soup.find_all('article', class_='tm-articles-list__item')

        # Filter articles by keywords
        relevant_articles = []
        for article in articles:
            preview_info = article.text.lower()

            # Check for the presence of at least one keyword
            if any(keyword in preview_info for keyword in KEYWORDS):
                date_element = article.find('time', class_='tm-article-snippet__datetime-published')
                title_element = article.find('a', class_='tm-article-snippet__title-link')
                link_element = article.find('a', class_='tm-article-snippet__title-link')

                # Check that the elements are found
                if date_element and title_element and link_element:
                    date = date_element.get('title')
                    title = title_element.text
                    link = link_element['href']

                    # Form the output string
                    output_string = f"{date} – {title} – {link}"
                    relevant_articles.append(output_string)
                else:
                    print("Не удалось найти элементы для одной из статей.")

        return relevant_articles
    else:
        print(f"Произошла ошибка при получении страницы: статус-код {response.status_code}")
        return []


# Specify the URL of the page with fresh articles
url = 'https://habr.com/ru/articles/'

# Call the function to get a list of relevant articles
relevant_articles = find_articles_with_keywords(url)

# Output the matching articles to the console
if relevant_articles:
    for article in relevant_articles:
        print(article)
else:
    print("Нет статей, содержащих указанные ключевые слова.")