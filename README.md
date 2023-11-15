# IPocalypse now: how IPAs invaded our pints

![Beer_periodic](https://github.com/epfl-ada/ada-2023-project-dondada/assets/145542268/c3dfb479-c48e-4263-92d3-1df533ccaf0e)

## Abstract: 
We can trace back first occurences of the word IPA as far back as the $`19^{th}`$ century. However it seems that it is only in the past decades that IPAs became popular, at the point that now, one cannot sit in a bar without seeing this word on every beer tap. But how did this happen ? In this project, we will try to identify how the IPA trend spread throughout the world both from a geographical and social point of view. To do so we will analyse millions of reviews from two beer rating websites [BeerAdvocate](https://www.beeradvocate.com/) and [RateBeer](https://www.ratebeer.com/). Ultimately, we would like to understand what are the key factors necessary for a beer style to spread at a global scale, identify what beer type will replace the IPA in the heart of beer lovers and from where it will emerge.

## Research Questions:
**Important: dans toute ces question est ce qu'on va pouvoir caler des anovas, t-test et autres joyeusetés ? Peut-etre en comparant notes IPA vs notes autres bières**

Is the IPA really the most popular type of beer ?
  
Geographical point of view:
- From where and when did the trend spread ? Is there a particular country at the root of the tree ?
- Is there region of the world that have not been invaded yet ?
- Is the fanbase of the beer type located where the trend started ? 

Social point of view:
- Can we link the microbreweries & craft beer trend to the IPA trend ?
- Can a brewery succeed if it has no IPAs in its cave ? (t-test)
- Among a specific beer type, can we identify a specific beer that stands out ?

Can we identify the next hyped beer type and where it will emerge ?

## Proposed additional datasets:
If we look at raw data from beer rating datasets, we can see that the USA is from far the country which rates the most beer, however is it the country with the most ratings per capita ? To answer such questions, we will need data about the population of each country. Therefore we will use a dataset such as the [world population dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset) to bring some data to a "per capita" ratio. This dataset contains the population of 234 countries. Data are given for each decade from 1970 to 2000 and every 5 years since 2000. We may be able to enrich this dataset with population estimate on every year, as we have the estimate of the growth rate from 1970 to 2022 available for each country.

For the same reasons and because we may have a closer look at what is happening in the USA, we will need a dataset with the population of states from the USA. We will use the[	
Population Estimates and Decennial Census dataset](https://www.statsamerica.org/downloads/default.aspx). In this dataset we can find the population (count or estimate) from each states, for every decade from 1970 to 2000 and for every year since 2000. We will use the population count released by the state (if not available, we will use the estimate).

## Methods:
### Data Pre-Process
Convert text files (ratings.txt and reviews.txt) to csv.

Filter the dataset by removing rows with relevant values missing.
**Svp ajoutez les preprocess que vous avez fait**

### Exploratory analysis
Make a few plots allowing to present the dataset (e.g. different beer types available on the website, repartition of nb of ratings per country, distribution of beer type in the top100)

Analyse the language of comments with a naïve Bayesian classifier to see if it is reasonable to only keep comments in english. We will use [CLD2](https://github.com/CLD2Owners/cld2) for this purpose.

### Geographical and social analysis
Compute metrics used to determine a beer type popularity:

- The number of ratings for that type
- The average grade and the average bros_score (the bros_score being a the score given by an expert)
- The number of fans of this type of beer (We will define a fan as a user who dedicates most of his reviews to the beer type of interest and who gives a good grade most of the time (we will define the thresholds later))
- Words that are often mentionned in reviews. First we will identify words describing a "good" beer by obtaining the words that are the most represented in positive reviews of beers graded 4.0 or more. Then we will see if these words also appear often for a given type of beer, if we find a match, it may suggest that this beer type is highly appreciated !

Then manage vizualization of these metrics (both on world maps and histogramms). Do a word cloud to vizualize data obtained from comments.

One way independant ANOVA to compare grades of IPAs vs other beers

### Predicting the next beer type 
Please propose the algorithm we are gonna use and maybe with which features.
Use PCA to extract features --> Then do a K-means clustering to distinguish between trendy and not trendy beer
  
## Proposed timeline:

- W9: Submit P2 + Release of H2
- W10: Work on H2. Make the website skeleton for P3
- W11: Submit H2 (beginning of week). Pre-process data and do the exploratory analysis
- W12: Do the geographical and social analysis
- W13: Make the algorithm predicting the next type of beer
- W14: Finalize of the datastory on the website.

## Organization within the team:

| Team member  | Tasks |
| ------------- | ------------- |
| Gaspard  | Fini le projet  |
| Gaspard  | Fini le projet  |
| Gaspard  | Fini le projet  |
| Gaspard  | Fini le projet  |
| Gaspard  | Fini le projet  |


## Questions for TAs:
