#!/usr/bin/env python

'''
Program created for the What is Cooking Challenge.
https://www.kaggle.com/c/whats-cooking
'''

import bayes, sys, json, argparse, logging

#setup argparse
parser = argparse.ArgumentParser(
    description='Whatscooking Program'
)
parser.add_argument("trainRecipesFile", help="train dataset")
parser.add_argument("unknownRecipesFile", help="unknown recipes dataset")
parser.add_argument("outputFile", help="output csv file")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

def main(argv):
	#load json files.
	with open(args.trainRecipesFile) as train_recipes_file:
		trainJson = json.load(train_recipes_file)
	with open(args.unknownRecipesFile) as unknown_recipes_file:
		unknownJson = json.load(unknown_recipes_file)

	results = {}

	#run naive bayes classifier.
	results = bayes.run(trainJson,unknownJson)

	# write to output file
	text_file = open(args.outputFile, "w")
	text_file.write('id,cuisine\n')
	for i in results:
		text_file.write(str(i) + ',' + results[i] + '\n')
	text_file.close()

if __name__ == '__main__':
    main(sys.argv)