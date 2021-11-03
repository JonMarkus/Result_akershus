"""
Compute number of mandates for each party based on the modified Sainte-Laguë rule.

The rule works as follows:
1. Each party receives a score equal to the number of votes received divided by 1.4.
2. All parties are sorted in descending order of scores.
3. The party with the largest score is then
   a. assigned a seat
   b. receives a new score, which is its number of votes divided by 3.
4. The process continues with point 2, successively using divisors 3, 5, 7, ..., until
   all seats have been assigned.

Note that divisors are increased independently for each party.

Expected results from this code are:

    A, H: 5 mandates each
    FRP, SP: 2 mandates each
    MDG, RØDT, SV, V: 1 mandate each

Høyre has six mandates from Akershus in total in the current Storting because they were allocated
the utjevningsmandat for Akershus.
"""

import pandas as pd

# Seats allocated to Akershus district. One seat is reserved for an utjevningsmandat
# (ensures better proprotional representation on the national level). Here, only the
# remaining "distriktsmandater" are distributed.
NUM_MANDATES = 19
NUM_DISTRICT_MANDATES = NUM_MANDATES - 1

# Read example data from CSV file into DataFrame
election_results = pd.read_csv('result_akershus_2021.csv')

# Create a record for each party containing the party name, the number of votes received,
# the initial score according to point 1, and the divisor for the next division (points 3.b and 4)

class party_result:

    def __init__(self, party, votes):
        self.party = party
        self.votes = votes
        self.score = votes/1.4
        self.next_div = 3

    def update_score(self):
        self.score = self.votes / self.next_div
        self.next_div += 2

scoring_data = [party_result(row.Party, row.Votes) for row in election_results.itertuples()]

# Distribute mandates, counting how many mandates are assigned to each party
mandates = {}
while sum(mandates.values()) < NUM_DISTRICT_MANDATES:
    # Ensure data is sorted in descending order of scores
    scoring_data.sort(key=lambda r: r.score, reverse=True)

    # First entry in sorted list wins the mandate
    winner = scoring_data[0]

    # Register seat won
    mandates[winner.party] = mandates.get(winner.party, 0) + 1

    # Update winner entry with new score and divisor for next round
    winner.update_score()

# Report mandates won
for party, seats in mandates.items():
    print(f'{party:<4s}: {seats:2d} mandates')
