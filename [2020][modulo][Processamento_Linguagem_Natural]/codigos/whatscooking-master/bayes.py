import numpy as np
import logging

'''
This module contains the functions needed to classify a list of recipes,
based on naive bayes method trained by a dataset of categorized recipes.
Some functions are based on the samples of the Machine Learning in Action book.
'''

def createVocabulary(trainrecipes):
	vocabSet = set([])
	for document in trainrecipes:
		vocabSet = vocabSet | set(document['ingredients'])
	return list(vocabSet)

def createClasses(trainrecipes):
	classSet = set([])
	for recipe in trainrecipes:
		classSet = classSet | set([recipe['cuisine']])
	return list(classSet)

def createFeatVector(vocabList, ingredientsList):
	featureVec = [0]*len(vocabList)
	notFound = 0
	notFoundTokens = []
	for word in ingredientsList:
		if word in vocabList:
			featureVec[vocabList.index(word)] = 1;
		else: 
			logging.debug("word %s is not in my vocabulary" % word)
			notFoundTokens.append(word)
			notFound += 1
	if notFound > 0:
		logging.debug(" recipe with ingrendients not found in the vocabulary")
		logging.debug("  tokens: %d, notfound: %d" % (len(ingredientsList),notFound))
		logging.debug("  not found: " + str(notFoundTokens))

	return featureVec, notFound

def trainNB(trainrecipes, vocabulary, classes):
	''' Bayes Theorem: p(c|w) = (p(w|c) * p(c)) / p(w) 
		This funcion calculates priors p(w|c) and p(c) 
		for each class present in the training data set
	'''
	
	''' initialization'''
	# Laplace smoothing (add 1 numerator) 
	numeratorPwc = np.array([[1.0]*len(vocabulary)]*len(classes))
	# Laplace smoothing (denominator)
	denominatorPwc = np.array([len(classes)]*len(vocabulary))
	# pc (vector)
	pc = np.array([0.0] * len(classes))	

	'''Builds p(c) and p(w|c) vectors for each class'''
	for recipe in trainrecipes:
		classIndex = classes.index(recipe['cuisine'])
		#pc
		pc[classIndex] += 1
		#pwc
		recipeFeatVector, numberOfNotFoundTokens = createFeatVector(vocabulary,recipe['ingredients'])
		numeratorPwc[classIndex] += recipeFeatVector
		denominatorPwc += recipeFeatVector
	
	'''Calculates pc and pwc'''	
	#pc[]/number of classes
	pc = pc / float(sum(pc))
	# calculates pwc using log to avoid underflow problem
	pwc = np.log(numeratorPwc / denominatorPwc)

	return pc, pwc

def classifyNB(pc, pwc, ingredFeatVector):
	'''	For each class calculates p(c|w), the probability of a class c
	    given a recipe w (represented as a feature vector) '''
	pcw=np.array([0.0]*len(pwc))
	for i in range(len(pcw)):
		pcw[i] = sum(pwc[i] * ingredFeatVector) + np.log(pc[i])
	
	#get maximum p(c|w) value (array index) to define the best class for this recipe
	classIndex = pcw.tolist().index(max(pcw))
	return classIndex
	
def run(trainrecipes, unkrecipes):

	logging.info("creating vocabulary...")
	vocabulary = createVocabulary(trainrecipes)
	logging.info("extracting classes...")
	classes = createClasses(trainrecipes)
	
	logging.info("training NB Classifier...")
	pc, pwc = trainNB(trainrecipes, vocabulary, classes)
	logging.info("classifying using NB...")
	classrecipes = {}
	nfTokens = 0
	nfTokensrecipes = 0

	for recipe in unkrecipes:
		featureVector, nft = createFeatVector(vocabulary,recipe['ingredients'])
		nfTokens += nft
		if nft > 0: nfTokensrecipes += 1
		classIndex= classifyNB(pc,pwc,featureVector)
		classrecipes[recipe['id']] = classes[classIndex]


	logging.info("### NB run summary ###")
	logging.info("  train dataset size: %d"  %len(trainrecipes))
	logging.info("  recipes to classify: %d"  %len(unkrecipes))
	logging.info("  vocabulary size: %d"  %len(vocabulary))
	logging.info("  number of classes: %d"  %len(classes))
	logging.info("  ingredients not in the vocabulary: %d" % nfTokens)
	logging.info("  recipes with ingredients not in the vocabulary: %d" % nfTokensrecipes)
  	
	return classrecipes