# coding=utf-8
from collections import defaultdict

ANSWERS = open('wordle_answers.txt').read().split('\n')
GUESSES = open('wordle_guesses.txt').read().split('\n') + ANSWERS


def calc_bucket(a, g):
    # print('An', a, 'Guess', g)
    a = list(a)
    g = list(g)
    bucket = ['-', '-', '-', '-', '-']
    for i in range(5):
        if g[i] == a[i]:
            bucket[i] = 'g'
            g[i] = '.'
            a[i] = '_'
    for i in range(5):
        for j in range(5):
            if g[i] == a[j]:
                bucket[i] = 'y'
                a[j] = '_'

    return ''.join(bucket)

def buckets(guess, answers):
    # print(guess)
    guess_buckets = defaultdict(int)
    for a in answers:
        bucket = calc_bucket(a, guess)
        guess_buckets[bucket] += 1

    largest_bucket = 0
    two_guesses = 0
    total_val = 0
    for bucket, value in guess_buckets.items():
        # print(bucket, value)
        if value > largest_bucket:
            largest_bucket = value
        if value == 1:
            two_guesses += 1
        total_val += 1 / value

    # print(guess_buckets)
    return two_guesses, largest_bucket, total_val

def best_guess(answer):
    answers = ANSWERS
    guess = 'trace'
    round = 0
    while len(answers) > 1:
        round += 1
        print(f"{guess}", end=",")
        ans_bucket = calc_bucket(answer, guess)
        new_answers = []
        for a in answers:
            bucket = calc_bucket(a, guess)
            if bucket == ans_bucket:
                new_answers.append(a)
        answers = new_answers
        # print(answers)

        best_guess = ''
        best_guess_val = 0
        smallest_large = 1000
        for g in range(len(GUESSES)):
            val, large, total_val = buckets(GUESSES[g], answers)
            if total_val > best_guess_val:
                best_guess_val = total_val
                best_guess_tot = GUESSES[g]
            elif total_val == best_guess_val and GUESSES[g] in answers:
                best_guess_tot = GUESSES[g]
            if large < smallest_large:
                smallest_large = large
                best_guess = GUESSES[g]
            elif large == smallest_large and GUESSES[g] in answers:
                best_guess = GUESSES[g]
        # print('righton', best_guess_tot, best_guess_val)
        if round <= 2:
            guess = best_guess_tot
        else:
            guess = best_guess
        # print('SMALL', best_guess, smallest_large)
    print(f"{answer}")

if __name__ == '__main__':
    for a in ANSWERS:
        best_guess(a)
