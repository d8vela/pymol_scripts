from .vecmat import *




a = Vec(34.155998, 66.834000, 0.232000  )
b = Vec(22.784122, 79.173546, -0.705234 )
c = Vec(21.641096, 67.769714, 11.566982 )

print((a-b).cross(a-c))
