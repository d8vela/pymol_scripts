import pymol
import glob
from pymol import cmd

import sys,os

def resfile(file,color="red"):

	# Read Rosetta Resfile
	for line in open(file):
		
		# Split Resfile Line by Tab
		#data = line.split('\t')
		data = line.split()
		
		# Only Consider Lines that Start with Residue Numbers
		if data[0].isdigit():
			
			# Get Revalent Data
			pos = data[0]
			chain = data[1]
			mut = data[3]
			
			# Generate Mutation Label
			label = mut
			label_list = list(label)
			# First Amino Acid in List is Assumed Native
			# Insert Position Number After First Residue in the List
			label_list.insert(1,"%s"%(pos))
			label = ''.join(label_list)
			
			# PyMOL Color and Label
			cmd.color(color,"resi %s and chain %s"%(pos,chain))
			cmd.label("resi %s and chain %s and name CA"%(pos,chain),"\'%s\'"%(label))

			# Create Selections by Chain
			cmd.select("\'%s Chain %s\'"%(label,chain),"resi %s and chain %s and name CA"%(pos,chain))
			
		# Output Comments to the Console
		elif line[:1] == "#":
			# Remove newline feeds
			line.rstrip("\n")
			print "\n%s"%(line)

cmd.extend("resfile",resfile)

def series_resfile(color="orange"):

	# Main PDB File Name
	object = cmd.get_names()[0]
	counter = 0;

	# Read Rosetta Resfile
	for fname in glob.glob('*.resfile'):
		counter += 1;
		if counter == 1:
			fname_rem = fname

		cmd.copy(fname,object);
		for line in open(fname):
			
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
				cmd.color(color,"resi %s and chain %s and %s"%(pos,chain,fname))
				cmd.label("resi %s and chain %s and name ca and %s"%(pos,chain,fname),"\'%s\'"%(label))
			# Output Comments to the Console
			elif line[:1] == "#":
				# Remove newline feeds
				line.rstrip("\n")
				print "\n%s"%(line)

	cmd.disable('all');
	cmd.enable(fname_rem);
	cmd.orient
	cmd.set_key('pgup', move_up)
	cmd.set_key('pgdn', move_down)
	#cmd.set_key('up', move_up)
	#cmd.set_key('down', move_down)
	#cmd.set_key('left', move_up)
	#cmd.set_key('right', move_down)

cmd.extend("series_resfile",series_resfile)

def move_down():
	enabled_objs = cmd.get_names("objects",enabled_only=1)
	all_objs = cmd.get_names("objects",enabled_only=0)
	for obj in enabled_objs:
		cmd.disable(obj)
		last_obj=obj
		for i in range(0,len(all_objs)):
			if all_objs[i] == obj:
				if i+1 >= len(all_objs):
					cmd.enable( all_objs[0] )
				else:
					cmd.enable( all_objs[i+1] )
	cmd.orient
def move_up():
	enabled_objs = cmd.get_names("objects",enabled_only=1)
        all_objs = cmd.get_names("objects",enabled_only=0)
        for obj in enabled_objs:
                cmd.disable(obj)
                last_obj=obj
                for i in range(0,len(all_objs)):
                        if all_objs[i] == obj:
                                if i-1 < 0:
                                        cmd.enable( all_objs[-1] )
                                else:
                                        cmd.enable( all_objs[i-1] )

def switch():
	cmd.orient
	cmd.set_key('pgup', move_up)
	cmd.set_key('pgdn', move_down)
	#cmd.set_key('up', move_up)
	#cmd.set_key('down', move_down)
	#cmd.set_key('left', move_up)
	#cmd.set_key('right', move_down)

cmd.extend("switch",switch)

