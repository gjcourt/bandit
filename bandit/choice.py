from collections import namedtuple

choice = namedtuple('Choice', ['id', 'obj'])
weighted_choice = namedtuple('WeightedChoice', ['id', 'obj', 'weight'])

