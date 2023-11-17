# Brewmageddon: How IPAs Took Over the Beeriverse

## Abstract: 
We can trace back first occurrences of the word IPA as far back as the $`19^{th}`$ century. However it seems that it is only in the past decades that IPAs became popular, at the point that now, one cannot sit in a bar without seeing this word on every beer tap. But how did this happen ? In this project, we will try to identify how the IPA trend spread throughout the world both from a geographical and social point of view. To do so we will analyse millions of reviews from two beer rating websites [BeerAdvocate](https://www.beeradvocate.com/) and [RateBeer](https://www.ratebeer.com/). Ultimately, we would like to understand what are the key factors necessary for a beer style to spread at a global scale and identify what beer type will replace the IPA in the heart of beer lovers and from where it will emerge.

## Research Questions:

Is IPA really the most popular type of beer or are there other beers that follow a trend ?

GEOGRAPHICAL POINT OF VIEW
- From where and when did the trend spread, is there a particular country or region at the root of the tree ?
- How is the trend spreading across the world, is there a specific pattern ?
- Can we link the microbreweries and craft beer trend to the IPA trend ?

SOCIAL POINT OF VIEW
- Is there a fanbase of IPAs and where would it be located ?
- Does a successful brewery produces trendy beers like IPAs ?

Can we predict the next trendy beer and where it will emerge ?

## Proposed additional datasets:
If we look at raw data from beer rating datasets, we can see that the USA is from far the country which rates the most beer, however is it the country with the most ratings per capita ? To answer such questions, we will need data about the population of each country. Therefore we will use a dataset such as the [world population dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset). This dataset contains the population of 234 countries. Data are given for each decade from 1970 to 2000 and every 5 years since 2000.

For the same reasons and because we may have a closer look at what is happening in the USA, we will need a dataset with the population of states from the USA. We will use the [Population Estimates and Decennial Census dataset](https://www.statsamerica.org/downloads/default.aspx). In this dataset we can find the population (count or estimate) from each states, for every decade from 1970 to 2000 and for every year since 2000.

## Methods:
### Data Pre-Process
Convert text files (ratings.txt and reviews.txt) to csv.

We didn’t keep the matched beer data files since it eliminated too much information. We created bigger styles of beer according to the [BeerAdvocate style classification](https://www.beeradvocate.com/beer/styles/). As for the locations we grouped them in continents, countries and a US state column in our dataset. For the missing values of the different scores we dropped them. Finally, we eliminated the rows with location that didn’t have the right format.

### Exploratory analysis
Study the number of ratings and the different styles of beer represented on both websites (e.g number of ratings per style, distribution of the number of ratings and styles of beers). Have a look at the different scores and their distribution.

Analyse the language of comments with a naïve Bayesian classifier to see if it is reasonable to only keep comments in english. We will use CLD2 for this purpose.

### Metrics to determine a beer type popularity (or review positivity)

- The nbr_ratings for that type
- The bros_score for that type (a score given by an expert)
- Beers and reviews that have a score (range 0-100) > to the 3rd quartile
- Beers and reviews that have an average grade (range 0-5) > to the 3rd quartile
- The number of fans of this type of beer. We will define a fan as a user who dedicates most of his reviews to the beer type of interest and who gives a good grade most of the time (we will define the thresholds later).
- Words associated with good reviews. First we will identify words describing a “good” beer by obtaining the words that are the most represented in positive reviews of great beers. Then we will see if these words also appear often for a given type of beer, if we find a match, it may suggest that this beer type is highly appreciated !

### Tests:

- **One way independent ANOVA:** to compare the average grade of IPA’s compared to other styles of beer.
- **Pearson coefficient:** to analyse a potential correlation between microbrewery emergence and IPA’s popularity.

### Predicting the next beer type 

In order to reduce the complexity of our dataset, we will perform a PCA to extract features with the most variance and get insights on the characteristics that make beers “trendy”. We could then perform clustering using DBSCAN in order to differenciate trendy beers from others, as DBSCANs allows detection of clusters of different sizes. Then we would segregate the styles of trendy beers. The final goal is to identify the fastest growing style of beer in the recent years among these beers.

## Proposed timeline:

- W9: Submit P2 + Release of H2
- W10: Work on H2. Make the website skeleton for P3
- W11: Submit H2 (beginning of week). Pre-process data and do the exploratory analysis
- W12: Do the geographical and social analysis
- W13: Make the algorithm predicting the next trendy beer
- W14: Finalize of the datastory on the website.

## Organization within the team:

| Team member  | Tasks |
| ------------- | ------------- |
| Gaspard  | Predicting trend  |
| Thomas  | Website building and NLP  |
| Margot  | Data story and geographical analysis  |
| Thibaut  | Data story and social analysis  |
| Adrien  | Website building & data visualization  |

## Questions for TAs:
