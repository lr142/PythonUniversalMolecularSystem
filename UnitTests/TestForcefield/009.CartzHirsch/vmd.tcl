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
label textthickness 1.5
label textsize 1.0
label add Atoms 0/0
label textoffset Atoms 0 { 0.01 0.01 0.5 }
label textformat Atoms 0 { %i:0.15 }
label add Atoms 0/1
label textoffset Atoms 1 { 0.01 0.01 0.5 }
label textformat Atoms 1 { %i:-0.115 }
label add Atoms 0/2
label textoffset Atoms 2 { 0.01 0.01 0.5 }
label textformat Atoms 2 { %i:0.0 }
label add Atoms 0/3
label textoffset Atoms 3 { 0.01 0.01 0.5 }
label textformat Atoms 3 { %i:0.0 }
label add Atoms 0/4
label textoffset Atoms 4 { 0.01 0.01 0.5 }
label textformat Atoms 4 { %i:-0.115 }
label add Atoms 0/5
label textoffset Atoms 5 { 0.01 0.01 0.5 }
label textformat Atoms 5 { %i:0.0 }
label add Atoms 0/6
label textoffset Atoms 6 { 0.01 0.01 0.5 }
label textformat Atoms 6 { %i:0.0 }
label add Atoms 0/7
label textoffset Atoms 7 { 0.01 0.01 0.5 }
label textformat Atoms 7 { %i:0.0 }
label add Atoms 0/8
label textoffset Atoms 8 { 0.01 0.01 0.5 }
label textformat Atoms 8 { %i:-0.12 }
label add Atoms 0/9
label textoffset Atoms 9 { 0.01 0.01 0.5 }
label textformat Atoms 9 { %i:0.0 }
label add Atoms 0/10
label textoffset Atoms 10 { 0.01 0.01 0.5 }
label textformat Atoms 10 { %i:0.0 }
label add Atoms 0/11
label textoffset Atoms 11 { 0.01 0.01 0.5 }
label textformat Atoms 11 { %i:0.0 }
label add Atoms 0/12
label textoffset Atoms 12 { 0.01 0.01 0.5 }
label textformat Atoms 12 { %i:0.0 }
label add Atoms 0/13
label textoffset Atoms 13 { 0.01 0.01 0.5 }
label textformat Atoms 13 { %i:-0.12 }
label add Atoms 0/14
label textoffset Atoms 14 { 0.01 0.01 0.5 }
label textformat Atoms 14 { %i:-0.12 }
label add Atoms 0/15
label textoffset Atoms 15 { 0.01 0.01 0.5 }
label textformat Atoms 15 { %i:-0.12 }
label add Atoms 0/16
label textoffset Atoms 16 { 0.01 0.01 0.5 }
label textformat Atoms 16 { %i:0.0 }
label add Atoms 0/17
label textoffset Atoms 17 { 0.01 0.01 0.5 }
label textformat Atoms 17 { %i:0.0 }
label add Atoms 0/18
label textoffset Atoms 18 { 0.01 0.01 0.5 }
label textformat Atoms 18 { %i:0.0 }
label add Atoms 0/19
label textoffset Atoms 19 { 0.01 0.01 0.5 }
label textformat Atoms 19 { %i:0.0 }
label add Atoms 0/20
label textoffset Atoms 20 { 0.01 0.01 0.5 }
label textformat Atoms 20 { %i:0.0 }
label add Atoms 0/21
label textoffset Atoms 21 { 0.01 0.01 0.5 }
label textformat Atoms 21 { %i:0.0 }
label add Atoms 0/22
label textoffset Atoms 22 { 0.01 0.01 0.5 }
label textformat Atoms 22 { %i:0.15 }
label add Atoms 0/23
label textoffset Atoms 23 { 0.01 0.01 0.5 }
label textformat Atoms 23 { %i:-0.12 }
label add Atoms 0/24
label textoffset Atoms 24 { 0.01 0.01 0.5 }
label textformat Atoms 24 { %i:0.0 }
label add Atoms 0/25
label textoffset Atoms 25 { 0.01 0.01 0.5 }
label textformat Atoms 25 { %i:0.0 }
label add Atoms 0/26
label textoffset Atoms 26 { 0.01 0.01 0.5 }
label textformat Atoms 26 { %i:-0.12 }
label add Atoms 0/27
label textoffset Atoms 27 { 0.01 0.01 0.5 }
label textformat Atoms 27 { %i:0.15 }
label add Atoms 0/28
label textoffset Atoms 28 { 0.01 0.01 0.5 }
label textformat Atoms 28 { %i:0.0 }
label add Atoms 0/29
label textoffset Atoms 29 { 0.01 0.01 0.5 }
label textformat Atoms 29 { %i:0.0 }
label add Atoms 0/30
label textoffset Atoms 30 { 0.01 0.01 0.5 }
label textformat Atoms 30 { %i:0.0 }
label add Atoms 0/31
label textoffset Atoms 31 { 0.01 0.01 0.5 }
label textformat Atoms 31 { %i:0.0 }
label add Atoms 0/32
label textoffset Atoms 32 { 0.01 0.01 0.5 }
label textformat Atoms 32 { %i:-0.12 }
label add Atoms 0/33
label textoffset Atoms 33 { 0.01 0.01 0.5 }
label textformat Atoms 33 { %i:-0.12 }
label add Atoms 0/34
label textoffset Atoms 34 { 0.01 0.01 0.5 }
label textformat Atoms 34 { %i:-0.12 }
label add Atoms 0/35
label textoffset Atoms 35 { 0.01 0.01 0.5 }
label textformat Atoms 35 { %i:-0.115 }
label add Atoms 0/36
label textoffset Atoms 36 { 0.01 0.01 0.5 }
label textformat Atoms 36 { %i:0.15 }
label add Atoms 0/37
label textoffset Atoms 37 { 0.01 0.01 0.5 }
label textformat Atoms 37 { %i:-0.115 }
label add Atoms 0/38
label textoffset Atoms 38 { 0.01 0.01 0.5 }
label textformat Atoms 38 { %i:-0.12 }
label add Atoms 0/39
label textoffset Atoms 39 { 0.01 0.01 0.5 }
label textformat Atoms 39 { %i:0.0 }
label add Atoms 0/40
label textoffset Atoms 40 { 0.01 0.01 0.5 }
label textformat Atoms 40 { %i:0.0 }
label add Atoms 0/41
label textoffset Atoms 41 { 0.01 0.01 0.5 }
label textformat Atoms 41 { %i:-0.115 }
label add Atoms 0/42
label textoffset Atoms 42 { 0.01 0.01 0.5 }
label textformat Atoms 42 { %i:0.0 }
label add Atoms 0/43
label textoffset Atoms 43 { 0.01 0.01 0.5 }
label textformat Atoms 43 { %i:0.0 }
label add Atoms 0/44
label textoffset Atoms 44 { 0.01 0.01 0.5 }
label textformat Atoms 44 { %i:0.0 }
label add Atoms 0/45
label textoffset Atoms 45 { 0.01 0.01 0.5 }
label textformat Atoms 45 { %i:-0.115 }
label add Atoms 0/46
label textoffset Atoms 46 { 0.01 0.01 0.5 }
label textformat Atoms 46 { %i:0.0 }
label add Atoms 0/47
label textoffset Atoms 47 { 0.01 0.01 0.5 }
label textformat Atoms 47 { %i:-0.115 }
label add Atoms 0/48
label textoffset Atoms 48 { 0.01 0.01 0.5 }
label textformat Atoms 48 { %i:0.0 }
label add Atoms 0/49
label textoffset Atoms 49 { 0.01 0.01 0.5 }
label textformat Atoms 49 { %i:0.15 }
label add Atoms 0/50
label textoffset Atoms 50 { 0.01 0.01 0.5 }
label textformat Atoms 50 { %i:-0.115 }
label add Atoms 0/51
label textoffset Atoms 51 { 0.01 0.01 0.5 }
label textformat Atoms 51 { %i:-0.115 }
label add Atoms 0/52
label textoffset Atoms 52 { 0.01 0.01 0.5 }
label textformat Atoms 52 { %i:-0.585 }
label add Atoms 0/53
label textoffset Atoms 53 { 0.01 0.01 0.5 }
label textformat Atoms 53 { %i:-0.18 }
label add Atoms 0/54
label textoffset Atoms 54 { 0.01 0.01 0.5 }
label textformat Atoms 54 { %i:-0.585 }
label add Atoms 0/55
label textoffset Atoms 55 { 0.01 0.01 0.5 }
label textformat Atoms 55 { %i:-0.12 }
label add Atoms 0/56
label textoffset Atoms 56 { 0.01 0.01 0.5 }
label textformat Atoms 56 { %i:-0.18 }
label add Atoms 0/57
label textoffset Atoms 57 { 0.01 0.01 0.5 }
label textformat Atoms 57 { %i:-0.585 }
label add Atoms 0/58
label textoffset Atoms 58 { 0.01 0.01 0.5 }
label textformat Atoms 58 { %i:-0.585 }
label add Atoms 0/59
label textoffset Atoms 59 { 0.01 0.01 0.5 }
label textformat Atoms 59 { %i:-0.585 }
label add Atoms 0/60
label textoffset Atoms 60 { 0.01 0.01 0.5 }
label textformat Atoms 60 { %i:0.115 }
label add Atoms 0/61
label textoffset Atoms 61 { 0.01 0.01 0.5 }
label textformat Atoms 61 { %i:0.115 }
label add Atoms 0/62
label textoffset Atoms 62 { 0.01 0.01 0.5 }
label textformat Atoms 62 { %i:0.06 }
label add Atoms 0/63
label textoffset Atoms 63 { 0.01 0.01 0.5 }
label textformat Atoms 63 { %i:0.06 }
label add Atoms 0/64
label textoffset Atoms 64 { 0.01 0.01 0.5 }
label textformat Atoms 64 { %i:0.06 }
label add Atoms 0/65
label textoffset Atoms 65 { 0.01 0.01 0.5 }
label textformat Atoms 65 { %i:0.06 }
label add Atoms 0/66
label textoffset Atoms 66 { 0.01 0.01 0.5 }
label textformat Atoms 66 { %i:0.06 }
label add Atoms 0/67
label textoffset Atoms 67 { 0.01 0.01 0.5 }
label textformat Atoms 67 { %i:0.06 }
label add Atoms 0/68
label textoffset Atoms 68 { 0.01 0.01 0.5 }
label textformat Atoms 68 { %i:0.06 }
label add Atoms 0/69
label textoffset Atoms 69 { 0.01 0.01 0.5 }
label textformat Atoms 69 { %i:0.06 }
label add Atoms 0/70
label textoffset Atoms 70 { 0.01 0.01 0.5 }
label textformat Atoms 70 { %i:0.06 }
label add Atoms 0/71
label textoffset Atoms 71 { 0.01 0.01 0.5 }
label textformat Atoms 71 { %i:0.06 }
label add Atoms 0/72
label textoffset Atoms 72 { 0.01 0.01 0.5 }
label textformat Atoms 72 { %i:0.06 }
label add Atoms 0/73
label textoffset Atoms 73 { 0.01 0.01 0.5 }
label textformat Atoms 73 { %i:0.06 }
label add Atoms 0/74
label textoffset Atoms 74 { 0.01 0.01 0.5 }
label textformat Atoms 74 { %i:0.06 }
label add Atoms 0/75
label textoffset Atoms 75 { 0.01 0.01 0.5 }
label textformat Atoms 75 { %i:0.06 }
label add Atoms 0/76
label textoffset Atoms 76 { 0.01 0.01 0.5 }
label textformat Atoms 76 { %i:0.06 }
label add Atoms 0/77
label textoffset Atoms 77 { 0.01 0.01 0.5 }
label textformat Atoms 77 { %i:0.06 }
label add Atoms 0/78
label textoffset Atoms 78 { 0.01 0.01 0.5 }
label textformat Atoms 78 { %i:0.115 }
label add Atoms 0/79
label textoffset Atoms 79 { 0.01 0.01 0.5 }
label textformat Atoms 79 { %i:0.115 }
label add Atoms 0/80
label textoffset Atoms 80 { 0.01 0.01 0.5 }
label textformat Atoms 80 { %i:0.06 }
label add Atoms 0/81
label textoffset Atoms 81 { 0.01 0.01 0.5 }
label textformat Atoms 81 { %i:0.06 }
label add Atoms 0/82
label textoffset Atoms 82 { 0.01 0.01 0.5 }
label textformat Atoms 82 { %i:0.115 }
label add Atoms 0/83
label textoffset Atoms 83 { 0.01 0.01 0.5 }
label textformat Atoms 83 { %i:0.115 }
label add Atoms 0/84
label textoffset Atoms 84 { 0.01 0.01 0.5 }
label textformat Atoms 84 { %i:0.115 }
label add Atoms 0/85
label textoffset Atoms 85 { 0.01 0.01 0.5 }
label textformat Atoms 85 { %i:0.115 }
label add Atoms 0/86
label textoffset Atoms 86 { 0.01 0.01 0.5 }
label textformat Atoms 86 { %i:0.115 }
label add Atoms 0/87
label textoffset Atoms 87 { 0.01 0.01 0.5 }
label textformat Atoms 87 { %i:0.435 }
label add Atoms 0/88
label textoffset Atoms 88 { 0.01 0.01 0.5 }
label textformat Atoms 88 { %i:0.06 }
label add Atoms 0/89
label textoffset Atoms 89 { 0.01 0.01 0.5 }
label textformat Atoms 89 { %i:0.06 }
label add Atoms 0/90
label textoffset Atoms 90 { 0.01 0.01 0.5 }
label textformat Atoms 90 { %i:0.06 }
label add Atoms 0/91
label textoffset Atoms 91 { 0.01 0.01 0.5 }
label textformat Atoms 91 { %i:0.435 }
label add Atoms 0/92
label textoffset Atoms 92 { 0.01 0.01 0.5 }
label textformat Atoms 92 { %i:0.06 }
label add Atoms 0/93
label textoffset Atoms 93 { 0.01 0.01 0.5 }
label textformat Atoms 93 { %i:0.06 }
label add Atoms 0/94
label textoffset Atoms 94 { 0.01 0.01 0.5 }
label textformat Atoms 94 { %i:0.06 }
label add Atoms 0/95
label textoffset Atoms 95 { 0.01 0.01 0.5 }
label textformat Atoms 95 { %i:0.06 }
label add Atoms 0/96
label textoffset Atoms 96 { 0.01 0.01 0.5 }
label textformat Atoms 96 { %i:0.435 }
label add Atoms 0/97
label textoffset Atoms 97 { 0.01 0.01 0.5 }
label textformat Atoms 97 { %i:0.435 }
label add Atoms 0/98
label textoffset Atoms 98 { 0.01 0.01 0.5 }
label textformat Atoms 98 { %i:0.435 }
label add Atoms 0/99
label textoffset Atoms 99 { 0.01 0.01 0.5 }
label textformat Atoms 99 { %i:0.06 }
label add Atoms 0/100
label textoffset Atoms 100 { 0.01 0.01 0.5 }
label textformat Atoms 100 { %i:0.06 }
label add Atoms 0/101
label textoffset Atoms 101 { 0.01 0.01 0.5 }
label textformat Atoms 101 { %i:0.06 }
mol modstyle 0 0 CPK 0.6 0.2 12.0 12.0
