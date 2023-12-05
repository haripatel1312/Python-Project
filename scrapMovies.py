from bs4 import BeautifulSoup
import requests,random

userAgents=[
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'
]

try:
    source = requests.get('https://en.wikipedia.org/wiki/List_of_highest-grossing_films', headers={'User-Agent': random.choice(userAgents)})
    source.raise_for_status()
    
    soup=BeautifulSoup(source.text,'html.parser')
    tbody = soup.find('tbody')
    # Iterate through rows in the table, skipping the header row.
    for row in tbody.find_all('tr')[1:]:
        # Extract data from each column in the row.
        columns = row.find_all('td')
        Title = row.find('a').text
        rank = columns[0].text.strip()
        Gross = columns[2].text.strip()
        Year = columns[3].text.strip()
        print(f"Rank: {rank}, Title: {Title}, WorldWide Gross: {Gross}, Year: {Year}")


except Exception as e:
    print(e)