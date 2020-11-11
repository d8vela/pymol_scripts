import pymol
from pymol import cmd

def transform_by_camera_rotation():
     view = list(cmd.get_view())
     M = view[0:3] + [-view[12]] + \
         view[3:6] + [-view[13]] + \
         view[6:9] + [-view[14]] + \
         view[12:15] + [1.]
     cmd.transform_selection('(all)', M, transpose=1)
     cmd.set_view([1,0,0,0,1,0,0,0,1] + view[9:])
cmd.extend('transform_by_camera_rotation', transform_by_camera_rotation)