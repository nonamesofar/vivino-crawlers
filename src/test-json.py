import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from duckdb.duckdb import numeric_const
from pandas.core.computation.ops import REDUCTIONS

# Winte types, not all are actually used but where does the list come from?
# 1 - RED
# 2 - WHITE
# 3 - BUBBLES
# 4 - ROSE
# 5 - SWEET
# 6 - FORT
# 7 - DESSERT
# 8 - PORT
# 9 - SHERRY
# 10 - MADEIRA
# 11 - MARSALA
# 12 - OTHER
wine_types = [
    "RED", "WHITE", "BUBBLES", "ROSE", "SWEET", "FORT", "DESSERT",
    "PORT", "SHERRY", "MADEIRA", "MARSALA", "OTHER"
]

def get_wine_pages(page):
    r = requests.get(
        "https://www.vivino.com/api/explore/explore",
        params={
            "country_code": "FR",
    #        "country_codes[]": "fr",
            "currency_code": "EUR",
            "min_rating": "1",
            "order_by": "price",
            "order": "asc",
            "page": {page},
            # "price_range_max": "3000",
            # "price_range_min": "1",
            # "wine_type_ids[]": "7",
        },
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
        },
        verify=False
    )
    with open('raw/response-'+f'{page}'+'.json', 'w') as f:
        json.dump(r.json(), f, indent=4)

    results = [
        (
            t["vintage"]["name"],
            wine_types[t["vintage"]["wine"]["type_id"] - 1],
            t["vintage"]["wine"]["name"],
            t["vintage"]["wine"]["region"]["name"],
            t["vintage"]["wine"]["region"]["country"]["name"],
            t["vintage"]["wine"]["winery"]["name"],
            t['vintage']['wine']['style'].get('regional_name', None) if t['vintage']['wine'].get('style') else None,
            t['vintage']['wine']['style'].get('varietal_name', None) if t['vintage']['wine'].get('style') else None,
            t["vintage"]["year"],
            t["vintage"]["statistics"]["ratings_average"],
            t["price"]["amount"],
            t["price"]["currency"]["code"],
            t["price"]["bottle_type"]["name"]
        )
        for t in r.json()["explore_vintage"]["matches"]
    ]

    return results

def get_wine_results():
    r = requests.get(
        "https://www.vivino.com/api/explore/explore",
        params={
            "country_code": "FR",
            "currency_code": "EUR",
            "min_rating": "1",
            "order_by": "price",
            "order": "asc",
            "page": 1,
#             "price_range_max": "3000",
#             "price_range_min": "1",
#             "wine_type_ids[]": "1",
        },
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
        },
        verify=False
    )

    return r.json().get('explore_vintage').get('records_matched')

def perform_eda():
    # Basic Information
    print("Basic Information:")
    print(dataframe.info())

    # Summary Statistics
    print("\nSummary Statistics:")
    print(dataframe.describe())

    # Check for Missing Values
    print("\nMissing Values:")
    print(dataframe.isnull().sum())

    # Data Distribution
    numerical_columns = ['Year', 'Rating', 'Price']
    for column in numerical_columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(dataframe[column], kde=True)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

    # Correlation Matrix
    # plt.figure(figsize=(10, 6))
    # correlation_matrix = dataframe.corr()
    # sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    # plt.title('Correlation Matrix')
    # plt.show()

# Print the explore_vintage field
number_records = get_wine_results()
number_pages = int(number_records / 25) + 1

print("Number records: "+ f'{number_records}')
print("Number pages: "+ f'{number_pages}')

dataframe = pd.DataFrame()
# Iterate from 1 to number_pages and call get_wine_pages
#for page in range(1, number_pages + 1):
for page in range(1,2):
    wine_data = get_wine_pages(page)
    df = pd.DataFrame(wine_data, columns=[
#        'Winery', 'Wine', 'Year', 'Country', 'Region', 'Rating', 'Price'
        'Name', 'Type', 'Wine', 'Region', 'Country', 'Winery', 'Regional Name', 'Varietal Name', 'Year', 'Rating', 'Price', 'Currency', 'Bottle Type'
    ])
    dataframe =pd.concat([dataframe, df], ignore_index=True)

dataframe.to_csv("raw_data.csv", index=False)

#perform_eda()



