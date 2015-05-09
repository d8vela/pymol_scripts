import pymol
import glob
import re
from pymol import cmd

import sys,os

def gremlin(file,chain='B',s_score_th=1.5,prob_th=1,inc='0',color="red"):

	count = 0
	pos1 = 0
	pos2 = 0
	pos1_rem = 0
	pos2_rem = 0
	pattern = re.compile('\_')

	# Initial Parameters
	cmd.set("dash_gap","0")
	cmd.set("dash_color","green")
	cmd.set("dash_width","6") # max is 6

	# Read Gremlin File
	for line in open(file):
		
		# Split Resfile Line by Tab
		data = line.split(' ')
		
		# Only Consider Lines that have the Pattern
		pair = data[0]
		if pattern.search(pair):
#print pair
			contact = pair.split('_')
			pos1 = int(contact[0])
			pos2 = int(contact[1])
			aa = contact[2]

			if aa == 'X':
				l2_score = float(data[1])
				s_score = float(data[2])
				prob = float(data[3])
				print prob

				if pos1 == pos1_rem:
					continue
				if pos2 == pos2_rem:
					continue
				if abs(pos1-pos2) <= 3:
					continue
				pos1_rem = pos1
				pos2_rem = pos2

				pos1 += int(inc)
				pos2 += int(inc)

				if prob >= float(prob_th) and s_score >= float(s_score_th):
					dist = cmd.distance("%s"%(pair),"resi %i and name ca and chain %s"%(pos1,chain),"resi %i and name ca and chain %s"%(pos2,chain))
					if dist <= 12:
						cmd.set("dash_color","yellow","%s"%(pair))
					if dist > 12 and dist <= 20:
						cmd.set("dash_color","orange","%s"%(pair))
					if dist > 20:
						cmd.set("dash_color","red","%s"%(pair))
			
			# PyMOL Color and Label
			#cmd.label("resi %s+%s and chain %s and name ca"%(,chain),"\'%s\'"%(label))

cmd.extend("gremlin",gremlin)


