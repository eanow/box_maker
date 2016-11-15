import sys
import math

LASER_KERF=0.1
MATERIAL_THICKNESS=3.2
#distance from center line; half of material thickness
MAT_BUFF=MATERIAL_THICKNESS/2
#extra size for lid in each direction
LID_BUFF=0.4
CONVERT_FACTOR=(90.0/25.4)
#CONVERT_FACTOR=1

LAYER_WIDTH=10.5
BASE_R=40

svg_header='''<svg
   width="1032"
   height="1032"
   id="svg4157"
   version="1.1">'''

svg_footer='''
</svg>'''

svg_path='''<path
       style="fill:none;stroke:#ff0000;stroke-width:1;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none"
       d="$pathCoords"
       id="$pathID"
       inkscape:connector-curvature="0" />'''
pathID=1001
fout=open('nonagon.svg','w')
fout.write(svg_header+'\n')


#create east-west interior bits
for jj in range(11):
    radius=jj*LAYER_WIDTH+BASE_R
    pathID=pathID+1
    #create 9 points around a circle
    angle=0
    circle=2*math.pi
    points=list()
    for ii in range(9):
        rad=circle*ii/9.0
        xx=145.6+math.cos(rad)*radius
        yy=145.6+math.sin(rad)*radius
        points.append((xx,yy))
    #pathstring
    pathString=''
    #start
    pathString=pathString+'M '+str(CONVERT_FACTOR*points[8][0])+' '+str(CONVERT_FACTOR*points[8][1])
    for point in points:
    #top right edge of notch
        pathString=pathString+' L '+str(CONVERT_FACTOR*point[0])+' '+str(CONVERT_FACTOR*point[1])
    #write path to SVG
    fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))

#############################################################3

fout.write(svg_footer)

fout.close()
