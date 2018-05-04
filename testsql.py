import sqlite3
import pandas as pd
con = sqlite3.connect("sakila.db")

def sql_to_df(sql_query):
    df = pd.read_sql(sql_query, con)
    return df

query = '''select first_name, last_name
            from customer'''
sql_to_df(query)

