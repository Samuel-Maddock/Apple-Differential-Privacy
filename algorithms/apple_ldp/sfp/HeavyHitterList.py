from sortedcontainers import SortedKeyList
from operator import itemgetter


class HeavyHitterList:
    def __init__(self, threshold):
        self.data = SortedKeyList(key=itemgetter(1))
        self.threshold = threshold

    def append(self, x):
        if len(self.data) < self.threshold:
            self.data.add(x)
        else:
            if x[1] > self.data[0][1]:
                self.data.remove(self.data[0])
                self.data.add(x)

    def get_data(self):
        return self.data

    def __str__(self):
        return self.data.__str__()
