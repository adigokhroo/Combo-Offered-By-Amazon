import sys
import csv
from combo.register.models import Document
from combo.register.forms import DocumentForm
import os

#for filename in request.FILES:
    #file_name = request.FILES[filename].name

file_name = Document.filename

path1 = "C:\\Users\\mayank jain\\Desktop\\combo\\media\\documents"
path2 = os.path.join(path1, "test.csv")


def subset_sum(numbers, target, partial=list()):
    s = sum(partial)
    # check if the partial sum is equals to target
    if s == target:
        with open(path2, 'a') as csv_file1:
            writer = csv.writer(csv_file1)
            writer.writerow(partial)

    if s >= target:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i + 1:]
        subset_sum(remaining, target, partial + [n])

if __name__ == '__main__':
    subset_sum([0], 500)
