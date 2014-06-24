import pymol
from pymol import cmd

import sys,os

def resfile(file,color="red"):

	# Read Rosetta Resfile
	for line in open(file):
		
		# Split Resfile Line by Tab
		data = line.split('\t')
		
		# Only Consider Lines that Start with Residue Numbers
		if data[0].isdigit():
			
			# Get Revalent Data
			pos = data[0]
			chain = data[1]
			mut = data[3]
			
			# Generate Mutation Label
			label = mut
			label_list = list(label)
			label_list.insert(1,"%s"%(pos))
			label = ''.join(label_list)
			
			# PyMOL Color and Label
			cmd.color(color,"resi %s and chain %s"%(pos,chain))
			cmd.label("resi %s and chain %s and name ca"%(pos,chain),"\'%s\'"%(label))
		# Output Comments to the Console
		elif line[:1] == "#":
			# Remove newline feeds
			line.rstrip("\n")
			print "\n%s"%(line)

cmd.extend("resfile",resfile)


