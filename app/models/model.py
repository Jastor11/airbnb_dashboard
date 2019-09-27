import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class AirbnbData(object):
    def __init__(self):
        absolute_path = './app/data/AB_NYC_2019.csv'
        df = pd.read_csv(absolute_path)
        na_map = {
            'reviews_per_month': 0,
            'last_review': 'None',
            'name': 'No name',
            'host_name': 'No host name'
        }
        df.fillna(na_map, inplace=True)        
        self.df = df
        
    def percentiles_per_borough(self):
        boroughs = ['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
        borough_prices = dict({})
        for b in boroughs:
          borough_prices[b] = self.df[ self.df['neighbourhood_group'] == b ]['price']
        percs = { 
            col: borough_prices[col].describe(percentiles=[.25, .50, .75, .90, .95]) 
            for col in boroughs 
        }
        percs_per_borough = pd.DataFrame(percs).iloc[4:-1].T
        return percs_per_borough
        
    def popular_first_names(self):
        top_ten = self.df['host_name'].value_counts()[:10]
        names, count = top_ten.index, top_ten.values
        avg_reviews = [ self.df[ self.df['host_name'] == name ]['number_of_reviews'].mean() for name in names ]
        data = { name: { '# Listings': count[i], 'Avg. # Reviews': avg_reviews[i] } for i, name in enumerate(names) }        
        return pd.DataFrame(data).T
        
    def price_range_hist(self):
        img = BytesIO()
        df_price_range = self.df[ (self.df['price'] >= 500) & (self.df['price'] <= 1000) ]
        plt.hist(df_price_range['price'], bins=30, normed=False, color='dodgerblue')
        plt.xlabel('Price')
        # plt.ylabel('Frequency')
        plt.ylabel('Count')
        plt.title('Price Distribution for Listings in the \$500-\$1000 Range')
        plt.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode()
        
    def get_map_data(self, neighbourhood='Williamsburg'):
        mask = self.df['neighbourhood'] == neighbourhood
        return self.df[ mask ].sort_values(by=['number_of_reviews'], ascending=False)[:20]
        
    def get_neighbourhood_options(self):
        options = self.df['neighbourhood'].unique()
        options.sort()
        return options
        
     

        