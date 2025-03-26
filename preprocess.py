'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import re

def convert_age(df):
   
    df['Age'] = df['Age'].astype('Int64')
    
    return df

def normalize_events(df):
    
    df['Event'] = df.apply(
        lambda row: re.sub(f'^{re.escape(row["Sport"])}\\s*', '',
                        re.sub(r'\s*metres$', 'm',
                        re.sub(r'^Athletics\s*', '', row['Event']))),
        axis=1
    )
    
    return df

def normalize_countries(olympics_df, regions_df):
    
    olympics_df['Region'] = olympics_df['NOC'].map(regions_df.set_index('NOC')['Region'])
    print(olympics_df.head(2))
    return olympics_df