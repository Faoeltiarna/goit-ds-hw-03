from bs4 import BeautifulSoup
import requests
import json
import re
from unidecode import unidecode

URL = "http://quotes.toscrape.com"
URL_author = URL + "/author/"


def scraping_q_to_s():
    quotes = []
    authors = {}
    page = 1
    
    while True:
        html_page = requests.get(f"{URL}/page/{page}/")
        if "No quotes found" in html_page.text:
            break
        
        soup = BeautifulSoup(html_page.text, "html.parser")
        elements_scrap = soup.findAll("div", attrs={"class": "quote"})

        for element_scrap in elements_scrap:
            quote = element_scrap.find("span", attrs={"class": "text"}).getText()
            author_name = element_scrap.find("small", attrs={"class": "author"}).getText()
            tags = [tag.get_text() for tag in element_scrap.findAll("a", attrs={"class": "tag"})]
        
            quotes.append({
                "quote": quote,
                "author": author_name,
                "tags": tags
            })
            
            if author_name not in authors:
                author_name_url = unidecode(author_name).replace("'", "")
                author_url = URL_author + re.sub(r"[.\s']+", "-", author_name_url).strip("-")
                author_html = requests.get(author_url)
                author_soup = BeautifulSoup(author_html.text, "html.parser")
                
                born_date = author_soup.find("span", attrs={"class": "author-born-date"}).getText()
                born_location = author_soup.find("span", attrs={"class": "author-born-location"}).getText()
                description = author_soup.find("div", attrs={"class": "author-description"}).getText()
                
                authors[author_name] = {
                    "fullname": author_name,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description.strip()
                }
        page += 1
    
    return quotes, list(authors.values())


def save_qoutes_json(quotes, authors):
    with open("quotes.json", "w", encoding="utf-8") as fh:
        json.dump(quotes, fh, ensure_ascii=False, indent=4)
    
    with open("authors.json", "w", encoding="utf-8") as fh:
        json.dump(authors, fh, ensure_ascii=False, indent=4)
        

if __name__ == "__main__":
    quotes, authors = scraping_q_to_s()
    save_qoutes_json(quotes, authors)
    print(f"Saved {len(quotes)} quotes and {len(authors)} authors in JSON files.")