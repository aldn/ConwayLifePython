import sys
import os
import re

f = open(sys.argv[1], 'r')
header = f.readline().rstrip()
match = re.search('(\d+)x(\d+)', header)
(w,h) = match.groups()
(field_width,field_height) = (int(w), int(h))
#print 'Width=%d  Height=%d' % (field_width,field_height)
if field_width != 16 or field_height != 16:
	exit()
match = re.search('\+(\d+)\+(\d+)', header)
if match:
	offset = (int(match.groups()[0]),int(match.groups()[1]))
else:
	offset = (0,0)
	
words = [0]*(16)
	
for line in f:
	coord_tuples = line.rstrip().split()
	for coord_str in coord_tuples:
		[x,y] = coord_str.split(',')
		coord = (int(x),int(y))
		#print coord[0]+offset[0], coord[1]+offset[1]
		words[coord[1]+offset[1]]  = words[coord[1]+offset[1]] |  1 << (15- (coord[0]+offset[0]))
		



hex_words = []
for word in words:
	hex_words.append( "0x%.4x" % word)
	
print  "const unsigned __int16 life_pattern_%s[] =  {" % os.path.basename(sys.argv[1]).replace(".life",""),  ', '.join(hex_words), "};"
