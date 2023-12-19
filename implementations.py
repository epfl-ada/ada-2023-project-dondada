'Implementation of the different functions used to analyse datasets'

import numpy as np
import pandas as pd
import os 
import gzip
import csv
import pycountry as py
import pycountry_convert as pc 
import unicodedata
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer




'''========================= LOADING FUNCTIONS ========================='''

def txt_to_csv(path,name):

    '''converts a .txt file to a .csv

        args : 
            path : relative path of the .txt file
            name : name of the .txt file 

        returns : no direct output, creates a .csv file in the data folder.
    '''

    if os.path.exists(f"{path}/{name}.csv"):
        print(f"{name}.csv is already present in the folder")
        return  # Exit the function
    
    
    with gzip.open(f'{path}/{name}.txt.gz', 'rt', encoding='utf-8') as text_file:
        # Create a CSV file
        with open(f'{path}/{name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
            # CSV
            csv_writer = csv.writer(csv_file)
        
            # Dictionnary
            data = {}
            total_lines = 0
            headers_created = False

            # Each line of txt
            for line in text_file:
                line = line.strip()

                if not line: # when there is no line, then add retrieved elements to one row in the CSV
                    if data:
                        
                        if not headers_created:
                            # Create headers with keys from dictionnary
                            headers = list(data.keys())
                            csv_writer.writerow(headers)
                            headers_created = True


                        # Write the data to the CSV
                        row = [data.get(header, "") for header in headers]
                        csv_writer.writerow(row)
                        data = {}
                        total_lines += 1
                else:
                    # Check if the line contains the separator ": "
                    if ": " in line:
                        key, value = line.split(": ", 1)
                        data[key] = value
                    else:
                        pass

            # Last writing
            if data:
                row = [data.get(header, "") for header in headers]
                csv_writer.writerow(row)
                total_lines += 1

    print(f"Total number of comments : {total_lines}")
    print(f"Saved as {name}.csv in {path}")



    '''========================= FORMATING FUNCTIONS  ========================='''


def rename_country(location) :

    if 'United States' in location:
        return 'United States'
    if 'U.S' in location: 
        return 'United States'
    if 'Canada' in location:
        return 'Canada'
    if 'United Kingdom' in location:
        return 'United Kingdom'
    if 'Northern Ireland' in location: 
        return 'United Kingdom'
    if 'Wales' in location: 
        return 'United Kingdom'
    if 'Scotland' in location:
        return 'United Kingdom'
    if 'England' in location:
        return 'United Kingdom'
    if 'Reunion' in location: 
        return 'France'
    if 'Fiji' in location: 
        return 'Fiji'
    if 'Utah' in location:
        return 'United States'
    if 'Trinidad & Tobago' in location:
        return 'Trinidad and Tobago'
    if 'British' in location:
        return 'United Kingdom'
    if 'Cape Verde Islands' in location:
        return 'Cabo Verde'
    if 'Saint Vincent and The Grenadines' in location:
        return 'Saint Vincent and the Grenadines'
    if 'Antigua & Barbuda' in location: 
        return 'Antigua and Barbuda'
    if 'Dem Rep of Congo' in location: 
        return 'Democratic Republic of the Congo'
    if 'Cyprus' in location: 
        return 'Cyprus'
    if 'Northern Marianas' in location: 
        return 'United States'
    if 'Tibet' in location: 
        return 'China'
    if 'South Ossetia' in location: 
        return 'Georgia'
    if 'Transdniestra' in location: 
        return 'Republic of Moldova'
    if 'Kosovo' in location: 
        return 'Serbia'
    if 'Abkhazia' in location: 
        return 'Georgia'
    if 'East Timor' in location: 
        return 'Indonesia'
    if 'Nagorno-Karabakh' in location: 
        return 'Azerbaijan'
    else:
        return location
    

def add_iso_code(location):
    try:
        country_alpha2 = py.countries.get(name=location).alpha_2
        return f'{country_alpha2}'
    except AttributeError:
        return location


def country_to_continent(country_name):

        try:
                country_alpha2 = pc.country_name_to_country_alpha2(country_name)
                country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
                country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
                return country_continent_name
        except KeyError:
                return None


def convert_to_date(series):

    '''
    Convert Unix timestamps to 'YYYY-MM-DD' format and handle non-timestamp values.

    arg : Unix timestamps  

    returns : formatted date 

    '''

    try:
        return pd.to_datetime(series, unit='s').dt.strftime('%Y-%m-%d')
    except (TypeError, ValueError):
        return series


def categorize_style(style):

    '''

    Merge different beer styles into larger categories. To do so, the function detects specific substrings that correspond to broader beer styles. 
    Also converts the provided string to lowercase beforehand for case-insensitive matching. 

    arg : beer style, as a string 

    returns : broader beer style 

    '''

    style = style.lower()

    if any(substring in style for substring in ['bock', 'doppelbock', 'eisbock', 'maibock', 'weizenbock']):
            return 'Bocks'
    elif any(substring in style for substring in ['altbier', 'brown ale', 'irish ale', 'american brown ale', 'belgian dark ale', 'english brown ale', 'english dark mild ale']):
            return 'Brown Ales'
    elif any(substring in style for substring in ['dubbel', 'traditional ale', 'mild ale', 'landbier', 'keller', 'zwickel', 'black ale','american black ale','roggenbier', 'scottish ale', 'winter warmer']):
            return 'Dark Ales'
    elif any(substring in style for substring in ['american amber / red lager', 'amber lager/vienna', 'dunkel/tmavý', 'dortmunder', 'euro dark lager', 'czech amber lager', 'czech dark lager', 'european dark lager', 'märzen', 'munich dunkel', 'rauchbier', 'schwarzbier', 'vienna lager']):
            return 'Dark Lagers'
    elif any(substring in style for substring in ['bière de champagne / bière brut', 'california common', 'braggot', 'california common / steam beer', 'cream ale']):
            return 'Hybrid Beers'
    elif any(substring in style for substring in ['american ipa', 'india style lager', 'ipa','belgian ipa', 'black ipa', 'brut ipa', 'english ipa', '(ipa)', 'imperial ipa', 'milkshake ipa', 'new england ipa']):
            return 'India Pale Ales'
    elif any(substring in style for substring in ['american amber / red ale', 'amber ale', 'bitter', 'blond ale', 'american blonde ale', 'american pale ale', '(apa)','belgian blonde ale', 'belgian pale ale', 'bière de garde', 'english bitter', 'english pale ale', 'english pale mild ale', 'extra special / strong bitter (esb)', 'grisette', 'irish red ale', 'kölsch', 'saison']):
            return 'Pale Ales'
    elif any(substring in style for substring in ['american adjunct lager', 'czech pilsner', 'premium lager', 'pilsener', 'pale lager', 'euro strong lager','german pilsener', 'czech pilsener','american pale lager', 'euro pale lager', 'american lager', 'bohemian / czech pilsner', 'czech pale lager', 'european / dortmunder export lager', 'european pale lager', 'european strong lager', 'festbier / wiesnbier', 'german pilsner', 'helles', 'imperial pilsner', 'india pale lager (ipl)', 'kellerbier / zwickelbier', 'light lager', 'malt liquor']):
            return 'Pale Lagers'
    elif any(substring in style for substring in ['american porter', 'porter', 'baltic porter', 'english porter', 'imperial porter', 'robust porter', 'smoked porter']):
            return 'Porters'
    elif any(substring in style for substring in ['chile beer', 'mead', 'radler/shandy', 'cider', 'specialty grain', 'smoked', 'low alcohol', 'vegetable','herb', 'spice', 'herbed / spiced beer', 'pumpkin ale', 'fruit', 'fruit and field beer', 'gruit / ancient herbed ale', 'happoshu', 'herb and spice beer', 'japanese rice lager', 'kvass', 'low-alcohol beer', 'pumpkin beer', 'rye beer', 'sahti', 'smoked beer']):
            return 'Specialty Beers'
    elif any(substring in style for substring in ['american imperial stout', 'stout', 'milk / sweet stout','imperial stout', 'american stout', 'english stout', 'foreign / export stout', 'irish dry stout', 'oatmeal stout', 'russian imperial stout', 'sweet / milk stout']):
            return 'Stouts'
    elif any(substring in style for substring in ['american barleywine','barley wine', 'abt/quadrupel', 'scotch ale', 'belgian strong ale', 'belgian ale', 'belgian strong dark ale', 'american strong ale', 'belgian dark strong ale', 'belgian pale strong ale', 'english barleywine', 'english strong ale', 'imperial red ale', 'old ale', 'quadrupel (quad)', 'scotch ale / wee heavy', 'tripel', 'wheatwine']):
            return 'Strong Ales'
    elif any(substring in style for substring in ['american dark wheat beer', 'wheat ale', 'american dark wheat ale', 'american pale wheat beer', 'american pale wheat ale', 'dunkelweizen', 'grodziskie', 'hefeweizen', 'kristallweizen', 'witbier']):
            return 'Wheat Beers'
    elif any(substring in style for substring in ['berliner weisse', 'sour red/brown', 'berliner weissbier','brett beer', 'faro', 'flanders oud bruin', 'flanders red ale', 'fruit lambic', 'fruited kettle sour', 'gose', 'gueuze', 'lambic', 'wild ale']):
            return 'Wild/Sour Beers'
    else:
            return 'Other'


def aggregate_data(input_data, group_column, user_location):

    '''
    Creates a new dataframe by aggregating data based on the specified group_column.

    Args:
    - input_data: DataFrame containing the input data.
    - group_column: Column based on which the data will be grouped and aggregated.

    Returns:
    - grouped_data: DataFrame with aggregated data.

    '''
     
    # Create an empty dictionary to store aggregated values
    aggregated_data = {}

    # Iterate over unique values in the specified column
    for group_value in input_data[group_column].unique():
        # Filter rows for the current group_value
        group_data = input_data[input_data[group_column] == group_value]
        group_data = group_data.sort_values(by='date', ascending=True)

        # Initialize a dictionary for dates
        aggregated_data[group_value] = {
            'beer_id': group_data['beer_id'].iloc[0],
            'beer_name': group_data['beer_name'].iloc[0],
            'style': group_data['style'].iloc[0],
            'bigger_style': group_data['bigger_style'].iloc[0],
            'nbr_ratings': len(group_data),
            'avg': group_data['avg'].iloc[0],
            'ratings_info': {}
        }

        # Iterate over unique dates
        for date in group_data['date'].unique():
            date_data = group_data[group_data['date'] == date]
            aggregated_data[group_value]['ratings_info'][str(date)] = {
                'nbr_ratings': len(date_data),
                'avg': date_data['avg'].iloc[0],
                'locations': {}
            }

            # Iterate through each location in the current group
            for location, location_group in date_data.groupby(user_location):
                aggregated_data[group_value]['ratings_info'][str(date)]['locations'][str(location)] = {
                    'nbr_ratings': len(location_group),
                    'avg': location_group['avg'].iloc[0]
                }

    # Convert the dictionary to a DataFrame
    grouped_data = pd.DataFrame.from_dict(aggregated_data, orient='index')

    # Sort columns in ascending order
    grouped_data = grouped_data.reset_index().drop(columns='index')

    return grouped_data


def plot_normalized_ratings_by_group(data, group_column, title, total_ratings_per_year):

    unique_groups = data[group_column].unique()

    years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
            2014, 2015, 2016, 2017]

    # Initialize a DataFrame to store normalized ratings
    normalized_ratings_df = pd.DataFrame(index=years, columns=unique_groups)

    for group_value in unique_groups:
        # Extracting the years and corresponding num_ratings for each group_value
        group_data = data[data[group_column] == group_value]["ratings_info"].iloc[0]

        # Ensure the 'ratings_info' structure is as expected
        years_data = list(group_data.keys())
        years_int = [int(year) for year in years_data]

        # Initialize nbr_ratings as a list of zeros
        nbr_ratings = [0] * len(years)

        # Update nbr_ratings for years where data is available
        for i, year in enumerate(years):
            if year in years_int:
                nbr_ratings[i] = group_data[str(year)]['nbr_ratings'] / total_ratings_per_year.loc[year, 'total_nbr_ratings']

        # Assign the normalized ratings to the DataFrame
        normalized_ratings_df[group_value] = nbr_ratings

    # Plotting the data as a stacked bar plot using pandas
    plt.figure(figsize=(12, 8))
    normalized_ratings_df.plot(kind='bar', stacked=True, colormap='tab20', edgecolor='w')
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Normalized Number of Ratings')
    plt.legend(title=group_column, loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()


def get_top_words(df, text_column, custom_stop_words=None, n_top_words=10):
    """
    Count the occurrences of words in a text column of a DataFrame and return the top N words.

    Parameters:
    - df: pandas DataFrame
    - text_column: str, the column containing the text data
    - custom_stop_words: list, custom stop words to be excluded from word counts
    - n_top_words: int, the number of top words to retrieve

    Returns:
    - pd.DataFrame, a DataFrame with the top N words and their counts
    """

    # Create a CountVectorizer instance with custom stop words
    vectorizer = CountVectorizer(stop_words=custom_stop_words, lowercase=True)

    # Fit and transform the text data
    X = vectorizer.fit_transform(df[text_column])

    # Get the feature names (words)
    feature_names = vectorizer.get_feature_names_out()

    # Sum the occurrences of each word
    word_counts = X.sum(axis=0)

    # Create a DataFrame with word counts and corresponding words
    word_counts_df = pd.DataFrame({'word': feature_names, 'count': word_counts.A1})

    # Get the top N words
    top_words = word_counts_df.nlargest(n_top_words, 'count')

    return top_words

