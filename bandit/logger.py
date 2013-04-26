from collections import Counter

class Logger(object):
    def __init__(self):
        self._hit_counter = Counter()
        self._attempt_counter = Counter()

    def key(self, choice, mode):
        return mode[0]+':'+str(choice.id)

    def hit(self, choice):
        self._hit_counter[choice.id] += 1

    def attempt(self, *args, **kwargs):
        self._attempt_counter[choice.id] += 1

