import requests
from bs4 import BeautifulSoup
import sqlite3

# Function to scrape news articles
def scrape_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    news_list = []

    for article in articles:
        headline = article.find('h2').get_text().strip()
        summary = article.find('p').get_text().strip()
        news_list.append((headline, summary))

    return news_list

# Function to create a SQLite database and store news articles
def create_news_database(news):
    conn = sqlite3.connect('news_database.db')
    c = conn.cursor()
    
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 headline TEXT,
                 summary TEXT)''')
    
    # Insert data into the table
    c.executemany('INSERT INTO news (headline, summary) VALUES (?, ?)', news)
    
    # Commit and close the connection
    conn.commit()
    conn.close()

# URL of the news website to scrape
url = 'https://example.com/news'

# Scrape news articles
news_articles = scrape_news(url)

# Create and store news articles into the database
create_news_database(news_articles)

print("News articles scraped and stored into the database successfully!")
