class Choice(object):
    """
    Choice objects have an ID that must be unique within a test and a choice object.
    The ID is used by the ProportionateTest class for tracking.
    The choice object can be any python object.
    """
    def __init__(self, choice_id, choice):
        self.id = choice_id
        self.choice_object = choice


class WeightedChoice(Choice):
    def __init__(self, choice_id, choice, weight):
        super(WeightedChoice, self).__init__(choice_id, weight)
        self.weight = weight

