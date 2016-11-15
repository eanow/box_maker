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

LAYER_WIDTH=17
SIDE=40


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
fout=open('8star.svg','w')
fout.write(svg_header+'\n')


#create east-west interior bits
for jj in range(11):
    this_side=SIDE+jj*LAYER_WIDTH
    cc=this_side/(1+(2/math.sqrt(2)))
    radius2=cc/(math.sqrt(2-math.sqrt(2)))
    radius1=math.sqrt(2)*this_side/2
    pathID=pathID+1
    #create 9 points around a circle
    angle=0
    circle=2*math.pi
    points=list()
    for ii in range(8):
        rad1=(ii*circle/8.0)-circle/16.0
        rad2=(ii*circle/8.0)
        xx=145.6+math.cos(rad1)*radius1
        yy=145.6+math.sin(rad1)*radius1
        points.append((xx,yy))
        xx=145.6+math.cos(rad2)*radius2
        yy=145.6+math.sin(rad2)*radius2
        points.append((xx,yy))

    #pathstring
    pathString=''
    #start
    pathString=pathString+'M '+str(CONVERT_FACTOR*points[-1][0])+' '+str(CONVERT_FACTOR*points[-1][1])
    for point in points:
    #top right edge of notch
        pathString=pathString+' L '+str(CONVERT_FACTOR*point[0])+' '+str(CONVERT_FACTOR*point[1])
    #write path to SVG
    fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))

#############################################################3

fout.write(svg_footer)

fout.close()
