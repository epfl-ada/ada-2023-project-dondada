# Brewmageddon: How IPAs Took Over the Beeriverse

## Check out our [Brewmageddon Datastory](https://tcastal.github.io/dondada/) !

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
Study the number of ratings and the different styles of beer represented on both websites (e.g number of ratings per style, distribution of the number of ratings and styles of beers). 
Analyse the language of comments with a naïve Bayesian classifier to see if it is reasonable to only keep comments in english. We will use CLD2 for this purpose.

### Defining Beer popularity

- The nbr_ratings for that type
- The bros_score for that type (a score given by an expert)
- Beers and reviews that have a score (range 0-100) > to the 3rd quartile
- Beers and reviews that have an average grade (range 0-5) > to the 3rd quartile

  **Microbrewery revolution and IPAs:** For each year, we counted the number of reviews where a word related to microbreweries (such as microbrewery, craft, brewpub, local) appeared. We then compare it with the number of IPA reviews for each year. Finally we measure the correlation between these two curves.
  
  **Beer Fanbase:** We identified users that were "fan" of each beer styles. We defined a fan as a user who dedicated at least 75% of his ratings to a given style. Once we identified fans, we compared the number of fan for each beer styles and displayed them on a world map to get geographical insights.
  
  **Analysis of review's text:** We extracted words from different kind of reviews like positive reviews (grade > 3rd quartile), negative reviews (grade < 1st quartile), IPA reviews and Stout reviews. Then we plot these words on a [wordcloud](https://amueller.github.io/word_cloud/) and extract the top 10 words appearing in each review category. With this we are able to identify characteristics of good and bad beers, IPAs and Stouts. Comparing IPAs and Stouts with good beer characteristics gives us an idea of the beer popularity.

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

## Members contribution

| Team member  | Tasks |
| ------------- | ------------- |
| Gaspard  |   |
| Thomas  |   |
| Margot  |   |
| Thibaut  |   |
| Adrien  | Datastory, Wordclouds, Fanbase, Microbreweries  |

## Questions for TAs:
