'''

Export PyMOL selection and import as PyRosetta Pose

'''
 
import pymol
from pymol import cmd

import os

def pdb2pose():
	from rosetta import *
	from pyrosetta import *
	init()

	# Export sele object to PDB file in the temp path
	cmd.save('.pose.pdb','sele')

	# Import Rosetta Pose from PDB file
	pose = Pose()
	pose.assign(pose)
	pose_from_file(pose,'.pose.pdb')

	return pose

cmd.extend("pdb2pose", pdb2pose)

def NetCharge():
	from rosetta import *
	from pyrosetta import *
	init()
	
	pose = pdb2pose()
	net_charge = protocols.simple_filters.NetChargeFilter()
	nc = net_charge.compute(pose)
	print 'Net Charge: ' ,  nc 

cmd.extend("NetCharge", NetCharge)

def OversaturatedHbondAcceptor():
	from rosetta import *
	from pyrosetta import *
	init()

	pose = pdb2pose()
	over_sat = protocols.cyclic_peptide.OversaturatedHbondAcceptorFilter()

	# Get Number of Atoms Not Passing the Filter
	atom_count = over_sat.report_sm(pose)
	print 'OversaturatedHbondAcceptor: ' , atom_count

cmd.extend("OversaturatedHbondAcceptor", OversaturatedHbondAcceptor)

def Ddg():
	from rosetta import *
	from pyrosetta import *
	init()

	pose = pdb2pose()
	#filt = protocols.simple_filters.DdgFilter()

	# Get ddG
	full_scorefxn = create_score_function('talaris2013')

	# Bound
	dG_bound = full_scorefxn(pose)

	# Unbound
	translate = protocols.rigid.RigidBodyTransMover(pose,1)
	translate.step_size(1000)
	translate.apply(pose)
	dG_unbound = full_scorefxn(pose)

	# Get ddG
	print 'Unbound Total Energy (dG): ', dG_unbound
	print 'Bound Total Energy (dG): ', dG_bound
	print 'Interface Energy (ddG): ' , dG_unbound - dG_bound

cmd.extend("Ddg", Ddg)

def ShapeComplementarity():
	from rosetta import *
	from pyrosetta import *
	init()

	pose = pdb2pose()
	filt = protocols.simple_filters.ShapeComplementarityFilter()

	# Get Number of Atoms Not Passing the Filter
	sc = filt.report_sm(pose)
	print 'ShapeComplementarity: ' , sc

cmd.extend("ShapeComplementarity", ShapeComplementarity)

def InterfaceSasa():
	from rosetta import *
	from pyrosetta import *
	init()

	pose = pdb2pose()
	#filt = protocols.simple_filters.InterfaceSasaFilter()

	# Get Interface SASA
	sasa = core.scoring.sasa.SasaCalc()

	# Bound
	area_bound = sasa.calculate(pose)

	# Unbound
	translate = protocols.rigid.RigidBodyTransMover(pose,1)
	translate.step_size(1000)
	translate.apply(pose)
	area_unbound = sasa.calculate(pose)

	print 'Unbound SASA: ', area_unbound
	print 'Bound SASA: ', area_bound
	print 'Interface SASA: ' , area_unbound - area_bound

cmd.extend("InterfaceSasa", InterfaceSasa)

def TotalSasa():
	from rosetta import *
	from pyrosetta import *
	init()

	pose = pdb2pose()
	#filt = protocols.simple_filters.TotalSasaFilter()

	# Get SASA
	sasa = core.scoring.sasa.SasaCalc()
	area = sasa.calculate(pose)
	print 'TotalSasa: ' , area

	# Visualize in PyMOL
	cmd.hide("surface");
	cmd.show("surface","sele");


cmd.extend("TotalSasa", TotalSasa)


