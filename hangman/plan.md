Data: txt doc with 370,105 words (will have to consider what to train and test on)

Goal: train a model to play hangman

Evaluate strategies/models (perplexity): Random guessing vs unigram vs bigram and ect.

Currently WIP: to handle the case where we are given a partially revealed word, plan is to, use the context before each blank to predict what should fill it. For each possible letter, sum its probabilities across all blank positions, then pick the letter with the highest total.
