import math
import random

def load_corpus(filepath): 
    return [line.strip() for line in open(filepath)]
#test
#corpus = load_corpus('words_alpha.txt')
#print(corpus[:5])

def train_test_split(corpus, train_ratio=0.95, seed=42):
    random.seed(seed)
    corpus = corpus.copy()
    random.shuffle(corpus)

    split = int(len(corpus) * train_ratio)
    return corpus[:split], corpus[split:]

def process(corpus, n):
    tokens = [list(word) for word in corpus]
    padded_tokens = [
        ['<s>'] * (n - 1) + word + ['</s>'] 
        for word in tokens
    ]
    return padded_tokens
#test
#print(process(['hello'], 4))

def ngram(padded_tokens, n):
    result = []
    for i in range(0, len(padded_tokens)-n+1):
        result.append(tuple(padded_tokens[i:i+n]))
    return result
#test = process(['hello'], 4)
#print(ngram(test[0], 4))

def train(padded_tokens, n):
    model = {}
    for word in padded_tokens:
        letter_ngrams = ngram(word, n)
        for gram in letter_ngrams:
            context = tuple(gram[:-1])
            target = gram[-1]
            if context not in model:
                model[context] = {}
            if target not in model[context]:
                model[context][target] = 0
            model[context][target] += 1

    vocab = set() 
    for word in padded_tokens:
        for char in word:
            vocab.add(char)
    vocab.discard('<s>')

    for context in model:
        for char in vocab:
            if char not in model[context]:
                model[context][char] = 0

    for context, targets in model.items():
        total_count = float(sum(targets.values()))
        for target in targets:
            targets[target] = targets[target] / total_count
    return model

def interpolate_prob(target, context, models, lambdas):
    prob = 0
    for n in range(1, 4):
        if n == 1:
            ctx = ()
        else:
            ctx = context[-(n-1):]
        if ctx in models[n] and target in models[n][ctx]:
            p = models[n][ctx][target]
        else:
            p = 0
        prob += lambdas[n] * p
    return prob

def perplexity(test_set, models, lambdas, n_max=3):
    padded = process(test_set, n_max)
    total_log_prob = 0
    total_chars = 0
    for word in padded:
        grams = ngram(word, n_max)
        for gram in grams:
            context = tuple(gram[:-1])
            target = gram[-1]
            prob = interpolate_prob(target, context, models, lambdas)
            if prob == 0:
                prob = 1e-10
            total_log_prob += math.log2(prob)
            total_chars += 1
    pp = 2 ** (-(1/total_chars) * total_log_prob)
    return pp

def optimize_lambdas(held_out, models, step=0.1):
    best_pp = float('inf')
    best_lambdas = None
    steps = [i * step for i in range(int(1.0 / step) + 1)]
    for l3 in steps:
        for l2 in steps:
            l1 = 1.0 - l3 - l2
            if l1 < 0:
                continue
            lambdas = {1: l1, 2: l2, 3: l3}
            pp = perplexity(held_out, models, lambdas, n_max=3)
            if pp < best_pp:
                best_pp = pp
                best_lambdas = lambdas
    return best_lambdas
#test
#corpus = load_corpus('words_alpha.txt')
#train_set, test_set = train_test_split(corpus, 0.95)
#train_set, held_out = train_test_split(train_set, 0.9)

#models = {}
#for n in range(1, 4):
#    padded = process(train_set, n)
#    models[n] = train(padded, n)
#lambdas = optimize_lambdas(held_out[:100], models, step=0.1)
#pp = perplexity(test_set, models, lambdas, n_max=3)
#print(f"{pp}\n{lambdas}")