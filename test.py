import numpy as np
import csv

csv1 = open('./label1.csv', 'r', encoding = 'utf8')
label1 = [row[0] for row in csv.reader(csv1)]

csv2 = open('./label2.csv', 'r', encoding = 'utf8')
label2 = [row[0] for row in csv.reader(csv2)]

wrong = open('./wrong.csv', 'w+', encoding = 'utf8')

index = 0
for label in label1:
	if label != label2[index]:
		wrong.write(str(index) + '\n')
	index += 1

csv1.close()
csv2.close()
wrong.close()