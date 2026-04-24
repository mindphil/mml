#Pick a word from the test set
#Keep guessing letters until the word is fully revealed
#Count how many wrong guesses were made

from ngram_model import load_corpus, train_test_split, process, train
import random

corpus = load_corpus('hangman/words_alpha.txt')
train_set, test_set = train_test_split(corpus)
padded = process(train_set, 2)
model = train(padded, 2)

secret_word = random.choice(test_set)
def solver(state, model, n, guessed_letters):
    padded_state = ['<s>'] * (n - 1) + state + ['</s>']
    context = []
    scores = {}
    for i in range(len(padded_state)):
        if padded_state[i] == '_':
            context = tuple(padded_state[i-n+1:i])
            if context in model: 
                probabilities = model[context]
                for letter, p in probabilities.items():
                    if letter not in guessed_letters:
                        if letter not in scores:
                            scores[letter] = 0
                        scores[letter] += p
    return max(scores, key=scores.get)
    
def play_game(secret_word, model, solver):
    n = 2 #bigram
    guessed_letters = set()
    mistakes = 0
    def current_state():
        return [
            c if c in guessed_letters else '_'
            for c in secret_word
        ]
    while '_' in current_state():
        state = current_state()
        guess = solver(state, model, n, guessed_letters)
        guessed_letters.add(guess)
        if guess not in secret_word:
            mistakes += 1
    return mistakes

def evaluate(test_set, model, solver):
    total_mistakes = 0
    for word in test_set:
        mistakes = play_game(word, model, solver)
        total_mistakes += mistakes
    avg_mistakes = total_mistakes / len(test_set)
    return avg_mistakes
#test
#print(evaluate(test_set[:10], model, solver))