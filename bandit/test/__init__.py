from bandit.backends import OptimizingBackend


class ProportionateTest(object):
    """
    This is an abstract base class for a bandit multivariate optimization algorithm.
    To use, subclass ProportionateTest and Choice.  Instantiate your subclass
    with a set of choices.

    Call log_hit when a hit occurs.  log_attempt is called automatically.
    The default behavior uses the hit/attempt ratio to calculate probabilities
    of choosing each choice.

    Call make_choices to retrieve a set of choices.
    """

    def __init__(self, choices, backend=OptimizingBackend, *args, **kwargs):
        self.choices = choices
        self.backend = backend(self.choices, self.__class__.__name__, *args, **kwargs)

    def make_choices(self, n, log_choices=True, **kwargs):
        selections = self.backend.make_choices(n)
        if log_choices:
            self.log_attempts(selections, **kwargs)
        return [selection.choice_object for selection in selections]

    def log_hits(self, items, **kwargs):
        return self.log_items(self.log_hit, items, **kwargs)

    def log_attempts(self, items, **kwargs):
        return self.log_items(self.log_attempt, items, **kwargs)

    def log_items(self, fn, items, **kwargs):
        for item in items:
            fn(item.id, **kwargs)

    def make_choice(self, log_choices=True, **kwargs):
        choices = self.make_choices(1, log_choices=log_choices, **kwargs)
        return choices[0] if len(choices) else None

    @classmethod
    def log_hit(cls, choice_id, **kwargs):
        Event(test_name=cls.__name__, choice_id=choice_id, mode="hit", **kwargs).execute()

    @classmethod
    def log_attempt(cls, choice_id, **kwargs):
        Event(test_name=cls.__name__, choice_id=choice_id, mode="attempt", **kwargs).execute()

