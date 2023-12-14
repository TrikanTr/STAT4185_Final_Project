# STAT4185_Final_Project
Final Project for STAT 4185, Pokemon Usage Statistics

The goal of this program is to determine is a Pokemon's base stats, such as Attack or Speed, significantly influence the amount of team they are used on.

This data was taken from a site that hosts various statictics on pokemon and their usages in various Pokemon formats. The specific format the data was taken from is the Scarlet/Violet Singles OverUsed format, the most common singles format. the data was scraped on 12/13/2023 for the most recent data on the site.

After the preprocessing was taken care of, the two models used to determine effectiveness of the base stats on usage were a multiple linear regression model of the stats against the usage percentage in the format tier;
Secondly, a random forest model, where the binary value is based on if the Pokemon has greater than a 0.2% usage among the dataset.

The F1 score for the forest model was deemed to be very low, and the r-squared value, while better than the F1 score, was not completely satisfactory. This may be due to a number of factors. The data was only using the top 200 usages of the avialable 498 on the website, which may have skewed the predictions in one way or another. Additionally, it may be that the unused and unscraped factors such as other used items, common moves, and the unused typing of the pokemon(it was deemed too intensive to try creating dummy variables for both primary and secondary typing, as it would have resulted in 37 dummy variables). A larger dataset may be necessary as well as a more thorough dataset to find the strongest correlation between an attribute and usage