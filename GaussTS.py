"""
Source:
https://github.com/WhatIThinkAbout/BabyRobot/blob/master/Multi_Armed_Bandits/Part%205b%20-%20Thompson%20Sampling%20using%20Conjugate%20Priors.ipynb
"""

from scipy.stats import gamma, norm


def ind_max(x):
    m = max(x)
    return x.index(m)


class GaussTS:
    def __init__(self, n_arms=3, alphas=None, betas=None, means=None, counts=None):
        self.n_arms = n_arms
        if alphas:
            self.alphas = alphas
        else:
            self.alphas = [1 for _ in range(n_arms)]

        if betas:
            self.betas = betas
        else:
            self.betas = [10 for _ in range(n_arms)]

        if means:
            self.means = means
        else:
            self.means = [1 for _ in range(n_arms)]

        self.vars = [self.betas[i] / (self.alphas[i] + 1) for i in range(n_arms)]

        if counts:
            self.counts = counts
        else:
            self.counts = [0 for _ in range(n_arms)]
        return

    def select_arm(self):
        samples = [self.sample_arm(arm) for arm in range(self.n_arms)]

        return ind_max(samples)

    def sample_arm(self, arm):
        est_var = float('inf')
        precision = gamma.rvs(self.alphas[arm], 1 / self.betas[arm])
        if precision != 0 and self.counts[arm] != 0:
            est_var = 1 / precision

        sample = norm.rvs(self.means[arm], est_var ** 0.5)

        return sample

    def update(self, arm, reward):
        v = self.counts[arm]

        self.alphas[arm] = self.alphas[arm] + 0.5
        self.betas[arm] = self.betas[arm] + ((1 * v / (v + 1)) * (((reward - self.means[arm]) ** 2) / 2))

        # estimate the variance - calculate the mean from the gamma hyper-parameters
        self.vars[arm] = self.betas[arm] / (self.alphas[arm] + 1)

        self.means[arm] = (self.means[arm] * self.counts[arm] + reward) / (v + 1)
        self.counts[arm] += 1
        return
