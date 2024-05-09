# Description

This project is a web scraper designed to extract product information from the Norland Biotech website. It retrieves data such as product descriptions, sentiment scores, categories, and keywords, and saves it into an Excel file for further analysis.

# Installation:

* nltk: Natural Language Toolkit for text processing and analysis.
* sklearn: Scikit-learn library for machine learning tools.
* bs4 (Beautiful Soup): Library for web scraping.
* pandas: Data manipulation and analysis library.
* requests: HTTP library for making requests to websites.
* lxml: XML and HTML parsing library.
* openpyxl: Library for reading and writing Excel files.

# Setup Instructions

1. Clone the repository to your local machine:

https://github.com/meravigupta/Norland-Biotech-Data-Scraper.git

2. Install the required dependencies using pip:

pip install -r requirements.txt

3. Run the scraper script:

python scrape_norlandbiotech.py

The scraped data will be saved to an Excel file `named norlandbiotech_data.xlsx` in the project directory.

# Approach

1. Data Retrieval: The scraper visits the Norland Biotech website, navigates through the product pages, and extracts relevant information from each product.

2. Data Enrichment: The scraped data is enriched using various AI techniques:
    * Summarization: Product descriptions are summarized to provide concise overviews of each product.
    * Sentiment Analysis: Sentiment scores are calculated for each product description to determine the overall sentiment (positive, negative, or neutral).
    * Categorization: Categories are extracted from product descriptions to classify products into specific groups.
    * Keyword Extraction: Keywords are extracted from product descriptions to identify important terms and topics.
    * Data Storage: The enriched data is stored in an Excel file (data2.xlsx) for easy access and analysis.

