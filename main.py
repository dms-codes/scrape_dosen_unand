import requests
from bs4 import BeautifulSoup as bs
import csv
import string
from urllib.parse import urljoin

# Constants
#http://dosen.unand.ac.id/web/pencarian?cari=A&act=dir&page=9
BASE_URL = "http://dosen.unand.ac.id/web/pencarian?cari={atoz}&act=dir"
TIMEOUT = 30
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
}

# Function to extract and clean text from an element
def extract_text(element):
    if element:
        return element.text.strip()
    return ''

def extract_pagination(element,url):
    try:
        return [urljoin(url,page['href']) for page in element.find_all('a', href=True)]
    except:
        return []
    
def extract_table(element,url):
    result = []
    for tr in element.find('tbody').find_all('tr'):
        result.append(urljoin(url,tr.find('a',href=True)['href']))
    return result

def extract_personal(element,url):
    #for i,tr in enumerate(element.find('table', {'id':'w1'}).find_all('tr')):
    #    print(i,tr.text.split('\n'))
    nama, nip, nidn, jenis_kelamin, status, jabatan, unit, fakultas, pangkat, pendidikan_terakhir = [tr.text.split('\n')[1].strip() for tr in element.find('table', {'id':'w1'}).find_all('tr')]
    print(nama, url, nip, nidn, jenis_kelamin, status, jabatan, unit, fakultas, pangkat, pendidikan_terakhir)
    return [nama, url, nip, nidn, jenis_kelamin, status, jabatan, unit, fakultas, pangkat, pendidikan_terakhir]

s = requests.Session()

# Fetch the HTML content
with open('data_dosen_unand.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = ['Nama', 'URL', 'NIP', 'NIDN', 'Jenis Kelamin', 'Status', 'Jabatan', 'Unit', 'Fakultas', 'Pangkat/Golongan', 'Pendidikan Terakhir']
    writer.writerow(header)
    for atoz in string.ascii_uppercase:
        url = f"{BASE_URL}"
        html = s.get(f"http://dosen.unand.ac.id/web/pencarian?cari={atoz}&act=dir", timeout=TIMEOUT, headers=HEADERS).content
        soup = bs(html, 'html.parser')
        for page in extract_pagination(soup.find('ul', class_='pagination'),url)[:-1]:
            html_= s.get(page,timeout=TIMEOUT, headers=HEADERS).content
            soup_= bs(html_, 'html.parser')
            for profile_page in extract_table(soup_,page):
                html__= s.get(profile_page,timeout=TIMEOUT, headers=HEADERS).content
                soup__= bs(html__, 'html.parser')  
                row = extract_personal(soup__,profile_page)
                if row:
                    writer.writerow(row)
                    f.flush()
