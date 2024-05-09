# Import necessary libraries
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import pandas as pd
import requests
import nltk
import re

# Download NLTK resources
# for tokenization
nltk.download('punkt')
# for sentiment analysis
nltk.download('vader_lexicon')

# Function to summarize product description
def summarize_description(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Calculate the length of each sentence
    sentence_lengths = [len(sentence.split()) for sentence in sentences]

    # Sort the sentences based on their lengths
    sorted_sentences = [sentence for _, sentence in sorted(zip(sentence_lengths, sentences), reverse=True)]

    # Choose the top N sentences as the summary
    summary_length = min(3, len(sorted_sentences))  # Choose the top 3 sentences as the summary
    summary = ' '.join(sorted_sentences[:summary_length])

    return summary

# Initialize SentimentIntensityAnalyzer for sentiment analysis
sia = SentimentIntensityAnalyzer()

# Function to extract categories from text
def extract_categories(text):
    categories = ["food colorant", "cosmetic additive", "dietary supplement", "health food", "algae", "antioxidant", "minerals"]
    # Tokenize the text into words
    words = re.findall(r'\b\w+\b', text.lower())
    # Check if any of the words match any of the categories
    matched_categories = [cat for cat in categories if any(cat_word in words for cat_word in cat.split())]
    return matched_categories

# Function to extract keywords from text using CountVectorizer
def extract_keywords(text):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    keywords = [feature_names[i] for i in X.toarray()[0].argsort()[0:10]]
    return keywords

# Function to prettify string by removing unnecessary characters and whitespaces
def _prettify_string(s):
    if not s:
        return ''
    s = s.replace('\n', ' ')
    s = s.replace('\t', ' ')
    s = s.replace('\r', ' ')
    s = s.replace('\xa0', ' ')
    s = s.replace('General Introduction:', ' ')
    s = s.replace('General introduction:', ' ')
    s = s.strip()
    s = re.sub(r'\s+', ' ', s, flags=re.I).strip()
    return s

# Function to scrape data from website and save it to Excel
def get_data():
    base_url = "https://www.norlandbiotech.com"
    #If you can use Guest User-Agent
    """from fake_useragent import UserAgent

    # Create an instance of UserAgent
    ua = UserAgent()

    # Get a random user agent
    random_user_agent = ua.random

    # Use it in your headers
    headers = {
        "User-Agent": random_user_agent
    }"""
    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    session = requests.session()
    response = session.get(base_url, headers=headers, verify=False, timeout=20)
    print(response.status_code)
    content = response.content
    soup = BeautifulSoup(content, "lxml")
    menu_tag = soup.find("div", {"class": "menu"})
    mainlevel_tags = menu_tag.find_all("li", {"class": "mainlevel"})
    if len(mainlevel_tags) >= 2:
        products_tag = mainlevel_tags[1].find("a")
        products = products_tag.get("href", "")
        if not products:
            exit(1)
        products_url = f"{base_url}{products}"
        products_response = session.get(products_url, headers=headers, verify=False, timeout=20)
        products_content = products_response.content
        products_soup = BeautifulSoup(products_content, "lxml")
        p_products = products_soup.find("div", {"class": "e_box e_box-000 p_products"})
        all_product_urls_tag = p_products.find_all("div", {"class": "e_box e_ProductBox-001 p_Product"})
        all_products_info = []
        for all_product_url_tag in all_product_urls_tag:
            product_details = {}
            product_page = all_product_url_tag.find("h3")
            if not product_page:
                continue
            single_product_url = f"{base_url}{product_page['data-url']}"
            single_product_response = session.get(single_product_url, headers=headers, verify=False, timeout=20)
            single_product_content = single_product_response.content
            single_product_soup = BeautifulSoup(single_product_content, "lxml")
            contentdiv_tag = single_product_soup.find("div", {"class": "reset_style js-reset_style js-adapMobile"})
            if single_product_url in ["https://www.norlandbiotech.com/product/13.html", "https://www.norlandbiotech.com/product/4.html"]:
                paragraphs = contentdiv_tag.find('p')
                if paragraphs:
                    summary = _prettify_string(paragraphs.text)
            else:
                product_summary = contentdiv_tag.find_all("div")
                summary = ' '.join([div.get_text() for div in product_summary[0:3] if div.get_text()])
                summary = _prettify_string(summary)
                if re.search(r"Product", summary):
                    summary = ""
                if not summary:
                    paragraphs = contentdiv_tag.find_all('p')
                    summary = ' '.join([p.get_text() for p in paragraphs[0:3] if p.get_text()])
                    summary = _prettify_string(summary)
            if summary:
                product_details["general_introduction"] = summary
                summarize_desc = summarize_description(summary)
                product_details["summarize_description"] = summarize_desc
                sentiment_scores = sia.polarity_scores(summary)
                product_details["sentiment_scores"] = sentiment_scores
                categories = extract_categories(summary)
                product_details["categories"] = categories
                keywords = extract_keywords(summary)
                product_details["keywords"] = keywords
                all_products_info.append(product_details)

        # Convert data to DataFrame
        df = pd.DataFrame(all_products_info)
        df['categories'] = df['categories'].apply(', '.join)
        df['keywords'] = df['keywords'].apply(', '.join)

        # Save DataFrame to Excel
        df.to_excel("norlandbiotech_data.xlsx", index=False)

# Main block
if __name__ == "__main__":
    get_data()
