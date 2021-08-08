#!/usr/bin/env python

__author__ = "Patricio Henderson"
__email__ = "patricio.henderson.v@gmail.com"
__version__ = "1.0"

numbers = [1 , 3 , 3 , 8 , 4 , 3 , 2 , 3 , 3]
def canBeSpliited(numbers):
    sum = 0
    for i in numbers:
        sum += i
    if (sum % 2) != 0:
        return (-1)
    sum = (sum / 2)
    
    counter = 0
    left = 0
    for i in numbers:
        left += i
        counter += 1
        if left == sum:
            break
    
    right = 0
    counter2 = 0

    for i in numbers:    
        while counter2 < counter:
            counter2 += 1
            pass
        right += i
    if left == right :
        return(1)
    else:
        return(-1)

if __name__ == "__main__":
    print(canBeSpliited(numbers))
    