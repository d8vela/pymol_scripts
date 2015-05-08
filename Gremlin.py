import pymol
import glob
import re
from pymol import cmd

import sys,os

def gremlin(file,chain='B',score_th=1,inc='0',color="red"):

	count = 0
	pos1 = 0
	pos2 = 0
	pos1_rem = 0
	pos2_rem = 0
	pattern = re.compile('\_')

	# Read Gremlin File
	for line in open(file):
		
		# Split Resfile Line by Tab
		data = line.split(' ')
		
		# Only Consider Lines that have the Pattern
		pair = data[0]
		if pattern.search(pair):
			print pair
			contact = pair.split('_')
			pos1 = int(contact[0])
			pos2 = int(contact[1])
			aa = contact[2]

			if aa == 'X':
				score = data[1]

				if pos1 == pos1_rem:
					continue
				if pos2 == pos2_rem:
					continue
				pos1_rem = pos1
				pos2_rem = pos2

				pos1 += int(inc)
				pos2 += int(inc)

				if score >= score_th:
					cmd.distance("resi %i and name ca and chain %s"%(pos1,chain),"resi %i and name ca and chain %s"%(pos2,chain))
			
			# PyMOL Color and Label
			#cmd.label("resi %s+%s and chain %s and name ca"%(,chain),"\'%s\'"%(label))

cmd.extend("gremlin",gremlin)


