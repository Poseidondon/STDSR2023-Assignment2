import random
from scipy.stats import beta


def ind_max_posterior(x):
    m = max(x, key=lambda value: beta.rvs(value[0], value[1]))
    return x.index(m)


class EpsilonBernTS:
    def __init__(self, epsilon, n_arms, values=None):
        self.epsilon = epsilon
        if values:
            self.values = values
        else:
            self.values = [[1, 1] for _ in range(n_arms)]
        return

    def initialize(self, n_arms):
        # List: [alpha, beta]
        return

    def select_arm(self):
        if random.random() > self.epsilon:
            return ind_max_posterior(self.values)
        else:
            return random.randrange(len(self.values))

    def update(self, chosen_arm, reward):
        if reward == 1:
            self.values[chosen_arm][0] += 1
        else:
            self.values[chosen_arm][1] += 1
        return
