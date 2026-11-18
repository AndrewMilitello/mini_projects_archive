#simple Naive Bayes Classifier I built 3 years ago (in 7th grade) - this was my first ML project
from math import *
dataset = [[1, 0],
        [3, 0],
        [2, 1],
        [4, 1]]
def naive_bayes_classifier(dataset):
    def organize_data(dataset):
    	separated = dict()
    	for i in range(len(dataset)):
    		vector = dataset[i]
    		class_value = vector[-1]
    		if (class_value not in separated):
    			separated[class_value] = list()
    		separated[class_value].append(vector)
    	return separated

    separated = organize_data(dataset)
    for label in separated:
    	print(label)
    	for row in separated[label]:
    		print(row)
    def mean(numbers):
        return float(sum(numbers))/float(len(numbers))
    def standev(numbers):
    	avg = mean(numbers)
    	variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
    	return sqrt(variance)
    def summarize_data(dataset):
        summaries = [(mean(column), standev(column), len(column)) for column in zip(*dataset)]
        del(summaries[-1])
        return summaries
    def summarize_by_class(dataset):
        separated = organize_data(dataset)
        summaries = dict()
        for class_value, rows in separated.items():
            summaries[class_value] = summarize_data(rows)
        return summaries
    def gaussian_prob(x, mean, standev):
        e = (-(((x-mean)**2)/(2*standev**2))) 
        return (1/(sqrt(2*pi))*standev)*exp(e)
    def probability_calculation(summaries, row):
    	total_rows = sum([summaries[label][0][2] for label in summaries])
        print(total_rows)
        probabilities = dict()
    	for class_value, class_summaries in summaries.items():
    		probabilities[class_value] = summaries[class_value][0][2]/float(total_rows)
    		for i in range(len(class_summaries)):
    			mean, stdev, count = class_summaries[i]
    			probabilities[class_value] *= gaussian_prob(row[i], mean, stdev)
    	return probabilities, total_rows
    summaries = summarize_by_class(dataset)
    probabilities = probability_calculation(summaries, dataset[0])
    print(probabilities)
naive_bayes_classifier(dataset)
