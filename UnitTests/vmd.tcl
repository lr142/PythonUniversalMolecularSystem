color	Element	C	gray
color	Element	Al	magenta
color	Element	Si	orange
color	Element	Mg	green
color	Element	Na	blue
color	Element	K	purple
color	Element	Cl	green
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
