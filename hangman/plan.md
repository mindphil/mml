Data: txt doc with 370,105 words (will have to consider what to train and test on)

Goal: train a model to play hangman

Evaluate strategies/models (perplexity): Random guessing vs unigram vs bigram and ect.

A secondary concern could be to use perplexity to evaluate the best 'k' for laplace add-k smoothing. But since I've gone through the trouble of implementing interpolation, the content might be technically deep enough.

Currently WIP: 
- I have introduced large model interpolation from chap. 3 ISL. I need to update game.py with the interpolation solver.
- A remark on my secondary concern: create table for k that min perplexity for each n & plot in notebook
