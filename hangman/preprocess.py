# data set is already all lowercase, just need to tokenize and add padding.
def process(corpus, n):
    tokens = [list(word) for word in corpus]
    padded_tokens = [
        ['<s>'] * (n - 1) + word + ['</s>'] 
        for word in tokens
    ]
    return padded_tokens
#test
#print(process(['hello'], 4))

## method for trimming down training data?

def ngram(padded_tokens, n):
    result = []
    for i in range(0, len(padded_tokens)-n+1):
        result.append(tuple(padded_tokens[i:i+n]))
    return result
#test = process(['hello'], 4)
#print(ngram(test[0], 4))

def train(padded_tokens,n):
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
    vocab.remove('<s>')

    for context in model:
        for char in vocab:
            if char not in model[context]:
                model[context][char] = 0

    for context, targets in model.items():
        total_count = float(sum(targets.values()))
        for target in targets:
            targets[target] = (targets[target] + 1) / (total_count + len(vocab))
    return model
#test
padded = process(['hello', 'help', 'held'], 2)
model = train(padded, 2)
print(model)

