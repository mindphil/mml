from preprocess import load_corpus, process, train

corpus = load_corpus('words_alpha.txt')
padded = process(corpus, 2)
model = train(padded, 2)