from bandit import logger
from bandit.backend import base


class TestMeta(type):
    def __new__(meta, name, bases, attrs):
        required_attrs = {
            'backend': base.BanditBackend,
            'logger': logger.Logger,
        }

        _meta = {'test_name': name}

        for attr, default in required_attrs.items():
            if attr in attrs:
                _attr = attrs[attr]
            else:
                _attr = type(
                    '%s%s' % (name, attr.capitalize()),
                    (default, ),
                    {'test_name': name}
                )

            _meta[attr] = _attr

        attrs['_meta'] = type('_meta', (object, ), _meta)()

        return super(TestMeta, meta).__new__(meta, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        return super(TestMeta, cls).__init__(name, bases, attrs)


class Test(object):
    """
    This is an abstract base class for a bandit multivariate optimization algorithm.
    To use, subclass Test and choice.  Instantiate your subclass
    with a set of choices.

    Call hit when a hit occurs.  attempt is called automatically.
    The default behavior uses the hit/attempt ratio to calculate probabilities
    of choosing each choice.

    Call make_choices to retrieve a set of choices.
    """
    __metaclass__ = TestMeta

    def __init__(self, choices):
        self.choices = choices
        self.backend = self._meta.backend(self._meta.test_name, self.choices)
        self.logger = self._meta.logger()

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


class MyTest(Test):
    pass

