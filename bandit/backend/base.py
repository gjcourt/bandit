import hashlib
import itertools
import random

from bandit.math import dot_product, normalize
from bandit.math.decorators import normalize


class BanditBackend(object):
    def __init__(self, test_name, choices):
        self.test_name = test_name
        self.choices = choices


class OptimizingBackend(BanditBackend):
    def __init__(self, *args, **kwargs):
        super(OptimizingBackend, self).__init__(*args, **kwargs)
        self.boost_methods = (self.ctr_boost, self.dither_boost)

    def average_ctr(self):
        return mean_ctr(self.test_name)

    def get_boost_weights(self):
        boosts = self._zk_bandit_boosts()
        weights = ()
        weights = tuple([boosts[m.func_name] for m in self.boost_methods])

        return weights

    @normalize
    def ctr_boost(self):
        return evm_wrapper(self.test_name, [c.id for c in self.choices], self.zk)

    @normalize
    def dither_boost(self):
        ctr = self.average_ctr()
        return [ctr*random.random() for choice in self.choices]

    def get_boosted_scores(self, **kwargs):
        # Matrix of score vectors.

        # TODO switch this to a simple matrix calculation
        scores = [boost_method() for boost_method in self.boost_methods]

        # TODO switch to use beta-distribution like https://github.com/pymc-devs/pymc

        # Transpose the above score matrix so that vector rows represent scores for a
        # given choice. Take the dot product of each choice score vector
        # with a boost_weight vector.
        weighted_scores = map(lambda score_set: dot_product(score_set, self.get_boost_weights()), zip(*scores))

        return weighted_scores

    def filter_choices(self, choices):
        """
        Filter choices
        """
        return choices

    def make_choices(self, n, **kwargs):
        if not self.choices:
            return []
        scores = self.get_boosted_scores(**kwargs)
        selections = [self.choices[i] for i, s in \
                sorted(enumerate(scores), key=lambda x:x[1], reverse=True)]
        return self.filter_choices(selections)[:n]


class RandomBackend(BanditBackend):
    def make_choices(self, n):
        n = min(n, len(self.choices))
        return random.sample(self.choices, n)


class RandomWeightedBackend(BanditBackend):
    def make_choices(self, n):
        scores = [random.random() + c.score for c in self.choices]
        sorted_choices = [pair[0] for pair in sorted(zip(self.choices, scores), key=lambda c: c[1], reverse=True)]
        return sorted_choices[0:n]


class ConsistentBackend(BanditBackend):
    """
    Ensures the same choices will be made whenever the same seed is used.
    """
    def __init__(self, choices, test_name, seed, *args):
        self.seed = seed
        super(ConsistentBackend, self).__init__(choices, test_name, *args)

    def make_choices(self, n):
        """
        Hashes the seed using md5
        Generates a list of all combinations of length n from self.choices
        Returns the list of combinations determined by the hash
        """
        hashed_seed = hashlib.md5(self.seed).hexdigest()
        combinations = list(itertools.combinations(self.choices, n))
        index = int(hashed_seed, 16) % len(combinations)
        return list(combinations[index])


