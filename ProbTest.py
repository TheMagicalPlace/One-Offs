from random import choice
from collections import Counter
from copy import  copy
from colorama import Fore, Back, Style
import sqlite3

if __name__ == '__main__':
    options = 4 # int
    weights = None # [0.1,0.5,0.22,0.012] # set weights, must be a list of length == options
    rounds = 10000 # int, number of rounds
    choices_per_round = 231
    outcomes_default = {}

    if weights is not None:
        minweight = sorted(weights)[0]
        for i,w in enumerate(weights):
            if w/minweight - w//minweight > 0.5:
                weights[i] = (w//minweight+1)
            else:
                weights[i] = w//minweight
            weights[i] = int(weights[i])
        choices = []
        for i in range(1,1+options):
            for j in range(weights[i-1]):
                choices.append(i)
                outcomes_default[i] = 0
    else:
        choices = list(range(1,1+options))
        outcomes_default = {c:0 for c in choices}

    avg_outcomes = copy(outcomes_default)
    for rnd in range(1,rounds+1):
        outcomes = copy(outcomes_default)
        for _ in range(choices_per_round):
            sel = choice(choices)
            outcomes[sel]+=1
            avg_outcomes[sel]+=1
        for i,res in outcomes.items():
            sd = (choices_per_round*(1/options)*(1-1/options))**1/2

            if res > choices_per_round*(1/options)+sd*1:
                print(f'Round {rnd} Results')
                print(Fore.RED + f'!! Notable Round !! ')
                print(Fore.RED + f'!! Choice {i} == {res} , {round((res-choices_per_round*1/options)/sd,2)} standard deviations from mean!! '+Style.RESET_ALL)

                break
        else:
            print(Style.RESET_ALL+f'Round {rnd} Results')
        print(f' Round Results   {outcomes}\n '
              f'Running Average { {n:round(res/rnd,2) for n,res in avg_outcomes.items()} }\n')