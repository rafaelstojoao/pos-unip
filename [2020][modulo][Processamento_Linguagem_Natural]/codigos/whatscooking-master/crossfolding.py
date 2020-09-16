#!/usr/bin/env python
import bayes, sys, json, numpy as np, logging, argparse
'''
Program to evaluate classifier based on ten fold validation
'''

#setup argparse
parser = argparse.ArgumentParser(
    description='Whatscooking Program cross folding classifier'
)
parser.add_argument("trainRecipesFile", help="training data set")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.INFO)

def crossfolding(trainrecipes):
	logging.info("### run summary ###")
	#initialize counters (at least 2)
	numPartitions = 10
	accuracy = np.array([0.0] * numPartitions)
	partitionsSize = np.array([0] * numPartitions)
	
	#define partitions size
	if len(trainrecipes) < numPartitions: 
		logging.error("Train dataset must have more than %d items" % numPartitions)
		sys.exit(0)
	partitionsSize += len(trainrecipes) / numPartitions
	for i in range(len(trainrecipes) % numPartitions):
		partitionsSize[i] += 1
	logging.info(">number of training recipes: %d" % len(trainrecipes))

	#calculate accuracy for each partition
	logging.info("...calculating accuracy for each partition...")
	partitionIndex = 0
	for i in range(numPartitions):
		logging.info("FOLD %d" % (i+1))
		#get train and test lists		
		testList = trainrecipes[partitionIndex:partitionIndex+partitionsSize[i]]
		trainList = [] * (len(trainrecipes)-len(testList))
		for nDocument in range(len(trainrecipes)):
			if (nDocument < partitionIndex) | (nDocument>partitionIndex+partitionsSize[i]):
				trainList.append(trainrecipes[nDocument])
		partitionIndex += partitionsSize[i]
		
		#classify test list
		classifiedList = bayes.run(trainList,testList)
		totalrecipes = 0.0
		truePositives = 0.0
		for recipe in testList:
			totalrecipes += 1
			if classifiedList[recipe['id']] == recipe['cuisine']:
				truePositives += 1
		#compare classification to calculate accuracy
		accuracy[i] = truePositives / totalrecipes
	#calculate avg accuracy
	avgAccuracy = 0.0
	avgAccuracy = np.average(accuracy)
	return avgAccuracy

def main(argv):
	with open(args.trainRecipesFile) as train_recipes_file:
		trainJson = json.load(train_recipes_file)

	#does crossfolding validation
	accuracy = crossfolding (trainJson)
	print "Accuracy=%f" % accuracy

if __name__ == '__main__':
    main(sys.argv)