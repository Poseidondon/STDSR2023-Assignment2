from scipy.stats import beta


class BernTS:
    def __init__(self, n_arms, values=None):
        if values:
            self.values = values
        else:
            self.values = [[1, 1] for _ in range(n_arms)]
        return

    def select_arm(self):
        ind = max(self.values, key=lambda value: beta.rvs(value[0], value[1]))
        return self.values.index(ind)

    def update(self, chosen_arm, reward):
        if reward == 1:
            self.values[chosen_arm][0] += 1
        else:
            self.values[chosen_arm][1] += 1
        return
