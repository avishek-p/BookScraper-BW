import requests #`requests` imported but unused
import sqlite3
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

def create_database():
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT ,
            currency TEXT,
            price REAL
        )
    """
    )

    conn.commit()
    conn.close()

def insert_book(title, currency, price):
    conn = sqlite3.connect("books.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO books (title, currency, price) VALUES (?, ?, ?)
""",
        (title, currency, price),
    )
    conn.commit()
    conn.close()


def scrape_book(url):
    response = requests.get(url)
    print(response.status_code)
    if response.status_code != 200:
        print(f"Failed to fetch the page, status code: {response.status_code}")
        return
    # Set encoding explicitly to handle special characters
    response.encoding = response.apparent_encoding
    print(response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    print(books)
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = price_text[1:]

        insert_book(title, currency, price)
        
# git tutorial       
# git config --global user.name "Avishek Pradhan"
# git config --global user.email "avishekmpradhan@outlook.com"

# install git
# create repository in github

# go to git bash
# git config --global user.name "Avishek Pradhan"
# git config --global user.email "avishekmpradhan@outlook.com"

# git init
# git status => check the current status of the files
# git diff => changes made
# git add. 
# git commit -m "Your changes to the code"
# create git repository
# push an existing repository from the command line

# always use this steps after code change
# git add.
# git commit - "Changes to the code"
# git push origin

# checking branch commit

create_database()
scrape_book(URL)