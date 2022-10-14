# 与VMD程序进行交互的界面
import os
from Utility import output

class VMDInterface:
    def __init__(self,molecularFileName,scriptFileName="vmd.tcl",autobonds=False):
        self.molecularFileName = molecularFileName
        self.scriptFileName = scriptFileName
        self.autobonds = autobonds
        self.textsize = 1.5
        self.textthickness = 1.5
        self.commands = []
        self.Step1_Representations()
        self.Step2_LoadMolecule()
        self.Step3_Representations()

    def Step1_Representations(self):
        # Adjust Colors for some elements
        self.AddCommand("color	Element	C	gray")
        self.AddCommand("color	Element	Al	magenta")
        self.AddCommand("color	Element	Si	orange")
        self.AddCommand("color	Element	Mg	green")
        self.AddCommand("color	Element	Na	blue")
        self.AddCommand("color	Element	K	purple")
        self.AddCommand("color	Element	Cl	green")
        self.AddCommand("#display cuedensity 0.0")  # Turn off depth cue if you like by uncommenting it
        self.AddCommand("display projection Orthographic")
        self.AddCommand("menu main on")
        self.AddCommand("mol modstyle 0 0 Licorice 0.300000 12.000000 12.000000")
        self.AddCommand("mol color Name")
        self.AddCommand("mol representation Licorice 0.300000 12.000000 12.000000")
        self.AddCommand("mol selection all")
        self.AddCommand("mol material Opaque")
        self.AddCommand("mol modrep 0 0")
        self.AddCommand("color Display Background white")

    def Step2_LoadMolecule(self):
        # Autobonds On/Off 可选择是否自动加载成键。关闭的话，可用于检测体系中成键是否正常
        self.AddCommand("mol new {} autobonds {}".format(self.molecularFileName,
            'on' if self.autobonds else 'off'))
        if self.molecularFileName.endswith("mol2"):
            self.AddCommand("set sel [atomselect top all]")
            self.AddCommand("$sel set element [$sel get type]")

    def Step3_Representations(self):
        self.AddCommand("mol modcolor 0 0 Element")
        # 以下根据原子数判断。如果 > 1000, 用Lines，否则用 Stick-and-Balls
        self.AddCommand("lassign [molinfo top get numatoms] NAtoms")
        self.AddCommand("if {$NAtoms < 1000} {;mol modstyle top 0 Licorice;} else {mol modstyle top 0 Lines}")
        for keyword in "Atoms Bonds Angles Dihedrals".split():
            self.AddCommand("color Labels {} black".format(keyword))
        self.AddCommand("label textthickness 3.6")
        self.AddCommand("label textsize 1.0")
        # label add Atoms 0/{i}
        # label textoffset Atoms 0 { -0.007692 -0.060440 } # 设置偏移
        # label textformat Atoms 0 { custem  }  # 设置Label内容。
        # label textformat Atoms 0 { %i  } # %加字符是一些特殊标记，包括：%a name, %q charge, %i 0-index, %1i 1-index, %e element

    def AddLabels(self,indexes,labels,offset=None):
        if offset == None:
            offset = "{0.03 0.03 0.03}"
        else:
            offset = "{{ {} {} {} }}".format(offset[0], offset[1], offset[2])

        for index,label in zip(indexes,labels):
            self.AddCommand("label add Atoms 0/{}".format(index))
            self.AddCommand("label textoffset Atoms {} {}".format(index,offset))
            self.AddCommand("label textformat Atoms {} {{ {} }}".format(index,label))



    def AddCommand(self,cmd):
        self.commands.append(cmd)

    def AddPeriodicBoundaryBox(self,boundary,color='black',width=1,style='solid'):
        # Boundary in the [[xlo,xhi],[ylo,yhi],[zlo,zhi]] format
        self.AddCommand("graphics 0 color {}".format(color))
        xlo,xhi = boundary[0]
        ylo,yhi = boundary[1]
        zlo,zhi = boundary[2]
        lines = [
            "{{ {} {} {} }} {{ {} {} {} }}".format(xlo, ylo, zlo, xlo, yhi, zlo),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xhi, ylo, zlo, xhi, yhi, zlo),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xlo, ylo, zlo, xhi, ylo, zlo),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xlo, yhi, zlo, xhi, yhi, zlo), # Bottom plane
            "{{ {} {} {} }} {{ {} {} {} }}".format(xlo, ylo, zhi, xlo, yhi, zhi),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xhi, ylo, zhi, xhi, yhi, zhi),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xlo, ylo, zhi, xhi, ylo, zhi),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xlo, yhi, zhi, xhi, yhi, zhi), # Top plane
            "{{ {} {} {} }} {{ {} {} {} }}".format(xlo, ylo, zlo, xlo, ylo, zhi),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xlo, yhi, zlo, xlo, yhi, zhi),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xhi, ylo, zlo, xhi, ylo, zhi),
            "{{ {} {} {} }} {{ {} {} {} }}".format(xhi, yhi, zlo, xhi, yhi, zhi)# Four pillars
        ]
        for line in lines:
            self.AddCommand("graphics 0 line {} width {} style {}".format( \
                line,width,style
            ))


    def Run(self,vmdlocation=None,dryrun=False):
        script = open(self.scriptFileName,"w")
        for cmd in self.commands:
            script.write(cmd)
            script.write("\n")
        script.close()

        if vmdlocation != None and not os.path.exists(vmdlocation) and not dryrun:
            output("In VMDInterface::Run(), the given path of VMD \"{}\" is invalid.".format(vmdlocation))
            vmdlocation = None
        else:
            try:
                vmdlocation = os.environ["VMD"]
            except:
                vmdlocation = None

        if vmdlocation == None and not dryrun:
            output("In VMDInterface::Run(), Cannot find the path of the VMD program. You have three options:")
            output("1. Provide the correct location of VMD explicitly when calling VMDInterface::Run(vmdlocation).")
            output("2. Write the location of VMD into an environment variable \"VMD\".")
            output("3. Call vmd yourself by \"vmd.exe -e {}\", where \"{}\" is the "
            "vmd script this program has created for you.".format(self.scriptFileName,self.scriptFileName))
            return False

        import subprocess
        cmd = [vmdlocation,"-e",self.scriptFileName]

        if not dryrun:
            vmdProcess = subprocess.Popen(cmd)
            vmdProcess.wait()
