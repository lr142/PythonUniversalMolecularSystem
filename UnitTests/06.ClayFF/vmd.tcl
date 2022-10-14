color	Element	C	gray
color	Element	Al	magenta
color	Element	Si	orange
color	Element	Mg	green
color	Element	Na	blue
#display cuedensity 0.0
display projection Orthographic
menu main on
mol modstyle 0 0 Licorice 0.300000 12.000000 12.000000
mol color Name
mol representation Licorice 0.300000 12.000000 12.000000
mol selection all
mol material Opaque
mol modrep 0 0
color Display Background white
mol new dump.mol2 autobonds off
set sel [atomselect top all]
$sel set element [$sel get type]
mol modcolor 0 0 Element
lassign [molinfo top get numatoms] NAtoms
if {$NAtoms < 1000} {;mol modstyle top 0 Licorice;} else {mol modstyle top 0 Lines}
color Labels Atoms black
color Labels Bonds black
color Labels Angles black
color Labels Dihedrals black
label textthickness 3.6
label textsize 1.0
label textthickness 1.5
label textsize 1.0
label add Atoms 0/0
label textoffset Atoms 0 { 0.01 0.01 0.5 }
label textformat Atoms 0 { 1:H2-C= }
label add Atoms 0/1
label textoffset Atoms 1 { 0.01 0.01 0.5 }
label textformat Atoms 1 { 2:RH-C= }
label add Atoms 0/2
label textoffset Atoms 2 { 0.01 0.01 0.5 }
label textformat Atoms 2 { 3:177 }
label add Atoms 0/3
label textoffset Atoms 3 { 0.01 0.01 0.5 }
label textformat Atoms 3 { 4:178 }
label add Atoms 0/4
label textoffset Atoms 4 { 0.01 0.01 0.5 }
label textformat Atoms 4 { 5:179 }
label add Atoms 0/5
label textoffset Atoms 5 { 0.01 0.01 0.5 }
label textformat Atoms 5 { 6:H-C= }
label add Atoms 0/6
label textoffset Atoms 6 { 0.01 0.01 0.5 }
label textformat Atoms 6 { 7:H-C= }
label add Atoms 0/7
label textoffset Atoms 7 { 0.01 0.01 0.5 }
label textformat Atoms 7 { 8:H-C= }
label add Atoms 0/8
label textoffset Atoms 8 { 0.01 0.01 0.5 }
label textformat Atoms 8 { 9:182 }
label add Atoms 0/9
label textoffset Atoms 9 { 0.01 0.01 0.5 }
label textformat Atoms 9 { 10:182 }
mol modstyle 0 0 CPK 0.6 0.2 12.0 12.0
