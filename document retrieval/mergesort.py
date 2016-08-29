#
# This file contains the Python code from Program 15.13 of
# "Data Structures and Algorithms
# with Object-Oriented Design Patterns in Python"
# by Bruno R. Preiss.
#
# Copyright (c) 2003 by Bruno R. Preiss, P.Eng.  All rights reserved.
#
# http://www.brpreiss.com/books/opus7/programs/pgm15_13.txt
#
class TwoWayMergeSorter(Sorter):

    def __init__(self):
        super(TwoWayMergeSorter, self).__init__()
        self._tempArray = None

    # ...

    
    def merge(self, left, middle, right):
        i = left
        j = left
        k = middle + 1
        while j <= middle and k <= right:
            if self._array[j] < self._array[k]:
                self._tempArray[i] = self._array[j]
                i += 1
                j += 1
            else:
                self._tempArray[i] = self._array[k]
                i += 1
                k += 1
        while j <= middle:
            self._tempArray[i] = self._array[j]
            i += 1
            j += 1
        for i in xrange(left, k):
            self._array[i] = self._tempArray[i]

    # ...

    def _sort(self):
        self._tempArray = Array(self._n)
        self.mergesort(0, self._n - 1)
        self._tempArray = None

    def mergesort(self, left, right):
        if left < right:
            middle = (left + right) / 2
            self.mergesort(left, middle)
            self.mergesort(middle + 1, right)
            self.merge(left, middle, right)

    # ...
