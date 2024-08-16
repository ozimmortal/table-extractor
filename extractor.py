import requests
import bs4
import uuid
import os
from requests.exceptions import HTTPError, Timeout

class Extractor:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_table(self, timeout: int = 60) -> str:
        try:
            response = self.session.get(self.url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Timeout:
            print("The request timed out")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None

    def extract_table(self) -> list[list[str]]:
        table_data = []
        try:
            html_content = self.fetch_table()
            if not html_content:
                return table_data

            soup = bs4.BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table')
            if not table:
                print("No table found on the page.")
                return table_data

            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td') or row.find_all('th')
                cols = [ele.text.strip() for ele in cols]
                table_data.append(cols)

            return table_data
        except Exception as e:
            print(f"An error occurred during table extraction: {e}")
            return []

    def save_to_file(self) -> str:
        try:
            table = self.extract_table()
            if not table:
                print("No data to save.")
                return None

            file_name = f'table-{uuid.uuid4()}.csv'
            with open(file_name, 'w') as f:
                for row in table:
                    f.write(';'.join(row))
                    f.write('\n')
            return os.path.abspath(file_name)
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
            return None

    def __del__(self):
        self.session.close()

