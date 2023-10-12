import json
import requests
import random
import time
from bs4 import BeautifulSoup
from kafka import KafkaProducer
from fake_useragent import UserAgent

class Scraper:
    def __init__(self, url, kafka_topic, kafka_bootstrap_servers):
        self.url = url
        self.kafka_topic = kafka_topic
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.user_agent = UserAgent()
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def scrape_site(self):
        headers = {
            'User-Agent': self.user_agent.random
        }
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def find_country_info(self, soup):
        country_info = soup.find_all("div", {"class": "country-info"})
        return country_info

    def extract_data(self, country_info):
        data = []
        for country in country_info:
            strong_keys = country.select("div > strong")
            span_values = country.select("div > span")

            data.append({
                strong_keys[0].text: span_values[0].text,
                strong_keys[1].text: span_values[1].text,
                strong_keys[2].text: span_values[2].text
            })
        return data

    def scrape_with_delay(self):
        soup = self.scrape_site()
        country_info = self.find_country_info(soup)
        data = self.extract_data(country_info)
        for item in data:
            self.producer.send(self.kafka_topic, value=item)

        time.sleep(random.uniform(1, 3))

    def close_producer(self):
        self.producer.close()

if __name__ == '__main__':
    scraper = Scraper('https://www.scrapethissite.com/pages/simple/', 'kafta_teste', 'localhost:9092')
    scraper.scrape_with_delay()
    scraper.close_producer()