import sys
#creates dice tower
#assumptions:
#0,0 is the upper left corner
#tabs will be 13 mm wide

LASER_KERF=0.1
MATERIAL_THICKNESS=3.2
#distance from center line; half of material thickness
MAT_BUFF=MATERIAL_THICKNESS/2
#extra size for lid in each direction
LID_BUFF=0.4
CONVERT_FACTOR=(90.0/25.4)
#CONVERT_FACTOR=1
TAB_WIDTH=13

TOWER_HEIGHT=200
TOWER_DEPTH=80
TOWER_WIDTH=100
OPEN_HEIGHT=50


try:
    fout=open('dice_tower.svg','w')
except:
    print 'Error opening output file'
    quit()

svg_header='''<svg
   width="2111.811"
   height="1031.1023"
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

svg_text='''<text
       y="$yCoord"
       x="$xCoord"
       style="font-size:40px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#00ff00;fill-opacity:1;stroke:none;font-family:Sans">'''

fout.write(svg_header+'\n')

base_slots=''
#aim for 20mm tabs
face_h=(TOWER_HEIGHT-OPEN_HEIGHT)
half_f_tabs=int(round((face_h-20)/40.0))
face_tab_w=(1.0*face_h)/(half_f_tabs*2+1)
#main tower, face
#roughly a rectangle, TOWER_HEIGHT-OPEN_HEIGHT x TOWER_WIDTH
moniker='face'
print 'Creating',moniker,'Panel:'

#create path
pathID=pathID+1
print 'Adding face panel to svg'
#actual part needs to account for material thickness, laser kerf, and then convert to the right coordinate system (pixels).
#east/west have all notches the same; so we can combine our notch list
#start at upper left corner
pathString=''
pathString=pathString+'M '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
#upper right
pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
print half_f_tabs
for ii in range(half_f_tabs):
    #out_down
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+1)*face_tab_w+LASER_KERF))
    #out_in    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+1)*face_tab_w+LASER_KERF))
    #in_down    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+2)*face_tab_w-LASER_KERF))
    #in_out
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+2)*face_tab_w-LASER_KERF))
#final bit
pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h+LASER_KERF))
#bottom left
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h+LASER_KERF))
for ii in range(half_f_tabs):
    #out_up
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h-((2*ii+1)*face_tab_w)-LASER_KERF))
    #out_in    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h-((2*ii+1)*face_tab_w)-LASER_KERF))
    #in_up   
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h-((2*ii+2)*face_tab_w)+LASER_KERF))
    #in_out
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h-((2*ii+2)*face_tab_w)+LASER_KERF))
#close it
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))

fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*(TOWER_WIDTH/2))).replace('$yCoord',str(CONVERT_FACTOR*face_h/2)))
fout.write(moniker)
fout.write('</text>')
#write path to SVG
fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
fout.write('</g>')
##############################################################
#aim for 20mm tabs
back_h=(TOWER_HEIGHT)
half_b_tabs=int(round((back_h-20)/40.0))
back_tab_w=(1.0*back_h)/(half_b_tabs*2+1)
#main tower, back
#roughly a rectangle, TOWER_HEIGHT x TOWER_WIDTH
moniker='back'
print 'Creating',moniker,'Panel:'

#create path
pathID=pathID+1
print 'Adding back panel to svg'
#actual part needs to account for material thickness, laser kerf, and then convert to the right coordinate system (pixels).
#east/west have all notches the same; so we can combine our notch list
#start at upper left corner
pathString=''
pathString=pathString+'M '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
#upper right
pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
print half_b_tabs
for ii in range(half_b_tabs):
    #out_down
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+1)*back_tab_w+LASER_KERF))
    #out_in    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+1)*back_tab_w+LASER_KERF))
    #in_down    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+2)*back_tab_w-LASER_KERF))
    #in_out
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+2)*back_tab_w-LASER_KERF))
#final bit
pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_WIDTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(back_h+LASER_KERF))
#bottom left
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(back_h+LASER_KERF))
for ii in range(half_b_tabs):
    #out_up
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(back_h-((2*ii+1)*back_tab_w)-LASER_KERF))
    #out_in    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(back_h-((2*ii+1)*back_tab_w)-LASER_KERF))
    #in_up   
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(back_h-((2*ii+2)*back_tab_w)+LASER_KERF))
    #in_out
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(back_h-((2*ii+2)*back_tab_w)+LASER_KERF))
#close it
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))

fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*(TOWER_WIDTH/2))).replace('$yCoord',str(CONVERT_FACTOR*back_h/2)))
fout.write(moniker)
fout.write('</text>')
#write path to SVG
fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
fout.write('</g>')
############################################################
#side
#left side front, right side back
back_h=(TOWER_HEIGHT)
half_b_tabs=int(round((back_h-20)/40.0))
back_tab_w=(1.0*back_h)/(half_b_tabs*2+1)
#main tower, back
#roughly a rectangle, TOWER_HEIGHT x TOWER_DEPTH
moniker='side'
print 'Creating',moniker,'Panel:'

#create path
pathID=pathID+1
print 'Adding back panel to svg'
#actual part needs to account for material thickness, laser kerf, and then convert to the right coordinate system (pixels).
#east/west have all notches the same; so we can combine our notch list
#start at upper left corner
pathString=''
pathString=pathString+'M '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
#upper right
pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_DEPTH-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
print half_b_tabs
for ii in range(half_b_tabs):
    #out_down
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_DEPTH-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+1)*back_tab_w-LASER_KERF))
    #out_in    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_DEPTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+1)*back_tab_w-LASER_KERF))
    #in_down    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_DEPTH+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+2)*back_tab_w+LASER_KERF))
    #in_out
    pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_DEPTH-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((2*ii+2)*back_tab_w+LASER_KERF))
#final bit
pathString=pathString+' L '+str(CONVERT_FACTOR*(TOWER_DEPTH-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(back_h+LASER_KERF))
#bottom left
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(back_h+LASER_KERF))
#stick forward
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h+LASER_KERF))
for ii in range(half_f_tabs):
    #out_up
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h-((2*ii+1)*face_tab_w)+LASER_KERF))
    #out_in    
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h-((2*ii+1)*face_tab_w)+LASER_KERF))
    #in_up   
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h-((2*ii+2)*face_tab_w)-LASER_KERF))
    #in_out
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(face_h-((2*ii+2)*face_tab_w)-LASER_KERF))
#close it
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))


fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*(TOWER_DEPTH/2))).replace('$yCoord',str(CONVERT_FACTOR*back_h/2)))
fout.write(moniker)
fout.write('</text>')
#write path to SVG
fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
fout.write('</g>')
############################################################

fout.write(svg_footer)

fout.close()
