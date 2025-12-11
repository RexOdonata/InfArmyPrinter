factionTemplate = """
\\documentclass{report}
\\usepackage[margin=1cm]{geometry}
\\usepackage{hyperref}

\\setlength{\parindent}{0pt}

\\input{sty/InfinityPrinter.sty}
\\input{sty/InfinityOptions.sty}
\\input{sty/InfinityFT.sty}

\\begin{document}
	
\\chapter*{@!FACTION!@}
\\large{Ver: @!VERSION!@}
\\begin{center}
\\frame{\\includegraphics[width=8cm]{logo/@!LOGO!@}}
\\end{center}
\\newpage
$!CONTENTS!$	
	
\\end{document}

"""

fireteamChartTemplate = """
\\section{Fireteam Chart - @!FACTION!@}
\\begin{itemize}
\\item \\textbf{DUO}: @!COUNT_DUO!@
\\item \\textbf{HARIS}: @!COUNT_HARIS!@
\\item \\textbf{CORE}: @!COUNT_CORE!@
\\end{itemize}
$!FT_CONTENT!$
"""

fteTemplate = """
\\ftEntry[fteName={@!NAME!@}, fteMin=@!MIN!@, fteMax=@!MAX!@]
"""

optionTemplate = """
\\option[oName=@!OPT_NAME!@,
 oPoints=@!OPT_POINTS!@,
  oSWC=@!OPT_SWC!@,
   oSpecial={$!OPT_SPECIAL!$},
    oWeaponMel={$!OPT_WEPM!$},
	oWeaponRng={$!OPT_WEPR!$}]
"""

profileTemplate = """
<!--(set_escape)-->
  None
<!--(end)-->
\\profile[pName=$!NAME!$, 
	pClass=@!CLASS!@, 
	pType=@!TYPE!@, 
	pMOVa=@!MOVA!@, 
	pMOVb=@!MOVB!@, 
	pCC=@!CC!@, 
	pBS=@!BS!@, 
	pPH=@!PH!@, 
	pWIP=@!WIP!@, 
	pARM=@!ARM!@,
	pSIL=@!SIL!@,
	pBTS=@!BTS!@,
	pWounds=@!WOUND!@,
	pWoundType=@!WTYPE!@,
	pHack=@!HACK!@,
	pCube=@!CUBE!@,
	pSkill={$!SKILL!$},
	pEquipment={$!EQUIP!$},
	pFaction=@!FACTION!@,
	pLogo=@!LOGO!@,
	pAVA=@!AVA!@,
	pTrain=@!TRAIN!@,
	pImpet=@!IMPET!@]
"""

teamTemplate = """
$!FT_ENTRIES!$
\\fireteam[teamName=$!NAME!$, teamTypes={$!FT_TYPES!$}]
\\vspace{1cm}
"""

troopTemplate = """
<!--(set_escape)-->
  None
<!--(end)-->
\\begin{minipage}{\\textwidth}
$!TROOP_PROFILES!$
\\header
$!TROOP_OPTIONS!$
\\end{minipage}
"""


unitTemplate = """
\\section{$!UNIT_NAME!$}
$!UNIT_CONTENT!$
\\newpage
"""