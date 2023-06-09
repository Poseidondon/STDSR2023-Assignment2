"""
Source: Lab 13
"""


import math


def ind_max(x):
    m = max(x)
    return x.index(m)


class UCB:
    def __init__(self, confidence=0.6, n_arms=3, counts=None, values=None):
        self.confidence = confidence
        if not (counts and values):
            self.counts = [0 for _ in range(n_arms)]
            self.values = [0.0 for _ in range(n_arms)]
        else:
            self.counts = counts
            self.values = values
        return

    def select_arm(self):
        n_arms = len(self.counts)
        for arm in range(n_arms):
            if self.counts[arm] == 0:
                return arm

        ucb_values = [0.0 for arm in range(n_arms)]
        total_counts = sum(self.counts)
        for arm in range(n_arms):
            if self.counts[arm] == 0:
                uncertainty = float('inf')
            else:
                uncertainty = self.confidence * math.sqrt((math.log(total_counts)) / float(self.counts[arm]))
            ucb_values[arm] = self.values[arm] + uncertainty

        return ind_max(ucb_values)

    def update(self, chosen_arm, reward):
        self.counts[chosen_arm] = self.counts[chosen_arm] + 1
        n = self.counts[chosen_arm]

        value = self.values[chosen_arm]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value
        return
