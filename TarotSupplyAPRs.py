# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 18:22:10 2021

@author: keatin6
"""

# In[0]: Import necessary libraries

import pandas as pd

from bs4 import BeautifulSoup

# In[1]: Main APR scraper classes

class TarotPair:
    
    def __init__(self, zipped_data):
        self.pair_name = '/'.join(zipped_data[0])
        self.token1 = zipped_data[0][0]
        self.token1_apr = zipped_data[1][0]
        self.token2 = zipped_data[0][1]
        self.token2_apr = zipped_data[1][1]
        self.exchange = zipped_data[2]
        
    def __repr__(self):
        print_string = f"{self.pair_name}"
        "{self.token1} : {self.token1_apr}"
        "{self.token2} : {self.token2_apr}"
        return print_string

class TarotScrapper:
    
    def __init__(self):
        self.file = r"tarot.txt"

    def read_file(self, file_path):
        try:
            with open(file_path) as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("Please sepecify a valid file path!")
            return None
        lines = ''.join(lines)
        soup = BeautifulSoup(lines,'lxml')
        return soup
    
    def find_pairs(self, soup_object):
        pairs_list = []
        html_tag = 'text-xl col-span-4 text-textPrimary filter saturate-50 ' \
            'self-center justify-self-center items-center'
        pairs = soup_object.findAll('span', {'class': html_tag})
        for pair in pairs:
            pair_name = pair.get_text()
            pairs_split = pair_name.split('/')
            pairs_list.append(pairs_split)
        return pairs_list
    
    def find_supply_aprs(self, soup_object):
        supply_aprs_list = []
        apr_divs = soup_object.findAll(
            'div',{'class':'grid grid-cols-4 gap-x-4 gap-y-6 mt-5'})
        for apr_div in apr_divs:
            supply_apr_div = apr_div.findAll('div')[3]
            t1_apr = supply_apr_div.findAll('span')[0].get_text()
            t2_apr = supply_apr_div.findAll('span')[1].get_text()
            supply_aprs_list.append([t1_apr, t2_apr])
        return supply_aprs_list
    
    def find_exchanges(self, soup_object):
        exchange_list = []
        exchange_spans = soup_object.findAll(
            'span',{'class':'text-textPrimary font-medium'})
        for exchange_span in exchange_spans:
            exchange = exchange_span.get_text()
            exchange_list.append(exchange)
        return exchange_list
    
    def scrape_aprs(self, file):
        soup = self.read_file(file)
        if not soup:
            return []
        pairs = self.find_pairs(soup)
        aprs = self.find_supply_aprs(soup)
        exchanges = self.find_exchanges(soup)
        zipped = zip(pairs, aprs, exchanges)
        pair_list = [TarotPair(row) for row in zipped]
        return pair_list
    
    def scrape_and_show_results(self):
        tarot_list = self.scrape_aprs(self.file)
        if not tarot_list:
            return
        
        name_list = []
        aprs_list = []
        pair_list = []
        exch_list = []
        
        for pair in tarot_list:
            name_list.append(pair.token1)
            aprs_list.append(pair.token1_apr)
            pair_list.append(pair.pair_name)
            exch_list.append(pair.exchange)
            name_list.append(pair.token2)
            aprs_list.append(pair.token2_apr)
            pair_list.append(pair.pair_name)
            exch_list.append(pair.exchange)
            
        df = pd.DataFrame()
        df['PairName'] = pair_list
        df['TokenName'] = name_list
        df['SupplyAPR'] = aprs_list
        df['SupplyAPR'] = df['SupplyAPR'].str.rstrip('%')
        df['SupplyAPR'] = df['SupplyAPR'].str.lstrip('<')
        df['SupplyAPR'] = df['SupplyAPR'].astype(float) / 100.0
        df['Exchange'] = exch_list

        pd.set_option("display.max_rows",None)
        print(df.sort_values(by=['SupplyAPR'], ascending=False))
        return df

# In[2]: Run scraper when file is called
    
if __name__ == "__main__":
    TarotScrapper().scrape_and_show_results()


# In[2]:



