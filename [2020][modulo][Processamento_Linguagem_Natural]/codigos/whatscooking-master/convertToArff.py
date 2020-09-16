#!/usr/bin/env python

'''
Program to convert Json training dataset to ARFF format
'''

import bayes, sys, json, argparse, logging

#setup argparse
parser = argparse.ArgumentParser(
    description='Convert Json training data set to Arff'
)
parser.add_argument("trainFile", help="train dataset")
parser.add_argument("arffFile", help="arffFile")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

def main(argv):
	#load json files.
	with open(args.trainFile) as train_receipes_file:
		trainJson = json.load(train_receipes_file)
	text_file = open(args.arffFile, "w")

	#create header
	header = ""
	header += "% Title: Receipes training data\n"
	header += "@RELATION receipe\n"
	header += "@ATTRIBUTE id numeric\n"
	classes = ""
	classSet = set([])
	for receipe in trainJson:
		classSet = classSet | set([receipe['cuisine']])
	classList = list(classSet)
	for classe in classList:
		classes += ( classe + ",")
	classes = classes[:-1]
	header += ("@ATTRIBUTE class {" + classes + "}\n@DATA\n")
	text_file.write(header)
   
	#convert each record
	for receipe in trainJson:
		body = ""
		body = "\n" + str(receipe['id']) + "," + body + receipe['cuisine']
		text_file.write(body)

	# write to output file
	text_file.close()

if __name__ == '__main__':
    main(sys.argv)