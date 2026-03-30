#funct takes a partially revealed word like _ e l _ and trained model
#for each blank position, gets the context and looks up the probability distribution
#for each candidate letter (a-z), sums its probability across all blank positions
#returns the letter with the highest total