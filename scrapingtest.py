#coding: UTF-8

import os, sys
from tkinter import *
from tkinter import ttk, StringVar
from tkinter import filedialog
from tkinter import messagebox
import xlrd
import pprint
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlite3

def referenceBtn_clicked():
    """
    参照ボタンクリック時処理。
    ファイルダイアログを表示し、選択されたファイルパスをinput_file_pathにセットする。
    """
    fTyp = [("", "*.xlsx")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    input_file_path.set(filepath)

def startBtn_clicked():
    """
    Startボタンクリック時処理。
    input_file_pathで指定されたExcelファイルのカテゴリ対照表を読み込み、カテゴリ毎にAmazonより
    トップランキング100のリストを取得して、ランキングリストを出力する。
    """
    pd.set_option('display.max_colwidth', 100)
    input_sheet_df = pd.read_excel(input_file_path.get(), sheet_name='カテゴリ対照表')
    data = input_sheet_df['AmazonCategoryURL']

    categoryName = data[0]
    resultHTML = requestHTML(categoryName)
    ranking_url = parseCategoryHTML(resultHTML)
    get_ranking(ranking_url,input_sheet_df.loc[0]).to_csv('AmazonTop100.csv')

def get_ranking(ranking_url_list,category_info):
    """
    ランキングページURLリストからTOP100リストを作る。

    Parameters
    ----------
    ranking_url_list : str[5]
        ランキングページURLリスト。

    Returns
    -------
    ranking_list_df : DataFrame
        ランキングTop100リスト。
    """

    print(category_info['AmazonCategoryURL'])
    # ランキング1〜100を取得
    ranking_list = []
    for i in range(5):
        ranking_list.append(parseRankingHTML(requestHTML(ranking_url_list[i]), category_info))

    ranking_list_df = pd.DataFrame(ranking_list)

    return ranking_list_df

def requestHTML(url):
    """
    サイトからHTMLソースを取得する。

    Parameters
    ----------
    url : str
        サイトのURL。

    Returns
    -------
    HTML_Source : str
        HTMLソース。
    """
    HTML_Source = requests.get(url).text
    return HTML_Source

def parseCategoryHTML(HTML_Source):
    """
    カテゴリページを解析し、ランキングページのURLを取得する。

    Parameters
    ----------
    HTML_Source : str
        カテゴリページHTMLソース。

    Returns
    -------
    ranking_pg_list : str[]
        ランキングページリスト。
    """

    soup = BeautifulSoup(HTML_Source, 'html.parser')
    parse_list = soup.find_all('li', class_="zg_page")

    ranking_pg_list = []
    for parse_item in parse_list:
        ranking_pg_list.append(parse_item.find('a').get('href'))

    return ranking_pg_list


def parseRankingHTML(HTML_Source, category_info):
    """
    ランキングページを解析し、必要な情報を取得する。

    Parameters
    ----------
    HTML_Source : str
        ランキングページHTMLソース。
    ranking_detail : str[[]]
        [ASIN,カテゴリ,URL,タイトル,価格,プライムフラグ,パントリーフラグ,あわせ買いフラグ,予備販売フラグ]リスト。
    """

    soup = BeautifulSoup(HTML_Source, 'html.parser')
    parse_list = soup.find_all('div', class_="zg_itemRow")

    ranking_detail = []

    for parse_item in parse_list:
        detail = []
        # ASIN
        asin = parse_item.find('a').get('href').split('/dp/')[1].split('/ref')[0].split('?_encoding=UTF8&psc=1')[0]
        detail.append(asin)
        # Amazonカテゴリ
        detail.append(category_info['AmazonCategory'])
        # AmazonカテゴリURL
        detail.append(category_info['AmazonCategoryURL'])
        # Yahooカテゴリ
        detail.append(category_info['YahooCategory'])
        # YahooカテゴリID
        detail.append(category_info['YahooCategoryID'])
        # 商品名
        item_name = parse_item.find('div', class_='p13n-sc-truncate p13n-sc-line-clamp-2').text.strip()
        detail.append(item_name)
        # ランキング
        rank = parse_item.find('span', class_="zg_rankNumber").text.replace('.', '').strip()
        detail.append(rank)
        # 価格
        price = parse_item.find('span', class_="p13n-sc-price").text.strip('￥').replace(',', '').strip()
        detail.append(price)
        # Prime
#        prime = parse_item.find('i', class_="a-icon").text
#        detail.append(prime)

#        link = uri + parse_item.find('a', class_="a-link-normal").get('href')
#        print(link)
#        detail.append(link)
    ranking_detail.append(detail)
    return ranking_detail

if __name__ == '__main__':

    root = Tk()
    root.title('Get Amazon List')
    root.resizable(False, False)

    frame1 = ttk.Frame(root, padding=10)
    frame1.grid()

    referenceBtn = ttk.Button(root, text=u'参照', command=referenceBtn_clicked)
    referenceBtn.grid(row=0, column=3)

    s = StringVar()
    s.set('ファイル>>')
    label = ttk.Label(frame1, textvariable=s)
    label.grid(row=0, column=0)

    input_file_path = StringVar()
    file1_entry = ttk.Entry(frame1, textvariable=input_file_path, width=50)
    file1_entry.grid(row=0, column=2)

    frame2 = ttk.Frame(root, padding=(0, 5))
    frame2.grid(row=1)

    startBtn = ttk.Button(frame2, text='Start', command=startBtn_clicked)
    startBtn.pack(side=LEFT)

    cancelBtn = ttk.Button(frame2, text='Cancel', command=quit)
    cancelBtn.pack(side=LEFT)

    root.mainloop()

