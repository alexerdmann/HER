import pickle
import sys
import os 
import fileinput
import random

def custom_list_eval_inclusive(train, test, predictions):

	predictions = (open(predictions).read().splitlines())
	predictedNEs = {}
	correctNEs = {}

	for line in fileinput.input(train):
		if len(line.split()) > 1:
			label = line.split()[0]
			word = line.split()[1]
			if label != '0':
				if label not in predictedNEs:
					predictedNEs[label] = {}
				predictedNEs[label][word] = True
				if label not in correctNEs:
					correctNEs[label] = {}
				correctNEs[label][word] = True
	fileinput.close()

	index = -1
	for line in fileinput.input(test):
		index += 1
		if len(line.split()) > 1:
			label = line.split()[0]
			word = line.split()[1]

			if label != '0':
				if label not in correctNEs:
					correctNEs[label] = {}
				correctNEs[label][word] = True

			if index == 0 and len(predictions[index].split()) == 0:
				index += 1
			predLine = predictions[index]
			predLabel = predLine.split()[0]

			if predLabel != '0':
				if predLabel not in predictedNEs:
					predictedNEs[predLabel] = {}
				predictedNEs[predLabel][word] = True
		elif index == 0:
			index -= 1

	fileinput.close()

	correct = 0
	precDenom = 0
	recDenom = 0

	for l in correctNEs:
		for w in correctNEs[l]:
			recDenom += 1
			if l in predictedNEs and w in predictedNEs[l]:
				correct += 1

	for l in predictedNEs:
		for w in predictedNEs[l]:
			precDenom += 1

	if precDenom == 0:
		prec = 0
	else:
		prec = correct / precDenom
	if recDenom == 0:
		return 0, 0, 0, 0
	else:
		rec = correct / recDenom
	if prec == 0 or rec == 0:
		F = 0
	else:
		F = 2 * ( (prec * rec) / (prec + rec))

	return F, prec, rec, recDenom

def custom_list_eval_exclusive(test, predictions):

	predictions = (open(predictions).read().splitlines())
	predictedNEs = {}
	correctNEs = {}

	index = -1
	for line in fileinput.input(test):
		index += 1
		if len(line.split()) > 1:
			label = line.split()[0]
			word = line.split()[1]

			if label != '0':
				if label not in correctNEs:
					correctNEs[label] = {}
				correctNEs[label][word] = True

			if index == 0 and len(predictions[index].split()) == 0:
				index += 1
			predLine = predictions[index]
			predLabel = predLine.split()[0]

			if predLabel != '0':
				if predLabel not in predictedNEs:
					predictedNEs[predLabel] = {}
				predictedNEs[predLabel][word] = True

	fileinput.close()

	correct = 0
	precDenom = 0
	recDenom = 0

	for l in correctNEs:
		for w in correctNEs[l]:
			recDenom += 1
			if l in predictedNEs and w in predictedNEs[l]:
				correct += 1

	for l in predictedNEs:
		for w in predictedNEs[l]:
			precDenom += 1

	if precDenom == 0:
		prec = 0
	else:
		prec = correct / precDenom
	if recDenom == 0:
		return 0, 0, 0, 0
	else:
		rec = correct / recDenom
	if prec == 0 or rec == 0:
		F = 0
	else:
		F = 2 * ( (prec * rec) / (prec + rec))

	return F, prec, rec, recDenom

def custom_eval_inclusive(train, test, predictions):

	predictions = (open(predictions).read().splitlines())
	correct = 0
	precDenom = 0
	recDenom = 0

	for line in fileinput.input(train):
		if len(line.split()) > 1:
			label = line.split()[0]
			word = line.split()[1]
			if label != '0':
				correct += 1
				recDenom += 1
				precDenom += 1
	fileinput.close()

	index = -1
	for line in fileinput.input(test):
		index += 1
		if len(line.split()) > 1:
			label = line.split()[0]
			word = line.split()[1]

			if label != '0':
				recDenom += 1

			if index == 0 and len(predictions[index].split()) == 0:
				index += 1
			predLine = predictions[index]
			predLabel = predLine.split()[0]

			if predLabel != '0':
				precDenom += 1
				if predLabel == label:
					correct += 1

	fileinput.close()

	if precDenom == 0:
		prec = 0
	else:
		prec = correct / precDenom
	if recDenom == 0:
		return 0, 0, 0, 0
	else:
		rec = correct / recDenom
	if prec == 0 or rec == 0:
		F = 0
	else:
		F = 2 * ( (prec * rec) / (prec + rec))

	return F, prec, rec, recDenom

def custom_eval_exclusive(test, predictions):

	predictions = (open(predictions).read().splitlines())
	correct = 0
	precDenom = 0
	recDenom = 0

	index = -1
	for line in fileinput.input(test):
		index += 1
		if len(line.split()) > 1:
			label = line.split()[0]
			word = line.split()[1]

			if label != '0':
				recDenom += 1

			if index == 0 and len(predictions[index].split()) == 0:
				index += 1
			predLine = predictions[index]
			predLabel = predLine.split()[0]

			if predLabel != '0':
				precDenom += 1
				if predLabel == label:
					correct += 1

	fileinput.close()

	if precDenom == 0:
		prec = 0
	else:
		prec = correct / precDenom
	if recDenom == 0:
		return 0, 0, 0, 0
	else:
		rec = correct / recDenom
	if prec == 0 or rec == 0:
		F = 0
	else:
		F = 2 * ( (prec * rec) / (prec + rec))

	return F, prec, rec, recDenom

def custom_eval_biased_recall_exclusive(test, predictions):
	list_recall = custom_list_eval_exclusive(test, predictions)
	list_recall = list_recall[2]
	text_F = custom_eval_exclusive(test, predictions)
	total = text_F[-1]
	text_F = text_F[2]

	biased_F = 2 * ( (text_F * list_recall) / (text_F + list_recall) )

	return biased_F, total

def custom_eval_biased_recall_inclusive(train, test, predictions):
	list_recall = custom_list_eval_inclusive(train, test, predictions)
	list_recall = list_recall[2]
	text_F = custom_eval_inclusive(train, test, predictions)
	text_F = text_F[2]

	biased_F = 2 * ( (text_F * list_recall) / (text_F + list_recall) )

	return biased_F

if __name__ == '__main__':

	train = sys.argv[1]
	test = sys.argv[2]
	predictions = sys.argv[3]

	F, prec, rec, recDenom = custom_list_eval_inclusive(train, test, predictions)
	print('F (PREC, REC) (COUNT): {}     ( {}    {})    ({})'.format(str(F),str(prec),str(rec),str(recDenom)))

	biased_F, total = custom_eval_biased_recall_inclusive(train, test, predictions)
	print('Recall-biased-F: {}'.format(str(biased_F)))

