from bandit import test, logger, backend
from bandit.choice import Choice


class MyLogger(logger.Logger):
    """
    Example logger
    """
    def key(self, name, id):
        return name + ' ' + str(id)

    def hit(self, choice, **kwargs):
        print 'Logging Hit', choice, kwargs
        key = self.key(kwargs['meta']['name'], choice.id)
        self.hits[key] += 1

    def attempt(self, choice, **kwargs):
        print 'Logging Attempt', choice, kwargs
        key = self.key(kwargs['meta']['name'], choice.id)
        self.attempts[key] += 1


class MyBackend(backend.BanditBackend):
    """
    Example backend
    """
    def select(self, limit=None, **kwargs):
        return self.choices[:limit]


class MyTest(test.Test):
    """
    Example test
    """
    logger = MyLogger
    backend = MyBackend


class MyOtherTest(test.Test):
    logger = MyLogger
    backend = MyBackend


# Create a few tests
test = MyTest([Choice(i,i) for i in range(3)])
test2 = MyOtherTest([Choice(i,i) for i in range(3)])


# Some test metadata
meta = {'name': 'foo'}


# Select choices (attempts implicitly logged)
test_choices = test.select(2, meta=meta)
test2_choices = test2.select(3, meta=meta)


# Log hits
test.hit(test_choices[0], meta=meta)
test2.hit(test2_choices[0], meta=meta)


# Print out the data
print test.data()
print test2.data()

