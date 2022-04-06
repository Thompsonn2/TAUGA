# TAUGA


### Aim
To examine past price points of financial data using technical analysis to predict the direction of future stock prices. Finding a an effective trading pattern is done through finding the best possible strategy through the analysis of a genetic algorithm. 

## Functionality
A trading system based on technical analysis and genetic algorithms to find trading patterns. An initial population of 75 individuals all containing different genes are backtested against a previous dataset from 2007 to 2020. The return from this dataset is then used to act as its fitness. The more fit the individual the better change they are selected to reproduce. Sixteen random individuals are chosen, resulting in the two most fit individuals to win. Their offspring is then adde back into the population, with the least fit individuals being removed, or dying off. This process is repeated 75 generations until the most fit individual is selected. 10 different populations were generated and each finding the most fit individual offering the highest return, indicating the best strategy. The best individuals from each population is return in a list with the fitness value and chromosome values.

The chromosomes are filled with genes that indicate buy and sell thresolds, and RSI lengths to use for the analysis. Each individual has two sets of four genes, with the first four being responsible for trading on a downtrend and the second four indicating when trades should be made in an uptrend period. Trend periods are indicated by moving average crossovers.  

## Setup Instructions
```
pip install copy
pip install random
pip install pandas_datareader
pip install datetime
```

## Running Instructions
```
python3 IndividualAnalysis.py
```
Changing the stock ticker in the company list allows for different companies to be analyzed. Each company included in the list is ran through 75 generations ten seperate times. 
