'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import re

# Global constants for age groups
AGE_BINS = [10, 14, 17, 20, 23, 26, 30, 35, 100]
AGE_LABELS = ["10-14", "15-17", "18-20", "21-23", "24-26", "27-30", "31-35", "36+"]
AGE_MIDPOINTS = {"10-14": 12, "15-17": 16, "18-20": 19, "21-23": 22, 
                    "24-26": 25, "27-30": 28, "31-35": 33, "36+": 40}

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
    return olympics_df


def add_age_group(df):
    '''
        Adds age group and midpoint columns to the dataframe based on predefined bins.

        args:
            df: The dataframe containing an "Age" column
        returns:
            The dataframe with "Age Group" and "Age_Midpoint" columns
    '''
    df = df.copy()
    df = df.dropna(subset=["Age"])
    df["Age Group"] = pd.cut(df["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=False)
    df["Age_Midpoint"] = df["Age Group"].map(AGE_MIDPOINTS)
    return df


def group_by_year_and_age_group(df):
    '''
        Groups the dataframe by year and age group, and counts the number of athletes in each group.

        args:
            df: The dataframe containing "Age" and "Year" columns
        returns:
            A grouped dataframe with counts and corresponding age midpoints
    '''
    df = df.copy()
    df = df.dropna(subset=["Age"])
    df["Age Group"] = pd.cut(df["Age"], bins=AGE_BINS, labels=AGE_LABELS, right=False)
    df["Age_Midpoint"] = df["Age Group"].map(AGE_MIDPOINTS)

    grouped = df.groupby(["Year", "Age Group"]).size().reset_index(name="Count")
    grouped["Age_Midpoint"] = grouped["Age Group"].map(AGE_MIDPOINTS)

    return grouped


def compute_relative_size_column(df, mode, value_col="Count", group_col="Year"):
    '''
        Computes relative percentages if mode is set to "Relative", otherwise returns absolute counts.

        args:
            df: The dataframe with a column to be used for sizing (e.g., "Count")
            mode: Either "Absolute" or "Relative"
            value_col: The column to compute percentage from (default "Count")
            group_col: The grouping column for relative computation (default "Year")
        returns:
            The updated dataframe and the name of the column to use for bubble size
    '''
    if mode == "Relative":
        total_per_group = df.groupby(group_col)[value_col].transform("sum")
        df["Percentage"] = ((df[value_col] / total_per_group) * 100).round(2)
        return df, "Percentage"
    else:
        return df, value_col
