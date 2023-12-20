'Implementation of the different functions used to analyse datasets'

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import gzip
import unicodedata
import re
import csv
import os 
import io
#import pycld2 as cld2
import pycountry as py 
import pycountry_convert as pc 
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from shapely.wkt import loads
from PIL import Image
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
    """
    Plot normalized ratings by group using Plotly Express.

    Parameters:
    - data: pandas DataFrame, the input data
    - group_column: str, the column containing group information
    - title: str, the title of the plot
    - total_ratings_per_year: pandas DataFrame, total ratings per year

    Returns:
    None
    """
    unique_groups = data[group_column].unique()

    years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
             2014, 2015, 2016, 2017]

    # Initialize a DataFrame to store normalized ratings
    normalized_ratings_df = pd.DataFrame(index=years, columns=unique_groups)

    for group_value in unique_groups:
        # Extracting the years and corresponding num_ratings for each group_value
        group_data = data[data[group_column] == group_value]["ratings_info"].iloc[0]
        years_data = list(group_data.keys())
        years_int = [int(year) for year in years_data]

        nbr_ratings = [0] * len(years)

        # Update nbr_ratings for years where data is available
        for i, year in enumerate(years):
            if year in years_int:
                nbr_ratings[i] = group_data[str(year)]['nbr_ratings'] / total_ratings_per_year.loc[year, 'total_nbr_ratings']

        normalized_ratings_df[group_value] = nbr_ratings

    # Create a long-format DataFrame for Plotly Express
    normalized_ratings_long = normalized_ratings_df.reset_index().melt(id_vars='index', var_name=group_column, value_name='Normalized Ratings')
    custom_colors = [
        '#FF8C00', '#995E19', '#DEB887', '#A52A2A', '#FF0000',
        '#FFC831', '#F2D6B5', '#060401', '#FFFFFF', '#FD8E8C',
        '#9F0B02', '#FAFE7D', '#1DFC07'  # Add three more custom colors
    ]
    
    # Plotting the data as a stacked bar plot using Plotly Express with a qualitative colormap
    fig = px.bar(normalized_ratings_long, x='index', y='Normalized Ratings', color=group_column, barmode='stack',
                 color_discrete_sequence=custom_colors,
                 labels={'index': 'Year', 'Normalized Ratings': 'Normalized Number of Ratings'},
                 title=title)

    fig.update_layout(barmode='stack', legend_title_text=group_column, xaxis_title='Year', yaxis_title='Normalized Number of Ratings')
    fig.show()

    return fig


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

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def add_iso_code3(location):
    try:
        country_alpha3 = py.countries.get(name=location).alpha_3
        return f'{country_alpha3}'
    except AttributeError:
        return location


def plot_increase_ratings(grouped_data):
    # Calculate the sum of ratings for each style
    style_ratings_sum = grouped_data.groupby("bigger_style")["nbr_ratings"].sum()

    # Select the top 5 styles with the highest number of ratings
    top_styles = style_ratings_sum.nlargest(5).index
    top_styles = sorted(top_styles)

    # Create an empty figure
    fig = go.Figure()

    mean_increase_list_per_year = []
    mean_increase_y1_yf_list = []

    for style in top_styles:
        # Extract information for the current style
        style_data = grouped_data[grouped_data["bigger_style"] == style]["ratings_info"].iloc[0]
        years = list(style_data.keys())
        years_int = [int(year) for year in years]
        nbr_ratings = [style_data[year]['nbr_ratings'] for year in years]

        # Calculate the mean increase between the first and last year
        mean_increase_y1_yf = (nbr_ratings[-1] - nbr_ratings[0]) / (len(nbr_ratings))
        mean_increase_y1_yf_list.append(mean_increase_y1_yf)

        # Calculate the mean increase per year
        mean_increase_per_year = sum([(nbr_ratings[i] - nbr_ratings[i - 1]) / nbr_ratings[i - 1]
                                       for i in range(1, len(nbr_ratings))]) / (len(nbr_ratings) - 1)
        mean_increase_list_per_year.append(mean_increase_per_year)

        # Add a trace for the current style
        fig.add_trace(go.Scatter(x=years_int, y=nbr_ratings, name=style, mode='lines'))

    # Update layout details
    fig.update_layout(
        title='Number of Ratings per Year for Top 5 Styles',
        xaxis_title='Years',
        yaxis_title='Number of Ratings (log scale)',
        yaxis_type='log',
        legend_title_text='Style',
        xaxis=dict(tickmode='array', tickvals=years_int),
        showlegend=True
    )

    fig.update_yaxes(tickvals=[1, 10, 100, 1000, 10000, 100000],
                 ticktext=['1', '10', '100', '1k', '10k', '100k'])

    # Print mean increase for each style per year
    print(f"Mean Increase for each style per year:")
    for style, increase in zip(top_styles, mean_increase_list_per_year):
        print(f"Mean Increase for {style}: {increase:.2%}")

    print("\n------------------------------------------------------")

    # Print mean increase for each style between the first year and last year
    print(f"\nMean Increase for each style between first year and last year:")
    for style, increase in zip(top_styles, mean_increase_y1_yf_list):
        print(f"Mean Increase for {style}: {increase:.2%}")

    # Show the plot
    fig.show()

    return fig

def ratings_per_country(data, style, location_column, ratings_info_column, country_rename_function, add_iso_code_function, continent_function):
    # Only select the data for the specified style
    style_data = data.query(f'bigger_style == "{style}"')

    # Flatten the nested 'locations' data
    flattened_locations = []

    for beer_data in style_data[ratings_info_column]:
        years = list(beer_data.keys())[:-1]

        for year in years:
            locations_data = beer_data[year]['locations']

            for location, location_info in locations_data.items():
                nbr_ratings = int(location_info['nbr_ratings'])

                flattened_locations.append({
                    'year': int(year),
                    'location': location,
                    'country': location,
                    'nbr_ratings': nbr_ratings
                })

    # Convert the flattened data to a DataFrame
    df_locations = pd.DataFrame(flattened_locations)

    # Rename the countries that don't have the right format to be converted into ISO 3166 norm
    df_locations['country'] = df_locations['country'].apply(country_rename_function)
    df_locations = df_locations.groupby(['year', 'country']).agg({'nbr_ratings': 'sum'}).reset_index()
    df_locations['log_nbr_ratings'] = np.log1p(df_locations['nbr_ratings'])

    # New column of ISO 3166 norm
    df_locations['location_with_iso'] = df_locations['country'].apply(add_iso_code_function)

    # New column continent
    df_locations['continent'] = df_locations['country'].apply(continent_function)

    return df_locations


def ratings_per_locations(data, style_column, ratings_info_column, country_rename_function, add_iso_code_function, continent_function, style):
    # Only select the data for the specified style
    style_data = data.query(f'{style_column} == "{style}"')

    # Flatten the nested 'locations' data
    flattened_locations = []

    for beer_data in style_data[ratings_info_column]:
        years = list(beer_data.keys())

        for year in years:
            locations_data = beer_data[year]['locations']

            for location, location_info in locations_data.items():
                nbr_ratings = int(location_info['nbr_ratings'])

                flattened_locations.append({
                    'year': int(year),
                    'location': location,
                    'country': location,
                    'nbr_ratings': nbr_ratings
                })

    # Convert the flattened data to a DataFrame
    df_locations = pd.DataFrame(flattened_locations)

    # Rename the countries that don't have the right format to be converted into ISO 3166 norm
    df_locations['country'] = df_locations['country'].apply(country_rename_function)
    df_locations = df_locations.groupby(['year', 'location', 'country']).agg({'nbr_ratings': 'sum'}).reset_index()

    # New column ISO 3166 norm
    df_locations['location_with_iso'] = df_locations['country'].apply(add_iso_code_function)

    # New column continent
    df_locations['continent'] = df_locations['country'].apply(continent_function)

    return df_locations


def ratings_per_US_states(data, us_states, style_column, style, year_column, location_column, nbr_ratings_column):
    fig = go.Figure()
    
    # Extract states data
    states_data = data[location_column].str.split(', ', expand=True)
    df_states = data.copy()
    df_states['NAME'] = states_data[1]
    
    # Merge with US states data
    merged_states = pd.merge(us_states, df_states, on='NAME')
    
    # Animation settings
    limits = [(0, 99), (100, 399), (400, 999), (1000, 2000), (2001, 6000)]
    colors = ["black", "orange", "crimson", "forestgreen", "royalblue"]
    scale = 20
    
    # Get unique years
    years = sorted(merged_states[year_column].unique())[:-1]
    
    frames = []
    
    # Iterate through each year
    for year in years:
        df_year = merged_states[merged_states[year_column] == year]
        frame_data = []
        
        # Iterate through each rating limit
        for i in range(len(limits)):
            lim = limits[i]
            df_sub = merged_states[(merged_states[year_column] == year) & 
                                   (merged_states[nbr_ratings_column].between(lim[0], lim[1]))]
            
            frame_data.append(go.Scattergeo(
                locationmode='USA-states',
                lon=df_sub['longitude'],
                lat=df_sub['latitude'],
                marker=dict(
                    size=df_sub[nbr_ratings_column] / scale,
                    color=colors[i],
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode='area'
                ),
                name='{0} - {1}'.format(lim[0], lim[1]),
                text=df_sub[nbr_ratings_column].astype(str) + ' - ' + df_sub['NAME'],
            ))
        
        frames.append(go.Frame(data=frame_data, name=str(year)))
    
    # Create scatter plots for the initial year
    initial_year = years[0]
    df_initial_year = merged_states[merged_states[year_column] == initial_year]
    
    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df_initial_year[df_initial_year[nbr_ratings_column].between(lim[0], lim[1])]
    
        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=df_sub['longitude'],
            lat=df_sub['latitude'],
            marker=dict(
                size=df_sub[nbr_ratings_column] / scale,
                color=colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode='area'
            ),
            name='{0} - {1}'.format(lim[0], lim[1]),
            text=df_sub['NAME'] + ': ' + df_sub[nbr_ratings_column].astype(str),  # Display city name and ratings
        ))
    
    # Update layout for animation and dropdown menu
    fig.update_layout(
        title_text=f'US City Number of Ratings for {style} by State',
        showlegend=True,
        geo=dict(
            scope='usa',
            landcolor='rgb(217, 217, 217)',
        ),
        sliders=[{
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'visible': True,
                'prefix': 'Year:',
                'suffix': '',
            },
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': [{
                'args': [
                    [str(year)],
                    {
                        'frame': {'duration': 500, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 300}
                    },
                ],
                'label': str(year),
                'method': 'animate',
            } for year in years],
        }],
        updatemenus=[{
            'buttons': [{
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate',
            }, {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate',
            }],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top',
        }],
    )
    
    # Add frames to the figure
    fig.frames = frames
    
    return fig


def review_keyword_percentage(df, key_words):
    """
    Calculate the percentage of reviews containing key words for each year.

    Parameters:
    - df: DataFrame containing 'text' and 'date' columns.
    - key_words: List of key words to search for in the reviews.

    Returns:
    - result_df: DataFrame with yearly counts and percentages.
    """
    # Convert the 'date' column to datetime format

    # Initialize a dictionary to store counts for each year
    yearly_counts = {}

    # Iterate through each year
    for year in df['date'].unique():
        # Filter the DataFrame for the current year
        year_df = df[df['date'] == year]

        # Count the number of reviews containing key words
        total_reviews = len(year_df)
        reviews_with_keywords = year_df['text'].str.contains('|'.join(key_words), case=False).sum()

        # Calculate the percentage
        percentage_with_keywords = (reviews_with_keywords / total_reviews) * 100 if total_reviews > 0 else 0

        # Store the result in the dictionary
        yearly_counts[year] = {
            'total_reviews': total_reviews,
            'reviews_with_keywords': reviews_with_keywords,
            'percentage_with_keywords': percentage_with_keywords
        }

    # Create a new DataFrame from the dictionary
    result_df = pd.DataFrame.from_dict(yearly_counts, orient='index')

    return result_df