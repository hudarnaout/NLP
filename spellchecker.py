import re
from collections import Counter

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

# Usage example
while True:
    user_input = input("Enter a word (or 'q' to quit): ")
    if user_input == 'q':
        break
    corrected_word = correct(user_input)
    print(f"Corrected: {corrected_word}")
