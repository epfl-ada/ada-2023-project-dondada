'Implementation of the different functions used to analyse datasets'

import numpy as np
import pandas as pd
import os 
import gzip
import csv
import pycountry_convert as pc 
import unicodedata




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


def country_to_continent(country_name):

    ''' 
    Link a country to its respective continent.

    arg : country name as a string 

    returns : country's continent as a string 
    '''
    
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    except KeyError:
        return None


def convert_to_date(value):

    '''
    Convert Unix timestamps to 'YYYY-MM-DD' format and handle non-timestamp values.

    arg : Unix timestamps  

    returns : formatted date 
    '''

    try:
        return pd.to_datetime(value, unit='s').strftime('%Y-%m-%d')
    except (TypeError, ValueError):
        return value


def categorize_style(style):

    '''
    Merge different beer styles into larger categories. To do so, the function detects specific substrings that correspond to broader beer styles. 
    Also converts the provided string to lowercase beforehand for case-insensitive matching. 

    arg : beer style, as a string 

    returns : broader beer style 

    '''

    style = style.str.lower()

    if any(substring in style for substring in ['bock', 'doppelbock', 'eisbock', 'maibock', 'weizenbock']):
        return 'Bocks'

    elif any(substring in style for substring in ['altbier', 'american brown ale', 'belgian dark ale', 'english brown ale', 'english dark mild ale']):
        return 'Brown Ales'

    elif any(substring in style for substring in ['dubbel', 'black ale','american black ale','roggenbier', 'scottish ale', 'winter warmer']):
        return 'Dark Ales'

    elif any(substring in style for substring in ['american amber / red lager', 'dortmunder', 'euro dark lager', 'czech amber lager', 'czech dark lager', 'european dark lager', 'märzen', 'munich dunkel', 'rauchbier', 'schwarzbier', 'vienna lager']):
        return 'Dark Lagers'

    elif any(substring in style for substring in ['bière de champagne / bière brut', 'braggot', 'california common / steam beer', 'cream ale']):
        return 'Hybrid Beers'

    elif any(substring in style for substring in ['american ipa', 'belgian ipa', 'black ipa', 'brut ipa', 'english ipa', '(ipa)', 'imperial ipa', 'milkshake ipa', 'new england ipa']):
        return 'India Pale Ales'

    elif any(substring in style for substring in ['american amber / red ale', 'american blonde ale', 'american pale ale', '(apa)','belgian blonde ale', 'belgian pale ale', 'bière de garde', 'english bitter', 'english pale ale', 'english pale mild ale', 'extra special / strong bitter (esb)', 'grisette', 'irish red ale', 'kölsch', 'saison']):
        return 'Pale Ales'

    elif any(substring in style for substring in ['american adjunct lager', 'euro strong lager','german pilsener', 'czech pilsener','american pale lager', 'euro pale lager', 'american lager', 'bohemian / czech pilsner', 'czech pale lager', 'european / dortmunder export lager', 'european pale lager', 'european strong lager', 'festbier / wiesnbier', 'german pilsner', 'helles', 'imperial pilsner', 'india pale lager (ipl)', 'kellerbier / zwickelbier', 'light lager', 'malt liquor']):
        return 'Pale Lagers'

    elif any(substring in style for substring in ['american porter', 'baltic porter', 'english porter', 'imperial porter', 'robust porter', 'smoked porter']):
        return 'Porters'

    elif any(substring in style for substring in ['chile beer', 'herbed / spiced beer', 'pumpkin ale', 'fruit', 'fruit and field beer', 'gruit / ancient herbed ale', 'happoshu', 'herb and spice beer', 'japanese rice lager', 'kvass', 'low-alcohol beer', 'pumpkin beer', 'rye beer', 'sahti', 'smoked beer']):
        return 'Specialty Beers'

    elif any(substring in style for substring in ['american imperial stout', 'milk / sweet stout','imperial stout', 'american stout', 'english stout', 'foreign / export stout', 'irish dry stout', 'oatmeal stout', 'russian imperial stout', 'sweet / milk stout']):
        return 'Stouts'

    elif any(substring in style for substring in ['american barleywine','belgian strong dark ale', 'american strong ale', 'belgian dark strong ale', 'belgian pale strong ale', 'english barleywine', 'english strong ale', 'imperial red ale', 'old ale', 'quadrupel (quad)', 'scotch ale / wee heavy', 'tripel', 'wheatwine']):
        return 'Strong Ales'

    elif any(substring in style for substring in ['american dark wheat beer', 'american dark wheat ale', 'american pale wheat beer', 'american pale wheat ale', 'dunkelweizen', 'grodziskie', 'hefeweizen', 'kristallweizen', 'witbier']):
        return 'Wheat Beers'

    elif any(substring in style for substring in ['berliner weisse', 'berliner weissbier','brett beer', 'faro', 'flanders oud bruin', 'flanders red ale', 'fruit lambic', 'fruited kettle sour', 'gose', 'gueuze', 'lambic', 'wild ale']):
        return 'Wild/Sour Beers'

    else:
        return 'Other'



def clean_text(text):

    '''
    To remove non UTF-8 characters from a string.
    The function removes non-printable characters but preserves newline characters \n  

    arg : string 

    returns : UFT-8 format string 
    '''
    cleaned_text = ''.join(c for c in text if unicodedata.category(c) != 'Cc' or c == '\n')
    return cleaned_text




