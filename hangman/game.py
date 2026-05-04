#Pick a word from the test set
#Keep guessing letters until the word is fully revealed
#Count how many wrong guesses were made

from ngram_model import load_corpus, train_test_split, process, train, interpolate_prob, optimize_lambdas

def solver(state, models, lambdas, guessed_letters, n_max=3):
    padded_state = ['<s>'] * (n_max - 1) + state + ['</s>']
    scores = {}
    candidates = [c for c in 'abcdefghijklmnopqrstuvwxyz' if c not in guessed_letters]
    for i in range(len(padded_state)):
        if padded_state[i] == '_':
            context = tuple(padded_state[i-n_max+1:i])
            for letter in candidates:
                p = interpolate_prob(letter, context, models, lambdas)
                if letter not in scores:
                    scores[letter] = 0
                scores[letter] += p
    return max(scores, key=scores.get)
    
def play_game(secret_word, models, solver, lambdas):
    guessed_letters = set()
    mistakes = 0
    def current_state():
        return [
            c if c in guessed_letters else '_'
            for c in secret_word
        ]
    while '_' in current_state():
        state = current_state()
        guess = solver(state, models, lambdas, guessed_letters, n_max=3)
        guessed_letters.add(guess)
        if guess not in secret_word:
            mistakes += 1
    return mistakes

def evaluate(test_set, models, solver, lambdas):
    total_mistakes = 0
    for word in test_set:
        mistakes = play_game(word, models, solver, lambdas)
        total_mistakes += mistakes
    avg_mistakes = total_mistakes / len(test_set)
    return avg_mistakes


#game
if __name__ == '__main__':
    corpus = load_corpus('words_alpha.txt')
    train_set, test_set = train_test_split(corpus, 0.95)
    train_set, held_out = train_test_split(train_set, 0.9)

    models = {}
    for n in range(1, 4):
        padded = process(train_set, n)
        models[n] = train(padded, n)

    lambdas = optimize_lambdas(held_out, models, step=0.1)

    uni_avg = evaluate(test_set[:10], models, solver, {1: 1.0, 2: 0.0, 3: 0.0})
    bi_avg = evaluate(test_set[:10], models, solver, {1: 0.0, 2: 1.0, 3: 0.0})
    tri_avg = evaluate(test_set[:10], models, solver, {1: 0.0, 2: 0.0, 3: 1.0})
    int_avg = evaluate(test_set[:10], models, solver, lambdas)

    print(f"Unigram: {uni_avg}")
    print(f"Bigram: {bi_avg}")
    print(f"Trigram: {tri_avg}")
    print(f"Interpolated: {int_avg}")
    print(lambdas)