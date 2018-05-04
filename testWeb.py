from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
url = 'https://www.ucop.edu/operating-budget/budgets-and-reports/legislative-reports/2017-18-legislative-session.html'
result = requests.get(url)
c = result.content
soup = BeautifulSoup(c,'lxml')
summary = soup.find('div', {'class':'list-land', 'id':'content'})
tables = summary.find_all('table')
data = []
rows = tables[0].find_all('tr')
for tr in rows:
    cols = tr.find_all('td')
    for td in cols:
        text = td.find(text=True)
        data.append(text)
reports = []
date = []
index = 0

for item in data:
    if not item:
        pass
    elif 'pdf' in item:
        date.append(data[index-1])
        reports.append(item.replace('\xa0',' '))
    index += 1
date = Series(date)
reports = Series(reports)
web_df = pd.concat([date,reports],axis=1)
web_df.columns = ['Date','Reports']
print(web_df)