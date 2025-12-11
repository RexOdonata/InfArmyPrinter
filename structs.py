class profileStruct:
    def __init__(self):
        self.NAME="name"
        self.CLASS=""
        self.MOVA="4"
        self.MOVB="4"
        self.CC="17"
        self.BS="12"
        self.PH="12"
        self.WIP="13"
        self.ARM="1"
        self.BTS="3"
        self.WOUND="1"
        self.WTYPE="VITA"
        self.HACK="false"
        self.CUBE="cube"
        self.SKILL=""
        self.EQUIP=""
        self.FACTION=""
        self.LOGO=""
        self.TYPE="LI"
        self.AVA="1"
        self.TRAIN="regular"
        self.IMPET="false"

class optionStruct:
    def __init__(self):
        self.NAME=""
        self.POINTS="0"
        self.SWC="0"
        self.SPECIAL=""
        self.WEPR=""
        self.WEPM=""

class ftChartStruct:
    def __init__(self):
        self.COUNT_DUO=1
        self.COUNT_HARIS=1
        self.COUNT_CORE=0
        self.FACTION="Faction"

class teamStruct:
    def __init__(self):
        self.NAME=""
        self.FT_TYPES=""

class ftEntryStruct:
    def __init__(self):
        self.NAME=""
        self.MIN=0
        self.MAX=0