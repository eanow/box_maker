import sys
#creates box for pathfinder
#assumptions:
#box is a square/rectangle, and sub-divided into bins by a set of panes that go across the box
#these panes can be (nearly) any length, and are always orthoganal
#when flat on table, sides of box are refered to as north, south, east, west
#interior panes use slots extending halfway, with panes running east to west going 'under' and north to south going over
#exterior panes are always over interior panes, and meet at the corner with a teeth pattern; north south exterior
#panes have an extended tooth on the top and east west an extended tooth on the bottom.
#Panes are specified as if they were 2-d planes, width of wood is set globally; panes should be specified to touch the center
#line of orthogonal panes. Appropriate extension will be added automatically
#laser kerf is set globally
#units are in mm, will be converted to SVG coordinates assuming 90 px to an inch and 25.4 mm to an inch.
#global settings
#0,0 is the upper left corner
#tabs will be 13 mm wide

LASER_KERF=0.1
MATERIAL_THICKNESS=3.2
#distance from center line; half of material thickness
MAT_BUFF=MATERIAL_THICKNESS/2
#extra size for lid in each direction
LID_BUFF=0.5
CONVERT_FACTOR=(90.0/25.4)
#CONVERT_FACTOR=1
TAB_WIDTH=13

if len(sys.argv)<3:
    print 'Usage: boxmaker.py [boxfile] [output]'
    
    
try:
    fin=open(sys.argv[1],'r')
    exec(fin.read())
except:
    print 'Error opening input file'
    quit()
try:
    fout=open(sys.argv[2],'w')
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

#create east-west interior bits
for panel in east_west:
    moniker=panel[0]
    print 'Creating',moniker,'Panel:'
    print 'Checking for crossing panels:'
    int_notches=list()
    ext_notches=list()
    tabs=list()
    num_tabs=0
    #check east panel
    if panel[1]<=0:
        print 'Panel crosses exterior panel at East edge'
        ext_notches.append(0)
    for item in north_south:
        #if x of north south is between beginning and end (inclusive) of east west panel, then we need a notch
        if item[1]>=panel[1] and item[1]<=panel[3] and panel[2]>=item[2] and panel[2]<=item[4]:
            print 'Panel crosses interior panel',item[0],'at',item[1]
            int_notches.append(item[1])
    #check west panel
    if panel[3]>=exterior_short:
        print 'Panel crosses exterior panel at West edge'
        ext_notches.append(exterior_short)
    #find tab locations
    size=panel[3]-panel[1]
    if size > exterior_short*.9:
        num_tabs=3
    elif size > TAB_WIDTH*2+30+10:
        num_tabs=2
    else:
        num_tabs=1
    print 'Attempting to position',num_tabs,'tabs on panel'
        #ideal placement (3) is middle, and 15 mm from each edge. If this crosses a notch, move tabs, if no position found, drop tab.
        #ideal placement (2) is .3, .7
        #ideal placement (1) is middle
    if num_tabs==1 or num_tabs==3:
        middle=((panel[3]-panel[1])/2)+panel[1]
        tab_edge=round(middle-(TAB_WIDTH/2)) #use whole units
        #since notches are on the top, we don't need to move tabs, technically.
        tabs.append(tab_edge)
    if num_tabs>1:
        tab_edge=round(panel[1]+15)
        tabs.append(tab_edge)
        tab_edge=round(panel[3]-(15+TAB_WIDTH))
        tabs.append(tab_edge)
    #create path
    pathID=pathID+1
    print 'Adding panel to svg'
    #actual part needs to account for material thickness, laser kerf, and then convert to the right coordinate system (pixels).
    #east/west have all notches the same; so we can combine our notch list
    full_notches=int_notches+ext_notches
    full_notches.sort()
    #first notch will start at the down position
    pathString=''
    #inside left edge of notch
    pathString=pathString+'M '+str(CONVERT_FACTOR*(full_notches[0]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
    #inside right edge of notch
    pathString=pathString+' L '+str(CONVERT_FACTOR*(full_notches[0]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
    #top right edge of notch
    pathString=pathString+' L '+str(CONVERT_FACTOR*(full_notches[0]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
    for notch in full_notches[1:-1]:
        #top left edge of notch
        pathString=pathString+' L '+str(CONVERT_FACTOR*(notch-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
        #bottom left edge of notch
        pathString=pathString+' L '+str(CONVERT_FACTOR*(notch-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
        #bottom right
        pathString=pathString+' L '+str(CONVERT_FACTOR*(notch+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
        #top right
        pathString=pathString+' L '+str(CONVERT_FACTOR*(notch+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
        
    #last notch
    
    #top left edge of notch
    pathString=pathString+' L '+str(CONVERT_FACTOR*(full_notches[-1]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
    #bottom left edge of notch
    pathString=pathString+' L '+str(CONVERT_FACTOR*(full_notches[-1]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
    #bottom right
    pathString=pathString+' L '+str(CONVERT_FACTOR*(full_notches[-1]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))

    #bottom right of panel
    pathString=pathString+' L '+str(CONVERT_FACTOR*(full_notches[-1]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(bin_height+LASER_KERF))
    tabs.sort()
    #tabs
    for tab in tabs[::-1]:
        #print tab
        #top right of tab
        pathString=pathString+' L '+str(CONVERT_FACTOR*(tab+TAB_WIDTH+LASER_KERF))+' '+str(CONVERT_FACTOR*(bin_height+LASER_KERF))
        #bottom right of tab
        pathString=pathString+' L '+str(CONVERT_FACTOR*(tab+TAB_WIDTH+LASER_KERF))+' '+str(CONVERT_FACTOR*(bin_height+MATERIAL_THICKNESS+LASER_KERF))
        #bottom left of tab
        pathString=pathString+' L '+str(CONVERT_FACTOR*(tab-LASER_KERF))+' '+str(CONVERT_FACTOR*(bin_height+MATERIAL_THICKNESS+LASER_KERF))
        #top left of tab
        pathString=pathString+' L '+str(CONVERT_FACTOR*(tab-LASER_KERF))+' '+str(CONVERT_FACTOR*(bin_height+LASER_KERF))
        #notch in base plate
        base_slots=base_slots+' M '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((tab)+LASER_KERF))
        base_slots=base_slots+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((tab)+LASER_KERF))
        base_slots=base_slots+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((tab+TAB_WIDTH)-LASER_KERF))
        base_slots=base_slots+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((tab+TAB_WIDTH)-LASER_KERF))
        base_slots=base_slots+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((tab)+LASER_KERF))
    #bottom right
    pathString=pathString+' L '+str(CONVERT_FACTOR*(full_notches[0]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(bin_height+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(full_notches[0]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
    #moniker
    fout.write('\n<g>')
    fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*(((panel[3]-panel[1])/2)+panel[1]))).replace('$yCoord',str(CONVERT_FACTOR*(bin_height/2))))
    fout.write(panel[0])
    fout.write('</text>')
    #write path to SVG
    fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
    fout.write('</g>')
#############################################################3
#create north-south interior bits
for panel in north_south:
    moniker=panel[0]
    print 'Creating',moniker,'Panel:'
    print 'Checking for crossing panels:'
    int_notches=list()
    ext_notches=list()
    tabs=list()
    num_tabs=0
    #check north panel
    if panel[2]<=0:
        print 'Panel crosses exterior panel at South edge'
        ext_notches.append(0)
    for item in east_west:
        #if x of north south is between beginning and end (inclusive) of east west panel, then we need a notch
        if item[2]>=panel[2] and item[2]<=panel[4] and panel[1]>=item[1] and panel[1]<=item[3]:
            print 'Panel crosses interior panel',item[0],'at',item[2]
            if item[2]==panel[2] or item[2]==panel[4]:
                #end
                print 'End notch'
            else:
                int_notches.append(item[2])
    int_notches.sort()
    #check west panel
    if panel[4]>=exterior_long:
        print 'Panel crosses exterior panel at North edge'
        ext_notches.append(exterior_long)
    #find tab locations
    size=panel[4]-panel[2]
    if size > exterior_long*.9:
        num_tabs=3
    elif size > TAB_WIDTH*2+30+10:
        num_tabs=2
    else:
        num_tabs=1
    print 'Attempting to position',num_tabs,'tabs on panel'
        #ideal placement (3) is middle, and 15 mm from each edge. If this crosses a notch, move tabs, if no position found, drop tab.
        #ideal placement (2) is .3, .7
        #ideal placement (1) is middle
    if num_tabs==1 or num_tabs==3:
        print 'finding spot for middle tab'
        middle=((panel[4]-panel[2])/2)+panel[2]
        tab_edge=round(middle-(TAB_WIDTH/2)) #use whole units
        #check if tab needs to be moved
        #use 5mm buffer
        blocked=False
        blocking_notch=-1
        for notch in int_notches:
            if (((notch-(.5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(.5+MAT_BUFF))>=(tab_edge))) or (((notch+(.5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(.5+MAT_BUFF))>=(tab_edge))):
            #tab overlaps, move it
                print 'initial tab location overlaps notch'
                blocked=True
                blocking_notch=notch
        if blocked:
            print 'Tab blocked, moving'
            tab_edge=blocking_notch+10
            blocked=False
            for notch in int_notches:
                if (((notch-(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(5+MAT_BUFF))>=(tab_edge))) or (((notch+(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(5+MAT_BUFF))>=(tab_edge))):
                #tab overlaps, move it
                    blocked=True
            if not blocked:
                print 'Tab Moved'
        #if it failed, try moving the other way
        if blocked:
            print 'Tab blocked, moving'
            tab_edge=blocking_notch-(10+TAB_WIDTH)
            blocked=False
            for notch in int_notches:
                if (((notch-(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(5+MAT_BUFF))>=(tab_edge))) or (((notch+(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(5+MAT_BUFF))>=(tab_edge))):
                #tab overlaps, move it
                    blocked=True
            if not blocked:
                print 'Tab Moved'
        if not blocked:
            tabs.append(tab_edge)
    if num_tabs>1:
    #going to assume these never block for now
        tab_edge=round(panel[2]+15)
        tabs.append(tab_edge)
        tab_edge=round(panel[4]-(15+TAB_WIDTH))
        tabs.append(tab_edge)
    tabs.sort()
    #create path
    pathID=pathID+1
    print 'Adding panel to svg'
    #actual part needs to account for material thickness, laser kerf, and then convert to the right coordinate system (pixels).

    pathString=''
    #upper left
    #these are interior, so if the start is lined up with the exterior, we need a notch on top
    if panel[2]==0:
        #start with top notch
        pathString=pathString+'M '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
    else:
        #notch will be on the bottom
        pathString=pathString+'M '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
    #top right
    if panel[4]==exterior_long:
        #print 'A'
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
        #bottom right
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
    else:
        #print 'B'
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
        #bottom right
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
    
    #notches and tabs
    cur_tab=len(tabs)-1
    cur_notch=len(int_notches)-1
    print 'Tabs and Notches:',cur_tab+1,cur_notch+1
    print tabs
    print int_notches
    while cur_tab>=0 or cur_notch>=0:
        #print 'Next Tab and Notch:',tabs[cur_tab],int_notches[cur_notch]
        todo=''
        if cur_tab==-1:
            #out of tabs
            todo='notch'
            #do a notch
        elif cur_notch==-1:
            #out of notches
            todo='tab'
            #do a tab
        elif tabs[cur_tab]>int_notches[cur_notch]:
            #tab is next
            todo='tab'
        else:
            todo='notch'
        if todo=='notch':
            #notch doing
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            
            
            cur_notch=cur_notch-1
        elif todo=='tab':
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height+MATERIAL_THICKNESS)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height+MATERIAL_THICKNESS)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            #notch in base plate#################
            base_slots=base_slots+' M '+str(CONVERT_FACTOR*(tabs[cur_tab]+LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF+LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH-LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF+LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH-LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF+LASER_KERF))
            cur_tab=cur_tab-1
        print 'Tabs and Notches:',cur_tab+1,cur_notch+1
    #final notch and close the path
    if panel[2]==0:
        #bottom left
        
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
        #notch
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
    else:
        #print 'Finish up'
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
        #print ' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
        #print ' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
        #print ' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
        pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
        
        
            
    #moniker
    fout.write('\n<g>')
    fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*(((panel[4]-panel[2])/2)+panel[2]))).replace('$yCoord',str(CONVERT_FACTOR*(bin_height/2))))
    fout.write(panel[0])
    fout.write('</text>')
    #write path to SVG
    fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
    fout.write('</g>')
    
#############################################################3
#create north-south exterior bits
for panel in [['WEST',0,0,0,exterior_long],['EAST',exterior_short,0,exterior_short,exterior_long]]:
    moniker='WEST'
    print 'Creating',moniker,'Panel:'
    print 'Checking for crossing panels:'
    int_notches=list()
    ext_notches=list()
    tabs=list()
    num_tabs=0
    #check north panel

    for item in east_west:
        #if x of north south is between beginning and end (inclusive) of east west panel, then we need a notch
        if item[2]>=panel[2] and item[2]<=panel[4] and panel[1]>=item[1] and panel[1]<=item[3]:
            print 'Panel crosses interior panel',item[0],'at',item[2]
            int_notches.append(item[2])
    int_notches.sort()
    #check west panel
    #find tab locations
    size=panel[4]-panel[2]
    if size > exterior_long*.9:
        num_tabs=3
    elif size > TAB_WIDTH*2+30+10:
        num_tabs=2
    else:
        num_tabs=1
    print 'Attempting to position',num_tabs,'tabs on panel'
        #ideal placement (3) is middle, and 15 mm from each edge. If this crosses a notch, move tabs, if no position found, drop tab.
        #ideal placement (2) is .3, .7
        #ideal placement (1) is middle
    if num_tabs==1 or num_tabs==3:
        print 'finding spot for middle tab'
        middle=((panel[4]-panel[2])/2)+panel[2]
        tab_edge=round(middle-(TAB_WIDTH/2)) #use whole units
        #check if tab needs to be moved
        #use 5mm buffer
        blocked=False
        blocking_notch=-1
        for notch in int_notches:
            if (((notch-(.5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(.5+MAT_BUFF))>=(tab_edge))) or (((notch+(.5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(.5+MAT_BUFF))>=(tab_edge))):
            #tab overlaps, move it
                print 'initial tab location overlaps notch'
                blocked=True
                blocking_notch=notch
        if blocked:
            print 'Tab blocked, moving'
            tab_edge=blocking_notch+10
            blocked=False
            for notch in int_notches:
                if (((notch-(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(5+MAT_BUFF))>=(tab_edge))) or (((notch+(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(5+MAT_BUFF))>=(tab_edge))):
                #tab overlaps, move it
                    blocked=True
            if not blocked:
                print 'Tab Moved'
        #if it failed, try moving the other way
        if blocked:
            print 'Tab blocked, moving'
            tab_edge=blocking_notch-(10+TAB_WIDTH)
            blocked=False
            for notch in int_notches:
                if (((notch-(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(5+MAT_BUFF))>=(tab_edge))) or (((notch+(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(5+MAT_BUFF))>=(tab_edge))):
                #tab overlaps, move it
                    blocked=True
            if not blocked:
                print 'Tab Moved'
        if not blocked:
            tabs.append(tab_edge)
    if num_tabs>1:
    #going to assume these never block for now
        tab_edge=round(panel[2]+15)
        tabs.append(tab_edge)
        tab_edge=round(panel[4]-(15+TAB_WIDTH))
        tabs.append(tab_edge)
    tabs.sort()
    #create path
    pathID=pathID+1
    print 'Adding panel to svg'
    #actual part needs to account for material thickness, laser kerf, and then convert to the right coordinate system (pixels).

    pathString=''
    #upper left


    #teeth
    pathString=pathString+'M '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/4.0)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/4.0)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[4]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
    
    #notches and tabs
    cur_tab=len(tabs)-1
    cur_notch=len(int_notches)-1
    print 'Tabs and Notches:',cur_tab+1,cur_notch+1
    print tabs
    print int_notches
    while cur_tab>=0 or cur_notch>=0:
        #print 'Next Tab and Notch:',tabs[cur_tab],int_notches[cur_notch]
        todo=''
        if cur_tab==-1:
            #out of tabs
            todo='notch'
            #do a notch
        elif cur_notch==-1:
            #out of notches
            todo='tab'
            #do a tab
        elif tabs[cur_tab]>int_notches[cur_notch]:
            #tab is next
            todo='tab'
        else:
            todo='notch'
        if todo=='notch':
            #notch doing
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            
            cur_notch=cur_notch-1
        elif todo=='tab':
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height+MATERIAL_THICKNESS)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height+MATERIAL_THICKNESS)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            #notch in base plate#################
            base_slots=base_slots+' M '+str(CONVERT_FACTOR*(tabs[cur_tab]+LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF+LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH-LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF+LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH-LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+LASER_KERF))+' '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF+LASER_KERF))
            cur_tab=cur_tab-1
        print 'Tabs and Notches:',cur_tab+1,cur_notch+1
    #teeth and close the path
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
        
        
            
    #moniker
    fout.write('\n<g>')
    fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*(((panel[4]-panel[2])/2)+panel[2]))).replace('$yCoord',str(CONVERT_FACTOR*(bin_height/2))))
    fout.write(panel[0])
    fout.write('</text>')
    #write path to SVG
    fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
    fout.write('</g>')

#############################################################3
#create east-west exterior bits
for panel in [['SOUTH',0,0,exterior_short,0],['NORTH',0,exterior_long,exterior_short,exterior_long]]:
    moniker='WEST'
    print 'Creating',moniker,'Panel:'
    print 'Checking for crossing panels:'
    int_notches=list()
    ext_notches=list()
    tabs=list()
    num_tabs=0
    #check north panel

    for item in north_south:
        #if x of north south is between beginning and end (inclusive) of east west panel, then we need a notch
        if item[1]>=panel[1] and item[1]<=panel[3] and panel[2]>=item[2] and panel[2]<=item[4]:
            print 'Panel crosses interior panel',item[0],'at',item[1]
            int_notches.append(item[1])
    int_notches.sort()
    #check west panel
    #find tab locations
    size=panel[3]-panel[1]
    if size > exterior_short*.9:
        num_tabs=3
    elif size > TAB_WIDTH*2+30+10:
        num_tabs=2
    else:
        num_tabs=1
    print 'Attempting to position',num_tabs,'tabs on panel'
        #ideal placement (3) is middle, and 15 mm from each edge. If this crosses a notch, move tabs, if no position found, drop tab.
        #ideal placement (2) is .3, .7
        #ideal placement (1) is middle
    if num_tabs==1 or num_tabs==3:
        print 'finding spot for middle tab'
        middle=((panel[3]-panel[1])/2)+panel[1]
        tab_edge=round(middle-(TAB_WIDTH/2)) #use whole units
        #check if tab needs to be moved
        #use 5mm buffer
        blocked=False
        blocking_notch=-1
        for notch in int_notches:
            if (((notch-(.5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(.5+MAT_BUFF))>=(tab_edge))) or (((notch+(.5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(.5+MAT_BUFF))>=(tab_edge))):
            #tab overlaps, move it
                print 'initial tab location overlaps notch'
                blocked=True
                blocking_notch=notch
        if blocked:
            print 'Tab blocked, moving'
            tab_edge=blocking_notch+10
            blocked=False
            for notch in int_notches:
                if (((notch-(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(5+MAT_BUFF))>=(tab_edge))) or (((notch+(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(5+MAT_BUFF))>=(tab_edge))):
                #tab overlaps, move it
                    blocked=True
            if not blocked:
                print 'Tab Moved'
        #if it failed, try moving the other way
        if blocked:
            print 'Tab blocked, moving'
            tab_edge=blocking_notch-(10+TAB_WIDTH)
            blocked=False
            for notch in int_notches:
                if (((notch-(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch-(5+MAT_BUFF))>=(tab_edge))) or (((notch+(5+MAT_BUFF))<=(tab_edge+TAB_WIDTH)) and ((notch+(5+MAT_BUFF))>=(tab_edge))):
                #tab overlaps, move it
                    blocked=True
            if not blocked:
                print 'Tab Moved'
        if not blocked:
            tabs.append(tab_edge)
    if num_tabs>1:
    #going to assume these never block for now
        tab_edge=round(panel[1]+15)
        tabs.append(tab_edge)
        tab_edge=round(panel[3]-(15+TAB_WIDTH))
        tabs.append(tab_edge)
    tabs.sort()
    #create path
    pathID=pathID+1
    print 'Adding panel to svg'
    #actual part needs to account for material thickness, laser kerf, and then convert to the right coordinate system (pixels).

    pathString=''
    #upper left
    #these are interior, so if the start is lined up with the exterior, we need a notch on top

    #teeth notch
    pathString=pathString+'M '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[3]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[3]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[3]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[3]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[3]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[3]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[3]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[3]+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
    
    #notches and tabs
    cur_tab=len(tabs)-1
    cur_notch=len(int_notches)-1
    print 'Tabs and Notches:',cur_tab+1,cur_notch+1
    print tabs
    print int_notches
    while cur_tab>=0 or cur_notch>=0:
        #print 'Next Tab and Notch:',tabs[cur_tab],int_notches[cur_notch]
        todo=''
        if cur_tab==-1:
            #out of tabs
            todo='notch'
            #do a notch
        elif cur_notch==-1:
            #out of notches
            todo='tab'
            #do a tab
        elif tabs[cur_tab]>int_notches[cur_notch]:
            #tab is next
            todo='tab'
        else:
            todo='notch'
        if todo=='notch':
            #notch doing
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height/2.0)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(int_notches[cur_notch]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            cur_notch=cur_notch-1

        elif todo=='tab':
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]+TAB_WIDTH+LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height+MATERIAL_THICKNESS)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height+MATERIAL_THICKNESS)+LASER_KERF))
            pathString=pathString+' L '+str(CONVERT_FACTOR*(tabs[cur_tab]-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
            #notch in base plate#########
            base_slots=base_slots+' M '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((tabs[cur_tab])+LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((tabs[cur_tab])+LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(panel[2]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((tabs[cur_tab]+TAB_WIDTH)-LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((tabs[cur_tab]+TAB_WIDTH)-LASER_KERF))
            base_slots=base_slots+' L '+str(CONVERT_FACTOR*(panel[2]-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((tabs[cur_tab])+LASER_KERF))
            

            cur_tab=cur_tab-1
        print 'Tabs and Notches:',cur_tab+1,cur_notch+1
    #final teeth and close the path

    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*bin_height)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[1]-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*bin_height)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(panel[1]+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((0)-LASER_KERF))
    
    #moniker
    fout.write('\n<g>')
    fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*(((panel[3]-panel[1])/2)+panel[1]))).replace('$yCoord',str(CONVERT_FACTOR*(bin_height/2))))
    fout.write(panel[0])
    fout.write('</text>')
    #write path to SVG
    fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
    fout.write('</g>')
    
#base plate
pathID=pathID+1
fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*exterior_long/2.0)).replace('$yCoord',str(CONVERT_FACTOR*exterior_short/2.0)))
fout.write('Base Plate')
fout.write('</text>')
#write path to SVG
pathString='M '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(exterior_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(exterior_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(exterior_short+MAT_BUFF+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(exterior_short+MAT_BUFF+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))
fout.write(svg_path.replace('$pathCoords',pathString+base_slots).replace('$pathID',str(pathID)))
fout.write('</g>')

#################Lid
lid_long=exterior_long+2*MATERIAL_THICKNESS+2*LID_BUFF
lid_short=exterior_short+2*MATERIAL_THICKNESS+2*LID_BUFF
long_teeth=int(round((lid_long-20)/40.0))
print 'Generating ',long_teeth,' Teeth on long side'
short_teeth=int(round((lid_short-20)/40.0))
print 'Generating ',short_teeth,' Teeth on short side'
long_tooth=lid_long/(2*long_teeth+1)
short_tooth=lid_short/(2*short_teeth+1)
#top left
pathString='M '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))
for ii in xrange(0,long_teeth):
    pathString=pathString+' L '+str(CONVERT_FACTOR*(long_tooth*(ii*2+1)+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(long_tooth*(ii*2+1)+LASER_KERF))+' '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(long_tooth*(ii*2+2)-LASER_KERF))+' '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(long_tooth*(ii*2+2)-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))
#Top Right
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))
for ii in xrange(0,short_teeth):
    pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(short_tooth*(ii*2+1)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(short_tooth*(ii*2+1)+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(short_tooth*(ii*2+2)-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(short_tooth*(ii*2+2)-LASER_KERF))
#bottom Right 
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short+MAT_BUFF+LASER_KERF))
for ii in xrange(0,long_teeth):
    pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-(long_tooth*(ii*2+1))-LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short+MAT_BUFF+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-(long_tooth*(ii*2+1))-LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short-MAT_BUFF+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-(long_tooth*(ii*2+2))+LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short-MAT_BUFF+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-(long_tooth*(ii*2+2))+LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short+MAT_BUFF+LASER_KERF))
#bottom left
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short+MAT_BUFF+LASER_KERF))
for ii in xrange(0,short_teeth):
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short-(short_tooth*(ii*2+1))-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short-(short_tooth*(ii*2+1))-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short-(short_tooth*(ii*2+2))+LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(lid_short-(short_tooth*(ii*2+2))+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))

#lid plate
pathID=pathID+1
fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*exterior_long/2.0)).replace('$yCoord',str(CONVERT_FACTOR*exterior_short/2.0)))
fout.write('Lid')
fout.write('</text>')
#write path to SVG
fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
fout.write('</g>')

#################Lid long side
#height of side
side_height=bin_height+MATERIAL_THICKNESS+.8
#.8 from felt liner
#top left
pathString='M '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
for ii in xrange(0,long_teeth):
    pathString=pathString+' L '+str(CONVERT_FACTOR*(long_tooth*(ii*2+1)-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(long_tooth*(ii*2+1)-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MATERIAL_THICKNESS-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(long_tooth*(ii*2+2)+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MATERIAL_THICKNESS-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(long_tooth*(ii*2+2)+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
#Top Right
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
#sides teeth
#teeth notch

pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*side_height)+LASER_KERF))

#bottom right
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_long-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(side_height+LASER_KERF))
#grab slot
pathString=pathString+' L '+str(CONVERT_FACTOR*(26.0+(lid_long/2.0)-LASER_KERF))+' '+str(CONVERT_FACTOR*(side_height+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(26.0+(lid_long/2.0)-LASER_KERF))+' '+str(CONVERT_FACTOR*((side_height/2)+5.0+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(21.0+(lid_long/2.0)-LASER_KERF))+' '+str(CONVERT_FACTOR*((side_height/2)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*((lid_long/2.0)-21.0-LASER_KERF))+' '+str(CONVERT_FACTOR*((side_height/2)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*((lid_long/2.0)-26.0-LASER_KERF))+' '+str(CONVERT_FACTOR*((side_height/2)+5.0+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*((lid_long/2.0)-26.0-LASER_KERF))+' '+str(CONVERT_FACTOR*(side_height+LASER_KERF))
#bottom left
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(side_height+LASER_KERF))
#teeth notch
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*side_height)+LASER_KERF))
#close
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))

#lid side
pathID=pathID+1
fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*lid_long/2.0)).replace('$yCoord',str(CONVERT_FACTOR*side_height/2.0)))
fout.write('West Lid')
fout.write('</text>')
#write path to SVG
fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
fout.write('</g>')

#lid side
pathID=pathID+1
fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*lid_long/2.0)).replace('$yCoord',str(CONVERT_FACTOR*side_height/2.0)))
fout.write('East Lid')
fout.write('</text>')
#write path to SVG
fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
fout.write('</g>')

#################Lid short side

#top left
pathString='M '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
for ii in xrange(0,short_teeth):
    pathString=pathString+' L '+str(CONVERT_FACTOR*(short_tooth*(ii*2+1)-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(short_tooth*(ii*2+1)-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MATERIAL_THICKNESS-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(short_tooth*(ii*2+2)+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-MATERIAL_THICKNESS-LASER_KERF))
    pathString=pathString+' L '+str(CONVERT_FACTOR*(short_tooth*(ii*2+2)+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
#Top Right
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_short-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))
#sides teeth
#teeth notch

pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_short-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_short+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_short+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_short-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_short-MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_short+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*side_height)-LASER_KERF))

#bottom right
pathString=pathString+' L '+str(CONVERT_FACTOR*(lid_short+MAT_BUFF+LASER_KERF))+' '+str(CONVERT_FACTOR*(side_height+LASER_KERF))

#bottom left
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(side_height+LASER_KERF))
#teeth notch
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.75*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.5*side_height)+LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0-MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*side_height)-LASER_KERF))
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*((.25*side_height)-LASER_KERF))
#close
pathString=pathString+' L '+str(CONVERT_FACTOR*(0+MAT_BUFF-LASER_KERF))+' '+str(CONVERT_FACTOR*(0-LASER_KERF))

#lid side
pathID=pathID+1
fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*lid_short/2.0)).replace('$yCoord',str(CONVERT_FACTOR*side_height/2.0)))
fout.write('North Lid')
fout.write('</text>')
#write path to SVG
fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
fout.write('</g>')

#lid side
pathID=pathID+1
fout.write('\n<g>')
fout.write(svg_text.replace('$xCoord',str(CONVERT_FACTOR*lid_short/2.0)).replace('$yCoord',str(CONVERT_FACTOR*side_height/2.0)))
fout.write('South Lid')
fout.write('</text>')
#write path to SVG
fout.write(svg_path.replace('$pathCoords',pathString).replace('$pathID',str(pathID)))
fout.write('</g>')


fout.write(svg_footer)
fin.close()
fout.close()
