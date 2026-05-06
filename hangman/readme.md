## Character-Level N-gram Language Models for Hangman
 
N-gram language models trained to play Hangman, evaluated via perplexity and simulated gameplay.
A character-level trigram with linear interpolation smoothing achieves an average of 8.2 incorrect guesses per word on a 370,000-word English corpus. See [paper](https://github.com/mindphil/mml/blob/main/hangman/nlp_hangman.pdf).
 
## Usage
 
```
python game.py
```
 
Trains unigram, bigram, and trigram models, optimizes interpolation weights on held-out data, and evaluates on the test set.
 
## Requirements
 
- Python 3.10+
- NumPy, Matplotlib (for experiments notebook only)
## Structure
 
- `ngram_model.py` — corpus loading, n-gram training, interpolation, perplexity
- `game.py` — Hangman solver and evaluation
- `experiments.ipynb` — all figures and analyses from the paper
- `words_alpha.txt` — training corpus ([source](https://github.com/dwyl/english-words))