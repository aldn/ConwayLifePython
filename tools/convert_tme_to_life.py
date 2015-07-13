import sys

w = 0
h = 0

file = open(sys.argv[1])
nlines = 0
for line in file:
    if nlines == 1:
        commas = line.split(',')
        w = len(commas) - 1
    nlines = nlines + 1
h = nlines - 2
file.close()

print "%dx%d" % (w,h)

file = open(sys.argv[1])
y = 0
for line in file:
    line = line.rstrip()
    if line[0] == '{' and line[-1] == ',':
        strippedline = line[1:-2]
        values = strippedline.split(',')
        
        x = 0
        for v in values:
            if int(v) == 1:
                print '%d,%d' % (x,y)
            x = x + 1
        y = y + 1
        
file.close()