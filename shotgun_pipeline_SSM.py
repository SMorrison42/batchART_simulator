#!/usr/bin/env python

### Developed by Shatavia Morrison, 20211213
### module load ART/latest

import gzip,argparse,os,sys,fnmatch,subprocess
import os.path
from datetime import datetime


### Read in input fasta location file and create dictionary of 
### sequences and desired depth coverage in list, will append
### global parameters to list for ART command composition

def seqCommandSet(fasta):
	seqSet={}
	count = 0
	with open(fasta,'r') as e:
		for line in e:
			count += 1
			lines = line.rstrip("\n")
			seqInfo = lines.split(",")
			seqSet[seqInfo[0]]= [seqInfo[1]]
			seqSet[seqInfo[0]].append(count)
	return seqSet
	

### ART arguments for shot gun dataset set in dictionary
def addGlobalARTParams(argsParams):
	artParams={}
	with open(argsParams,'r') as f:
		for line in f:
			lines = line.rstrip('\n')
			parInfo = lines.split(',')
			artParams['-'+parInfo[0]]=parInfo[1]
	return artParams

def ARTcommandSet(seqsSets,globalParams):
	shCommands = open("inSilico_shotgun.sh","w")
	shCommands.write("#!/bin/bash -l"+"\n")	
	### Need to get rid of outDir placeholder to allow for dynamic output results
	artPar = list(globalParams.keys())
	artParValue = list(globalParams.values())
	del artPar[-1]
	del artParValue[-1]
	finalParams = list(zip(artPar,artParValue))
	lParm = []
	for j in finalParams:
		lParm.append(' '.join(j))
	finalParm = ' '.join(lParm)
	for i in seqsSets:
		shCommands.write("art_illumina "+finalParm+" -i "+ i+" -f "+seqsSets[i][0]+" -o outDir"+str(seqsSets[i][1])+"_"+"\n")
def main(arguments):
	parser = argparse.ArgumentParser(description='This script will generate in silico shot gun sequencing data for a set of genomes with different levels of genome coverage', epilog='______')
	parser.add_argument('-f','--inputFasta',type=str, required=True,help="Location of fasta files and desired depth coverage")
	parser.add_argument('-p','--params',type=str, required=True,help="Global Parameters for ART Simulator")
	
	### parse arguments and convert to variables to use in script and functions
	args = parser.parse_args()

	fasta = args.inputFasta
	argsParams = args.params
	
	seqsSets = seqCommandSet(fasta)
	
	globalParams = addGlobalARTParams(argsParams)

	commandLineExecute = ARTcommandSet(seqsSets,globalParams)
	

if __name__=='__main__':
	main(sys.argv[1:])
