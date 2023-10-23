import re
from collections import Counter
from nltk import trigrams, FreqDist, ConditionalFreqDist

# Step 1: Load necessary data
def words(text):
    return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    return WORDS[word] / N

# Step 2: Define functions for generating possible corrections
def edits1(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in WORDS)

def known(words):
    return set(w for w in words if w in WORDS)

# Step 3: Define the spelling corrector function
def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=P)

# Define Brill and Moore transformation rules
def apply_rules(word):
    if word.endswith('ie'):
        return word[:-2] + 'y'
    return word

# Step 4: Integrate language model
def trigram_language_model(corpus):
    trigrams_list = list(trigrams(corpus))
    cfd = ConditionalFreqDist((w1_w2, w3) for w1_w2_w3 in trigrams_list for w1_w2, w3 in [(w1_w2_w3[:2], w1_w2_w3[2])])
    return cfd

# Example usage of language model
corpus = words(open('big.txt').read())
lm = trigram_language_model(corpus)

def language_model_probability(context, word):
    return lm[context].freq(word)

# Usage example
while True:
    user_input = input("Enter a word (or 'q' to quit): ")
    if user_input == 'q':
        break
    user_input = apply_rules(user_input)
    candidates = known([user_input]) or known(edits1(user_input)) or known_edits2(user_input) or [user_input]
    corrected_word = max(candidates, key=lambda w: P(w) * language_model_probability(tuple(user_input.split()[-2:]), w))
    print(f"Corrected: {corrected_word}")
