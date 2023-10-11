import requests
from bs4 import BeautifulSoup as bs
import csv
import string
from urllib.parse import urljoin

# Constants
BASE_URL = "http://dosen.unand.ac.id/web/pencarian?cari={atoz}&act=dir"
TIMEOUT = 30
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}

# Function to extract and clean text from an element
def extract_text(element):
    return element.text.strip() if element else ''

def extract_pagination(element, base_url):
    try:
        return [urljoin(base_url, page['href']) for page in element.find_all('a', href=True)]
    except:
        return []

def extract_table(element, base_url):
    result = []
    for tr in element.find('tbody').find_all('tr'):
        result.append(urljoin(base_url, tr.find('a', href=True)['href']))
    return result

def extract_personal_info(element, url):
    info_table = element.find('table', {'id': 'w1'})
    nama, nip, nidn, jenis_kelamin, status, jabatan, unit, fakultas, pangkat, pendidikan_terakhir = [tr.text.split('\n')[1].strip() for tr in info_table.find_all('tr')]
    return [nama, url, nip, nidn, jenis_kelamin, status, jabatan, unit, fakultas, pangkat, pendidikan_terakhir]

s = requests.Session()

# Open a CSV file for writing
with open('data_dosen_unand.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = ['Nama', 'URL', 'NIP', 'NIDN', 'Jenis Kelamin', 'Status', 'Jabatan', 'Unit', 'Fakultas', 'Pangkat/Golongan', 'Pendidikan Terakhir']
    writer.writerow(header)

    for atoz in string.ascii_uppercase:
        url = BASE_URL.format(atoz=atoz)
        html = s.get(url, timeout=TIMEOUT, headers=HEADERS).content
        soup = bs(html, 'html.parser')

        # Extract pagination links for the current letter
        pagination_links = extract_pagination(soup.find('ul', class_='pagination'), url)[:-1]

        for page in pagination_links:
            html_ = s.get(page, timeout=TIMEOUT, headers=HEADERS).content
            soup_ = bs(html_, 'html.parser')

            # Extract profile links from the current page
            profile_links = extract_table(soup_, page)

            for profile_page in profile_links:
                html__ = s.get(profile_page, timeout=TIMEOUT, headers=HEADERS).content
                soup__ = bs(html__, 'html.parser')
                row = extract_personal_info(soup__, profile_page)

                if row:
                    writer.writerow(row)
                    f.flush()
