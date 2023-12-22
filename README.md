# Brewmageddon: How IPAs Took Over the Beeriverse

## Check out our [Brewmageddon Datastory](https://tcastal.github.io/dondada/) !

## Abstract: 
We can trace back first occurrences of the word IPA as far back as the $`19^{th}`$ century. However it seems that it is only in the past decades that IPAs became popular, at the point that now, one cannot sit in a bar without seeing this word on every beer tap. But how did this happen ? In this project, we will try to identify how the IPA trend spread throughout the world both from a geographical and social point of view. To do so we will analyse millions of reviews from two beer rating websites [BeerAdvocate](https://www.beeradvocate.com/) and [RateBeer](https://www.ratebeer.com/). Ultimately, we would like to understand what are the key factors necessary for a beer style to spread at a global scale and identify what beer style BeerAficionados will venerate next.

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

## Methods:
### Data Pre-Process
Convert text files (ratings.txt and reviews.txt) to csv.

We created bigger styles of beer according to the [BeerAdvocate style classification](https://www.beeradvocate.com/beer/styles/). As for the locations we grouped them in continents, countries and a US state column in our dataset. For the missing values of the different scores we dropped them. Finally, we eliminated the rows with location that didn’t have the right format.

When using BA and RB dataset at the same time, we used the matched_beer files to eliminate users duplicates in order to not take their reviews into account 2 times.

### Exploratory analysis
Study the number of ratings and the different styles of beer represented on both websites (e.g number of ratings per style, distribution of the number of ratings and styles of beers). 
We analysed the language of comments with a naïve Bayesian classifier, [CLD2]( https://github.com/CLD2Owners/cld2) to see if not taking into account other languages was reasonable.

### Defining Beer popularity

**Analysis of ratings means:** We sampled a given number of ratings for 6 different beer styles we noticed were important. We then perform an ANOVA test on these data to assess if any mean significantly differed from others. ANOVA results being conclusive, we used tukey's honestly significant difference (HSD) test to see which beer style had significantly different ratings mean and in which direction was the difference.

**Analysis of review's text:** We extracted words from different kind of reviews like positive reviews (grade > 4), negative reviews (grade < 1.5), IPA reviews and Stout reviews. Then we plot these words on a [WordCloud](https://amueller.github.io/word_cloud/) and extract the top 10 words appearing in each review category. With this we are able to identify characteristics of good and bad beers, IPAs and Stouts. Comparing IPAs and Stouts with good beer characteristics gives us an idea of the beer popularity. Note that we only did this for the BeerAdvocate dataset for computational purpose.

  **Chronological evolution of popular beers** We filtered the dataset in order to keep only highly appreciated beers (grade $>3^{rd}$ quartile). We then studied the share of ratings between each big beer styles for every year since 2000. This allowed us to see that some beers disappeared from the trend as they were not rated anymore, while others appeared. We also extracted the highest increase percentage from these data to identify popular types.

**Beer Fanbase:** We identified users that were "fan" of each beer styles. We defined a fan as a user who dedicated at least 75% of his ratings to a given style. Once we identified fans, we compared the number of fan for each beer styles and displayed them on a world map to get geographical insights.

  **Microbrewery revolution and IPAs:** For each year, we counted the percentage of reviews that contained keywords related to the microbrewing universe (e.g. craft, microbrewery, taproom, etc…). We did this for several categories (overall, IPA, Stouts, etc…). We displayed the results on a line plot to see if IPAs was more related to the microbrewery culture than other beers. Then to have a qualitative point of view, we performed a $\chi^2$-test between IPA reviews and overall reviews
  

 **Prediction of the next trendy beer**
In order to reduce the complexity of our dataset, we will perform a PCA to extract features with the most variance and get insights on the characteristics that make beers “trendy”. We could then perform clustering using DBSCAN in order to differentiate trendy beers from others, as DBSCANs allows detection of clusters of different sizes. Then we would segregate the styles of trendy beers. The final goal is to identify the fastest growing style of beer in the recent years among these beers.

## Timeline

- W9: Submit P2 + Release of H2
- W10: Work on H2. Make the website skeleton for P3
- W11: Submit H2 (beginning of week). Pre-process data and finish introduction
- W12: Do the geographical and social analysis
- W13: Make the algorithm predicting the next trendy beer
- W14: Finalize of the datastory on the website.

## Members contribution

| Team member  | Contribution |
| ------------- | ------------- |
| **Gaspard**  |  - Impact of microbrewery culture on beer trends <br> - Prediction of next trends|
| **Thomas**  |  - Website development <br> - Datastory <br> - Language processing |
| **Margot** |  - Geographical and chronological analysis <br> - Social Analysis <br> Datastory|
| **Thibaut**  |   - Geographical and chronological analysis <br> - Social Analysis <br> - Prediction on next trends |
| **Adrien**  | - Sentiment analysis <br> - Social analysis <br> - Datastory|
