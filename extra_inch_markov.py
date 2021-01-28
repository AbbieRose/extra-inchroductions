import os
import numpy as np

fragment_length = 4
f = open("introductions.txt")
text = " ".join(f.readlines())
text = " ".join(text.split())
text = text.lower()
text = text.encode("ascii", errors="ignore").decode()
f.close()
dictionary = {}
# put everything into a dictionary
for i in range(len(text) - fragment_length - 1) :
    fragment = text[i:i + fragment_length]
    next_letter = text[i + fragment_length:i + fragment_length + 1]
    if fragment in dictionary :
        if next_letter in dictionary[fragment] :
            dictionary[fragment][next_letter] += 1
        else :
            dictionary[fragment][next_letter] = 1
    else :
        dictionary[fragment] = {next_letter: 1}

def get_next_letter(fragment) :
    if fragment in dictionary :
        distribution = list(dictionary[fragment].items())
        keys = [k for k, _ in distribution]
        values = [v for _, v in distribution]
        sum_values = sum(values)
        values_distribution = list(map(lambda x: x/sum_values, values))
        return np.random.choice(keys, 1, p=values_distribution)[0]
    else:
        return np.random.choice([x for x in "abcdefghijklmnopqrstuvwxyz"])

def generate_opening(opening_length, starting_sequence) :
    opening = []
    opening.extend(starting_sequence)
    print(opening)
    current_fragment = starting_sequence[len(starting_sequence)-fragment_length:]
    for i in range(opening_length) :
        next_letter = get_next_letter(current_fragment)
        current_fragment = current_fragment[1:] + next_letter
        opening.append(next_letter)
    return ''.join(opening)

# for now will be 10 but we'll change that
def get_n_introductions(number) :
    initial_gram = "Our tactics guy, and "
    introductions = []
    for i in range(number) :
        opening = generate_opening(100, initial_gram)
        introductions.append(opening)
    return introductions
