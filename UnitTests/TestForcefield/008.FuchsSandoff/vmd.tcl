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
label textformat Atoms 0 { %i:0.14 }
label add Atoms 0/1
label textoffset Atoms 1 { 0.01 0.01 0.5 }
label textformat Atoms 1 { %i:-0.12 }
label add Atoms 0/2
label textoffset Atoms 2 { 0.01 0.01 0.5 }
label textformat Atoms 2 { %i:-0.06 }
label add Atoms 0/3
label textoffset Atoms 3 { 0.01 0.01 0.5 }
label textformat Atoms 3 { %i:-0.06 }
label add Atoms 0/4
label textoffset Atoms 4 { 0.01 0.01 0.5 }
label textformat Atoms 4 { %i:0.14 }
label add Atoms 0/5
label textoffset Atoms 5 { 0.01 0.01 0.5 }
label textformat Atoms 5 { %i:-0.4 }
label add Atoms 0/6
label textoffset Atoms 6 { 0.01 0.01 0.5 }
label textformat Atoms 6 { %i:-0.06 }
label add Atoms 0/7
label textoffset Atoms 7 { 0.01 0.01 0.5 }
label textformat Atoms 7 { %i:0.17 }
label add Atoms 0/8
label textoffset Atoms 8 { 0.01 0.01 0.5 }
label textformat Atoms 8 { %i:-0.12 }
label add Atoms 0/9
label textoffset Atoms 9 { 0.01 0.01 0.5 }
label textformat Atoms 9 { %i:-0.12 }
label add Atoms 0/10
label textoffset Atoms 10 { 0.01 0.01 0.5 }
label textformat Atoms 10 { %i:-0.4 }
label add Atoms 0/11
label textoffset Atoms 11 { 0.01 0.01 0.5 }
label textformat Atoms 11 { %i:0.17 }
label add Atoms 0/12
label textoffset Atoms 12 { 0.01 0.01 0.5 }
label textformat Atoms 12 { %i:-0.06 }
label add Atoms 0/13
label textoffset Atoms 13 { 0.01 0.01 0.5 }
label textformat Atoms 13 { %i:-0.12 }
label add Atoms 0/14
label textoffset Atoms 14 { 0.01 0.01 0.5 }
label textformat Atoms 14 { %i:0.0 }
label add Atoms 0/15
label textoffset Atoms 15 { 0.01 0.01 0.5 }
label textformat Atoms 15 { %i:0.0 }
label add Atoms 0/16
label textoffset Atoms 16 { 0.01 0.01 0.5 }
label textformat Atoms 16 { %i:0.0 }
label add Atoms 0/17
label textoffset Atoms 17 { 0.01 0.01 0.5 }
label textformat Atoms 17 { %i:-0.06 }
label add Atoms 0/18
label textoffset Atoms 18 { 0.01 0.01 0.5 }
label textformat Atoms 18 { %i:0.0 }
label add Atoms 0/19
label textoffset Atoms 19 { 0.01 0.01 0.5 }
label textformat Atoms 19 { %i:0.0 }
label add Atoms 0/20
label textoffset Atoms 20 { 0.01 0.01 0.5 }
label textformat Atoms 20 { %i:0.2 }
label add Atoms 0/21
label textoffset Atoms 21 { 0.01 0.01 0.5 }
label textformat Atoms 21 { %i:0.0 }
label add Atoms 0/22
label textoffset Atoms 22 { 0.01 0.01 0.5 }
label textformat Atoms 22 { %i:-0.12 }
label add Atoms 0/23
label textoffset Atoms 23 { 0.01 0.01 0.5 }
label textformat Atoms 23 { %i:-0.12 }
label add Atoms 0/24
label textoffset Atoms 24 { 0.01 0.01 0.5 }
label textformat Atoms 24 { %i:-0.115 }
label add Atoms 0/25
label textoffset Atoms 25 { 0.01 0.01 0.5 }
label textformat Atoms 25 { %i:-0.4 }
label add Atoms 0/26
label textoffset Atoms 26 { 0.01 0.01 0.5 }
label textformat Atoms 26 { %i:0.2 }
label add Atoms 0/27
label textoffset Atoms 27 { 0.01 0.01 0.5 }
label textformat Atoms 27 { %i:0.0 }
label add Atoms 0/28
label textoffset Atoms 28 { 0.01 0.01 0.5 }
label textformat Atoms 28 { %i:0.0 }
label add Atoms 0/29
label textoffset Atoms 29 { 0.01 0.01 0.5 }
label textformat Atoms 29 { %i:0.0 }
label add Atoms 0/30
label textoffset Atoms 30 { 0.01 0.01 0.5 }
label textformat Atoms 30 { %i:-0.06 }
label add Atoms 0/31
label textoffset Atoms 31 { 0.01 0.01 0.5 }
label textformat Atoms 31 { %i:0.0 }
label add Atoms 0/32
label textoffset Atoms 32 { 0.01 0.01 0.5 }
label textformat Atoms 32 { %i:0.0 }
label add Atoms 0/33
label textoffset Atoms 33 { 0.01 0.01 0.5 }
label textformat Atoms 33 { %i:0.0 }
label add Atoms 0/34
label textoffset Atoms 34 { 0.01 0.01 0.5 }
label textformat Atoms 34 { %i:-0.12 }
label add Atoms 0/35
label textoffset Atoms 35 { 0.01 0.01 0.5 }
label textformat Atoms 35 { %i:-0.115 }
label add Atoms 0/36
label textoffset Atoms 36 { 0.01 0.01 0.5 }
label textformat Atoms 36 { %i:-0.12 }
label add Atoms 0/37
label textoffset Atoms 37 { 0.01 0.01 0.5 }
label textformat Atoms 37 { %i:-0.12 }
label add Atoms 0/38
label textoffset Atoms 38 { 0.01 0.01 0.5 }
label textformat Atoms 38 { %i:0.0 }
label add Atoms 0/39
label textoffset Atoms 39 { 0.01 0.01 0.5 }
label textformat Atoms 39 { %i:0.0 }
label add Atoms 0/40
label textoffset Atoms 40 { 0.01 0.01 0.5 }
label textformat Atoms 40 { %i:-0.12 }
label add Atoms 0/41
label textoffset Atoms 41 { 0.01 0.01 0.5 }
label textformat Atoms 41 { %i:-0.06 }
label add Atoms 0/42
label textoffset Atoms 42 { 0.01 0.01 0.5 }
label textformat Atoms 42 { %i:-0.12 }
label add Atoms 0/43
label textoffset Atoms 43 { 0.01 0.01 0.5 }
label textformat Atoms 43 { %i:-0.12 }
label add Atoms 0/44
label textoffset Atoms 44 { 0.01 0.01 0.5 }
label textformat Atoms 44 { %i:0.1025 }
label add Atoms 0/45
label textoffset Atoms 45 { 0.01 0.01 0.5 }
label textformat Atoms 45 { %i:-0.115 }
label add Atoms 0/46
label textoffset Atoms 46 { 0.01 0.01 0.5 }
label textformat Atoms 46 { %i:0.0 }
label add Atoms 0/47
label textoffset Atoms 47 { 0.01 0.01 0.5 }
label textformat Atoms 47 { %i:0.1025 }
label add Atoms 0/48
label textoffset Atoms 48 { 0.01 0.01 0.5 }
label textformat Atoms 48 { %i:-0.205 }
label add Atoms 0/49
label textoffset Atoms 49 { 0.01 0.01 0.5 }
label textformat Atoms 49 { %i:-0.115 }
label add Atoms 0/50
label textoffset Atoms 50 { 0.01 0.01 0.5 }
label textformat Atoms 50 { %i:0.0 }
label add Atoms 0/51
label textoffset Atoms 51 { 0.01 0.01 0.5 }
label textformat Atoms 51 { %i:0.0 }
label add Atoms 0/52
label textoffset Atoms 52 { 0.01 0.01 0.5 }
label textformat Atoms 52 { %i:0.0 }
label add Atoms 0/53
label textoffset Atoms 53 { 0.01 0.01 0.5 }
label textformat Atoms 53 { %i:0.0 }
label add Atoms 0/54
label textoffset Atoms 54 { 0.01 0.01 0.5 }
label textformat Atoms 54 { %i:0.0 }
label add Atoms 0/55
label textoffset Atoms 55 { 0.01 0.01 0.5 }
label textformat Atoms 55 { %i:0.0 }
label add Atoms 0/56
label textoffset Atoms 56 { 0.01 0.01 0.5 }
label textformat Atoms 56 { %i:-0.115 }
label add Atoms 0/57
label textoffset Atoms 57 { 0.01 0.01 0.5 }
label textformat Atoms 57 { %i:0.0 }
label add Atoms 0/58
label textoffset Atoms 58 { 0.01 0.01 0.5 }
label textformat Atoms 58 { %i:0.2 }
label add Atoms 0/59
label textoffset Atoms 59 { 0.01 0.01 0.5 }
label textformat Atoms 59 { %i:0.0 }
label add Atoms 0/60
label textoffset Atoms 60 { 0.01 0.01 0.5 }
label textformat Atoms 60 { %i:0.0 }
label add Atoms 0/61
label textoffset Atoms 61 { 0.01 0.01 0.5 }
label textformat Atoms 61 { %i:0.0 }
label add Atoms 0/62
label textoffset Atoms 62 { 0.01 0.01 0.5 }
label textformat Atoms 62 { %i:-0.115 }
label add Atoms 0/63
label textoffset Atoms 63 { 0.01 0.01 0.5 }
label textformat Atoms 63 { %i:0.0 }
label add Atoms 0/64
label textoffset Atoms 64 { 0.01 0.01 0.5 }
label textformat Atoms 64 { %i:0.0 }
label add Atoms 0/65
label textoffset Atoms 65 { 0.01 0.01 0.5 }
label textformat Atoms 65 { %i:0.0 }
label add Atoms 0/66
label textoffset Atoms 66 { 0.01 0.01 0.5 }
label textformat Atoms 66 { %i:0.0 }
label add Atoms 0/67
label textoffset Atoms 67 { 0.01 0.01 0.5 }
label textformat Atoms 67 { %i:0.0 }
label add Atoms 0/68
label textoffset Atoms 68 { 0.01 0.01 0.5 }
label textformat Atoms 68 { %i:0.0 }
label add Atoms 0/69
label textoffset Atoms 69 { 0.01 0.01 0.5 }
label textformat Atoms 69 { %i:0.0 }
label add Atoms 0/70
label textoffset Atoms 70 { 0.01 0.01 0.5 }
label textformat Atoms 70 { %i:-0.4 }
label add Atoms 0/71
label textoffset Atoms 71 { 0.01 0.01 0.5 }
label textformat Atoms 71 { %i:0.17 }
label add Atoms 0/72
label textoffset Atoms 72 { 0.01 0.01 0.5 }
label textformat Atoms 72 { %i:-0.06 }
label add Atoms 0/73
label textoffset Atoms 73 { 0.01 0.01 0.5 }
label textformat Atoms 73 { %i:0.205 }
label add Atoms 0/74
label textoffset Atoms 74 { 0.01 0.01 0.5 }
label textformat Atoms 74 { %i:-0.12 }
label add Atoms 0/75
label textoffset Atoms 75 { 0.01 0.01 0.5 }
label textformat Atoms 75 { %i:-0.12 }
label add Atoms 0/76
label textoffset Atoms 76 { 0.01 0.01 0.5 }
label textformat Atoms 76 { %i:0.14 }
label add Atoms 0/77
label textoffset Atoms 77 { 0.01 0.01 0.5 }
label textformat Atoms 77 { %i:-0.06 }
label add Atoms 0/78
label textoffset Atoms 78 { 0.01 0.01 0.5 }
label textformat Atoms 78 { %i:-0.12 }
label add Atoms 0/79
label textoffset Atoms 79 { 0.01 0.01 0.5 }
label textformat Atoms 79 { %i:-0.12 }
label add Atoms 0/80
label textoffset Atoms 80 { 0.01 0.01 0.5 }
label textformat Atoms 80 { %i:0.08 }
label add Atoms 0/81
label textoffset Atoms 81 { 0.01 0.01 0.5 }
label textformat Atoms 81 { %i:-0.78 }
label add Atoms 0/82
label textoffset Atoms 82 { 0.01 0.01 0.5 }
label textformat Atoms 82 { %i:0.2 }
label add Atoms 0/83
label textoffset Atoms 83 { 0.01 0.01 0.5 }
label textformat Atoms 83 { %i:0.2 }
label add Atoms 0/84
label textoffset Atoms 84 { 0.01 0.01 0.5 }
label textformat Atoms 84 { %i:0.0 }
label add Atoms 0/85
label textoffset Atoms 85 { 0.01 0.01 0.5 }
label textformat Atoms 85 { %i:-0.4 }
label add Atoms 0/86
label textoffset Atoms 86 { 0.01 0.01 0.5 }
label textformat Atoms 86 { %i:0.17 }
label add Atoms 0/87
label textoffset Atoms 87 { 0.01 0.01 0.5 }
label textformat Atoms 87 { %i:0.17 }
label add Atoms 0/88
label textoffset Atoms 88 { 0.01 0.01 0.5 }
label textformat Atoms 88 { %i:-0.4 }
label add Atoms 0/89
label textoffset Atoms 89 { 0.01 0.01 0.5 }
label textformat Atoms 89 { %i:-0.12 }
label add Atoms 0/90
label textoffset Atoms 90 { 0.01 0.01 0.5 }
label textformat Atoms 90 { %i:-0.12 }
label add Atoms 0/91
label textoffset Atoms 91 { 0.01 0.01 0.5 }
label textformat Atoms 91 { %i:-0.12 }
label add Atoms 0/92
label textoffset Atoms 92 { 0.01 0.01 0.5 }
label textformat Atoms 92 { %i:-0.12 }
label add Atoms 0/93
label textoffset Atoms 93 { 0.01 0.01 0.5 }
label textformat Atoms 93 { %i:0.0 }
label add Atoms 0/94
label textoffset Atoms 94 { 0.01 0.01 0.5 }
label textformat Atoms 94 { %i:-0.115 }
label add Atoms 0/95
label textoffset Atoms 95 { 0.01 0.01 0.5 }
label textformat Atoms 95 { %i:0.0 }
label add Atoms 0/96
label textoffset Atoms 96 { 0.01 0.01 0.5 }
label textformat Atoms 96 { %i:0.2 }
label add Atoms 0/97
label textoffset Atoms 97 { 0.01 0.01 0.5 }
label textformat Atoms 97 { %i:-0.115 }
label add Atoms 0/98
label textoffset Atoms 98 { 0.01 0.01 0.5 }
label textformat Atoms 98 { %i:0.0 }
label add Atoms 0/99
label textoffset Atoms 99 { 0.01 0.01 0.5 }
label textformat Atoms 99 { %i:0.0 }
label add Atoms 0/100
label textoffset Atoms 100 { 0.01 0.01 0.5 }
label textformat Atoms 100 { %i:-0.115 }
label add Atoms 0/101
label textoffset Atoms 101 { 0.01 0.01 0.5 }
label textformat Atoms 101 { %i:-0.4 }
label add Atoms 0/102
label textoffset Atoms 102 { 0.01 0.01 0.5 }
label textformat Atoms 102 { %i:0.2 }
label add Atoms 0/103
label textoffset Atoms 103 { 0.01 0.01 0.5 }
label textformat Atoms 103 { %i:0.0 }
label add Atoms 0/104
label textoffset Atoms 104 { 0.01 0.01 0.5 }
label textformat Atoms 104 { %i:-0.06 }
label add Atoms 0/105
label textoffset Atoms 105 { 0.01 0.01 0.5 }
label textformat Atoms 105 { %i:-0.06 }
label add Atoms 0/106
label textoffset Atoms 106 { 0.01 0.01 0.5 }
label textformat Atoms 106 { %i:0.0 }
label add Atoms 0/107
label textoffset Atoms 107 { 0.01 0.01 0.5 }
label textformat Atoms 107 { %i:-0.06 }
label add Atoms 0/108
label textoffset Atoms 108 { 0.01 0.01 0.5 }
label textformat Atoms 108 { %i:-0.12 }
label add Atoms 0/109
label textoffset Atoms 109 { 0.01 0.01 0.5 }
label textformat Atoms 109 { %i:-0.12 }
label add Atoms 0/110
label textoffset Atoms 110 { 0.01 0.01 0.5 }
label textformat Atoms 110 { %i:-0.12 }
label add Atoms 0/111
label textoffset Atoms 111 { 0.01 0.01 0.5 }
label textformat Atoms 111 { %i:0.0 }
label add Atoms 0/112
label textoffset Atoms 112 { 0.01 0.01 0.5 }
label textformat Atoms 112 { %i:0.0 }
label add Atoms 0/113
label textoffset Atoms 113 { 0.01 0.01 0.5 }
label textformat Atoms 113 { %i:0.0 }
label add Atoms 0/114
label textoffset Atoms 114 { 0.01 0.01 0.5 }
label textformat Atoms 114 { %i:0.0 }
label add Atoms 0/115
label textoffset Atoms 115 { 0.01 0.01 0.5 }
label textformat Atoms 115 { %i:0.0 }
label add Atoms 0/116
label textoffset Atoms 116 { 0.01 0.01 0.5 }
label textformat Atoms 116 { %i:-0.06 }
label add Atoms 0/117
label textoffset Atoms 117 { 0.01 0.01 0.5 }
label textformat Atoms 117 { %i:-0.18 }
label add Atoms 0/118
label textoffset Atoms 118 { 0.01 0.01 0.5 }
label textformat Atoms 118 { %i:-0.18 }
label add Atoms 0/119
label textoffset Atoms 119 { 0.01 0.01 0.5 }
label textformat Atoms 119 { %i:-0.683 }
label add Atoms 0/120
label textoffset Atoms 120 { 0.01 0.01 0.5 }
label textformat Atoms 120 { %i:-0.115 }
label add Atoms 0/121
label textoffset Atoms 121 { 0.01 0.01 0.5 }
label textformat Atoms 121 { %i:-0.115 }
label add Atoms 0/122
label textoffset Atoms 122 { 0.01 0.01 0.5 }
label textformat Atoms 122 { %i:0.0 }
label add Atoms 0/123
label textoffset Atoms 123 { 0.01 0.01 0.5 }
label textformat Atoms 123 { %i:0.0 }
label add Atoms 0/124
label textoffset Atoms 124 { 0.01 0.01 0.5 }
label textformat Atoms 124 { %i:0.0 }
label add Atoms 0/125
label textoffset Atoms 125 { 0.01 0.01 0.5 }
label textformat Atoms 125 { %i:0.0 }
label add Atoms 0/126
label textoffset Atoms 126 { 0.01 0.01 0.5 }
label textformat Atoms 126 { %i:0.0 }
label add Atoms 0/127
label textoffset Atoms 127 { 0.01 0.01 0.5 }
label textformat Atoms 127 { %i:-0.115 }
label add Atoms 0/128
label textoffset Atoms 128 { 0.01 0.01 0.5 }
label textformat Atoms 128 { %i:-0.115 }
label add Atoms 0/129
label textoffset Atoms 129 { 0.01 0.01 0.5 }
label textformat Atoms 129 { %i:-0.115 }
label add Atoms 0/130
label textoffset Atoms 130 { 0.01 0.01 0.5 }
label textformat Atoms 130 { %i:0.0 }
label add Atoms 0/131
label textoffset Atoms 131 { 0.01 0.01 0.5 }
label textformat Atoms 131 { %i:0.0 }
label add Atoms 0/132
label textoffset Atoms 132 { 0.01 0.01 0.5 }
label textformat Atoms 132 { %i:0.0 }
label add Atoms 0/133
label textoffset Atoms 133 { 0.01 0.01 0.5 }
label textformat Atoms 133 { %i:0.0 }
label add Atoms 0/134
label textoffset Atoms 134 { 0.01 0.01 0.5 }
label textformat Atoms 134 { %i:0.0 }
label add Atoms 0/135
label textoffset Atoms 135 { 0.01 0.01 0.5 }
label textformat Atoms 135 { %i:0.0 }
label add Atoms 0/136
label textoffset Atoms 136 { 0.01 0.01 0.5 }
label textformat Atoms 136 { %i:-0.115 }
label add Atoms 0/137
label textoffset Atoms 137 { 0.01 0.01 0.5 }
label textformat Atoms 137 { %i:-0.115 }
label add Atoms 0/138
label textoffset Atoms 138 { 0.01 0.01 0.5 }
label textformat Atoms 138 { %i:-0.115 }
label add Atoms 0/139
label textoffset Atoms 139 { 0.01 0.01 0.5 }
label textformat Atoms 139 { %i:0.0 }
label add Atoms 0/140
label textoffset Atoms 140 { 0.01 0.01 0.5 }
label textformat Atoms 140 { %i:0.0 }
label add Atoms 0/141
label textoffset Atoms 141 { 0.01 0.01 0.5 }
label textformat Atoms 141 { %i:0.0 }
label add Atoms 0/142
label textoffset Atoms 142 { 0.01 0.01 0.5 }
label textformat Atoms 142 { %i:-0.12 }
label add Atoms 0/143
label textoffset Atoms 143 { 0.01 0.01 0.5 }
label textformat Atoms 143 { %i:-0.12 }
label add Atoms 0/144
label textoffset Atoms 144 { 0.01 0.01 0.5 }
label textformat Atoms 144 { %i:-0.12 }
label add Atoms 0/145
label textoffset Atoms 145 { 0.01 0.01 0.5 }
label textformat Atoms 145 { %i:0.47 }
label add Atoms 0/146
label textoffset Atoms 146 { 0.01 0.01 0.5 }
label textformat Atoms 146 { %i:-0.47 }
label add Atoms 0/147
label textoffset Atoms 147 { 0.01 0.01 0.5 }
label textformat Atoms 147 { %i:0.03 }
label add Atoms 0/148
label textoffset Atoms 148 { 0.01 0.01 0.5 }
label textformat Atoms 148 { %i:0.03 }
label add Atoms 0/149
label textoffset Atoms 149 { 0.01 0.01 0.5 }
label textformat Atoms 149 { %i:0.06 }
label add Atoms 0/150
label textoffset Atoms 150 { 0.01 0.01 0.5 }
label textformat Atoms 150 { %i:0.06 }
label add Atoms 0/151
label textoffset Atoms 151 { 0.01 0.01 0.5 }
label textformat Atoms 151 { %i:0.06 }
label add Atoms 0/152
label textoffset Atoms 152 { 0.01 0.01 0.5 }
label textformat Atoms 152 { %i:0.06 }
label add Atoms 0/153
label textoffset Atoms 153 { 0.01 0.01 0.5 }
label textformat Atoms 153 { %i:0.03 }
label add Atoms 0/154
label textoffset Atoms 154 { 0.01 0.01 0.5 }
label textformat Atoms 154 { %i:0.03 }
label add Atoms 0/155
label textoffset Atoms 155 { 0.01 0.01 0.5 }
label textformat Atoms 155 { %i:0.06 }
label add Atoms 0/156
label textoffset Atoms 156 { 0.01 0.01 0.5 }
label textformat Atoms 156 { %i:0.03 }
label add Atoms 0/157
label textoffset Atoms 157 { 0.01 0.01 0.5 }
label textformat Atoms 157 { %i:0.06 }
label add Atoms 0/158
label textoffset Atoms 158 { 0.01 0.01 0.5 }
label textformat Atoms 158 { %i:0.06 }
label add Atoms 0/159
label textoffset Atoms 159 { 0.01 0.01 0.5 }
label textformat Atoms 159 { %i:0.06 }
label add Atoms 0/160
label textoffset Atoms 160 { 0.01 0.01 0.5 }
label textformat Atoms 160 { %i:0.06 }
label add Atoms 0/161
label textoffset Atoms 161 { 0.01 0.01 0.5 }
label textformat Atoms 161 { %i:0.03 }
label add Atoms 0/162
label textoffset Atoms 162 { 0.01 0.01 0.5 }
label textformat Atoms 162 { %i:0.06 }
label add Atoms 0/163
label textoffset Atoms 163 { 0.01 0.01 0.5 }
label textformat Atoms 163 { %i:0.06 }
label add Atoms 0/164
label textoffset Atoms 164 { 0.01 0.01 0.5 }
label textformat Atoms 164 { %i:0.06 }
label add Atoms 0/165
label textoffset Atoms 165 { 0.01 0.01 0.5 }
label textformat Atoms 165 { %i:0.06 }
label add Atoms 0/166
label textoffset Atoms 166 { 0.01 0.01 0.5 }
label textformat Atoms 166 { %i:0.06 }
label add Atoms 0/167
label textoffset Atoms 167 { 0.01 0.01 0.5 }
label textformat Atoms 167 { %i:0.06 }
label add Atoms 0/168
label textoffset Atoms 168 { 0.01 0.01 0.5 }
label textformat Atoms 168 { %i:0.06 }
label add Atoms 0/169
label textoffset Atoms 169 { 0.01 0.01 0.5 }
label textformat Atoms 169 { %i:0.06 }
label add Atoms 0/170
label textoffset Atoms 170 { 0.01 0.01 0.5 }
label textformat Atoms 170 { %i:0.115 }
label add Atoms 0/171
label textoffset Atoms 171 { 0.01 0.01 0.5 }
label textformat Atoms 171 { %i:0.06 }
label add Atoms 0/172
label textoffset Atoms 172 { 0.01 0.01 0.5 }
label textformat Atoms 172 { %i:0.06 }
label add Atoms 0/173
label textoffset Atoms 173 { 0.01 0.01 0.5 }
label textformat Atoms 173 { %i:0.06 }
label add Atoms 0/174
label textoffset Atoms 174 { 0.01 0.01 0.5 }
label textformat Atoms 174 { %i:0.115 }
label add Atoms 0/175
label textoffset Atoms 175 { 0.01 0.01 0.5 }
label textformat Atoms 175 { %i:0.06 }
label add Atoms 0/176
label textoffset Atoms 176 { 0.01 0.01 0.5 }
label textformat Atoms 176 { %i:0.06 }
label add Atoms 0/177
label textoffset Atoms 177 { 0.01 0.01 0.5 }
label textformat Atoms 177 { %i:0.06 }
label add Atoms 0/178
label textoffset Atoms 178 { 0.01 0.01 0.5 }
label textformat Atoms 178 { %i:0.06 }
label add Atoms 0/179
label textoffset Atoms 179 { 0.01 0.01 0.5 }
label textformat Atoms 179 { %i:0.06 }
label add Atoms 0/180
label textoffset Atoms 180 { 0.01 0.01 0.5 }
label textformat Atoms 180 { %i:0.06 }
label add Atoms 0/181
label textoffset Atoms 181 { 0.01 0.01 0.5 }
label textformat Atoms 181 { %i:0.06 }
label add Atoms 0/182
label textoffset Atoms 182 { 0.01 0.01 0.5 }
label textformat Atoms 182 { %i:0.06 }
label add Atoms 0/183
label textoffset Atoms 183 { 0.01 0.01 0.5 }
label textformat Atoms 183 { %i:0.06 }
label add Atoms 0/184
label textoffset Atoms 184 { 0.01 0.01 0.5 }
label textformat Atoms 184 { %i:0.06 }
label add Atoms 0/185
label textoffset Atoms 185 { 0.01 0.01 0.5 }
label textformat Atoms 185 { %i:0.06 }
label add Atoms 0/186
label textoffset Atoms 186 { 0.01 0.01 0.5 }
label textformat Atoms 186 { %i:0.115 }
label add Atoms 0/187
label textoffset Atoms 187 { 0.01 0.01 0.5 }
label textformat Atoms 187 { %i:0.115 }
label add Atoms 0/188
label textoffset Atoms 188 { 0.01 0.01 0.5 }
label textformat Atoms 188 { %i:0.115 }
label add Atoms 0/189
label textoffset Atoms 189 { 0.01 0.01 0.5 }
label textformat Atoms 189 { %i:0.115 }
label add Atoms 0/190
label textoffset Atoms 190 { 0.01 0.01 0.5 }
label textformat Atoms 190 { %i:0.03 }
label add Atoms 0/191
label textoffset Atoms 191 { 0.01 0.01 0.5 }
label textformat Atoms 191 { %i:0.06 }
label add Atoms 0/192
label textoffset Atoms 192 { 0.01 0.01 0.5 }
label textformat Atoms 192 { %i:0.06 }
label add Atoms 0/193
label textoffset Atoms 193 { 0.01 0.01 0.5 }
label textformat Atoms 193 { %i:0.06 }
label add Atoms 0/194
label textoffset Atoms 194 { 0.01 0.01 0.5 }
label textformat Atoms 194 { %i:0.06 }
label add Atoms 0/195
label textoffset Atoms 195 { 0.01 0.01 0.5 }
label textformat Atoms 195 { %i:0.06 }
label add Atoms 0/196
label textoffset Atoms 196 { 0.01 0.01 0.5 }
label textformat Atoms 196 { %i:0.06 }
label add Atoms 0/197
label textoffset Atoms 197 { 0.01 0.01 0.5 }
label textformat Atoms 197 { %i:0.06 }
label add Atoms 0/198
label textoffset Atoms 198 { 0.01 0.01 0.5 }
label textformat Atoms 198 { %i:0.06 }
label add Atoms 0/199
label textoffset Atoms 199 { 0.01 0.01 0.5 }
label textformat Atoms 199 { %i:0.06 }
label add Atoms 0/200
label textoffset Atoms 200 { 0.01 0.01 0.5 }
label textformat Atoms 200 { %i:0.06 }
label add Atoms 0/201
label textoffset Atoms 201 { 0.01 0.01 0.5 }
label textformat Atoms 201 { %i:0.06 }
label add Atoms 0/202
label textoffset Atoms 202 { 0.01 0.01 0.5 }
label textformat Atoms 202 { %i:0.06 }
label add Atoms 0/203
label textoffset Atoms 203 { 0.01 0.01 0.5 }
label textformat Atoms 203 { %i:0.06 }
label add Atoms 0/204
label textoffset Atoms 204 { 0.01 0.01 0.5 }
label textformat Atoms 204 { %i:0.06 }
label add Atoms 0/205
label textoffset Atoms 205 { 0.01 0.01 0.5 }
label textformat Atoms 205 { %i:0.38 }
label add Atoms 0/206
label textoffset Atoms 206 { 0.01 0.01 0.5 }
label textformat Atoms 206 { %i:0.03 }
label add Atoms 0/207
label textoffset Atoms 207 { 0.01 0.01 0.5 }
label textformat Atoms 207 { %i:0.03 }
label add Atoms 0/208
label textoffset Atoms 208 { 0.01 0.01 0.5 }
label textformat Atoms 208 { %i:0.06 }
label add Atoms 0/209
label textoffset Atoms 209 { 0.01 0.01 0.5 }
label textformat Atoms 209 { %i:0.06 }
label add Atoms 0/210
label textoffset Atoms 210 { 0.01 0.01 0.5 }
label textformat Atoms 210 { %i:0.06 }
label add Atoms 0/211
label textoffset Atoms 211 { 0.01 0.01 0.5 }
label textformat Atoms 211 { %i:0.06 }
label add Atoms 0/212
label textoffset Atoms 212 { 0.01 0.01 0.5 }
label textformat Atoms 212 { %i:0.06 }
label add Atoms 0/213
label textoffset Atoms 213 { 0.01 0.01 0.5 }
label textformat Atoms 213 { %i:0.06 }
label add Atoms 0/214
label textoffset Atoms 214 { 0.01 0.01 0.5 }
label textformat Atoms 214 { %i:0.06 }
label add Atoms 0/215
label textoffset Atoms 215 { 0.01 0.01 0.5 }
label textformat Atoms 215 { %i:0.06 }
label add Atoms 0/216
label textoffset Atoms 216 { 0.01 0.01 0.5 }
label textformat Atoms 216 { %i:0.115 }
label add Atoms 0/217
label textoffset Atoms 217 { 0.01 0.01 0.5 }
label textformat Atoms 217 { %i:0.115 }
label add Atoms 0/218
label textoffset Atoms 218 { 0.01 0.01 0.5 }
label textformat Atoms 218 { %i:0.115 }
label add Atoms 0/219
label textoffset Atoms 219 { 0.01 0.01 0.5 }
label textformat Atoms 219 { %i:0.06 }
label add Atoms 0/220
label textoffset Atoms 220 { 0.01 0.01 0.5 }
label textformat Atoms 220 { %i:0.06 }
label add Atoms 0/221
label textoffset Atoms 221 { 0.01 0.01 0.5 }
label textformat Atoms 221 { %i:0.06 }
label add Atoms 0/222
label textoffset Atoms 222 { 0.01 0.01 0.5 }
label textformat Atoms 222 { %i:0.06 }
label add Atoms 0/223
label textoffset Atoms 223 { 0.01 0.01 0.5 }
label textformat Atoms 223 { %i:0.06 }
label add Atoms 0/224
label textoffset Atoms 224 { 0.01 0.01 0.5 }
label textformat Atoms 224 { %i:0.06 }
label add Atoms 0/225
label textoffset Atoms 225 { 0.01 0.01 0.5 }
label textformat Atoms 225 { %i:0.06 }
label add Atoms 0/226
label textoffset Atoms 226 { 0.01 0.01 0.5 }
label textformat Atoms 226 { %i:0.06 }
label add Atoms 0/227
label textoffset Atoms 227 { 0.01 0.01 0.5 }
label textformat Atoms 227 { %i:0.06 }
label add Atoms 0/228
label textoffset Atoms 228 { 0.01 0.01 0.5 }
label textformat Atoms 228 { %i:0.06 }
label add Atoms 0/229
label textoffset Atoms 229 { 0.01 0.01 0.5 }
label textformat Atoms 229 { %i:0.06 }
label add Atoms 0/230
label textoffset Atoms 230 { 0.01 0.01 0.5 }
label textformat Atoms 230 { %i:0.06 }
label add Atoms 0/231
label textoffset Atoms 231 { 0.01 0.01 0.5 }
label textformat Atoms 231 { %i:0.06 }
label add Atoms 0/232
label textoffset Atoms 232 { 0.01 0.01 0.5 }
label textformat Atoms 232 { %i:0.06 }
label add Atoms 0/233
label textoffset Atoms 233 { 0.01 0.01 0.5 }
label textformat Atoms 233 { %i:0.06 }
label add Atoms 0/234
label textoffset Atoms 234 { 0.01 0.01 0.5 }
label textformat Atoms 234 { %i:0.06 }
label add Atoms 0/235
label textoffset Atoms 235 { 0.01 0.01 0.5 }
label textformat Atoms 235 { %i:0.418 }
label add Atoms 0/236
label textoffset Atoms 236 { 0.01 0.01 0.5 }
label textformat Atoms 236 { %i:0.115 }
label add Atoms 0/237
label textoffset Atoms 237 { 0.01 0.01 0.5 }
label textformat Atoms 237 { %i:0.115 }
label add Atoms 0/238
label textoffset Atoms 238 { 0.01 0.01 0.5 }
label textformat Atoms 238 { %i:0.115 }
label add Atoms 0/239
label textoffset Atoms 239 { 0.01 0.01 0.5 }
label textformat Atoms 239 { %i:0.115 }
label add Atoms 0/240
label textoffset Atoms 240 { 0.01 0.01 0.5 }
label textformat Atoms 240 { %i:0.115 }
label add Atoms 0/241
label textoffset Atoms 241 { 0.01 0.01 0.5 }
label textformat Atoms 241 { %i:0.115 }
label add Atoms 0/242
label textoffset Atoms 242 { 0.01 0.01 0.5 }
label textformat Atoms 242 { %i:0.115 }
label add Atoms 0/243
label textoffset Atoms 243 { 0.01 0.01 0.5 }
label textformat Atoms 243 { %i:0.115 }
label add Atoms 0/244
label textoffset Atoms 244 { 0.01 0.01 0.5 }
label textformat Atoms 244 { %i:0.06 }
label add Atoms 0/245
label textoffset Atoms 245 { 0.01 0.01 0.5 }
label textformat Atoms 245 { %i:0.06 }
label add Atoms 0/246
label textoffset Atoms 246 { 0.01 0.01 0.5 }
label textformat Atoms 246 { %i:0.06 }
label add Atoms 0/247
label textoffset Atoms 247 { 0.01 0.01 0.5 }
label textformat Atoms 247 { %i:0.06 }
label add Atoms 0/248
label textoffset Atoms 248 { 0.01 0.01 0.5 }
label textformat Atoms 248 { %i:0.06 }
label add Atoms 0/249
label textoffset Atoms 249 { 0.01 0.01 0.5 }
label textformat Atoms 249 { %i:0.06 }
mol modstyle 0 0 CPK 0.6 0.2 12.0 12.0
