from templateText import *
from structs import *

import os
import copy
import json
import pyratemp
import requests
import resvg_py
import argparse
import subprocess

def stripLogoURL(url):

    tokens = url.split('/')

    return tokens[-1]

def createDictFromArr(jsonArray):

    dict = {}

    for jsonObj in jsonArray:

        id = jsonObj['id']

        obj = copy.deepcopy(jsonObj)

        dict[id] = obj

    return dict


class processor:

    def checkImg(self, imgURL):

        imgName = stripLogoURL(imgURL).strip('.svg') + ".png"

        images = os.listdir(self.pngDir)

        if imgName not in images:

            svg = requests.get(imgURL)

            outpath = os.path.join(self.pngDir, imgName)

            png_bytes = resvg_py.svg_to_bytes(svg_string=svg.text, width=400, height=400, dpi=200)

            with open(outpath, "wb") as out:
                out.write(png_bytes)

    def getChars(self, charsJson):

        chars = []

        for id in charsJson:
            charVal = self.charDict[id]["name"]
            chars.append(charVal)

        return chars

    def addExtra(self, name, json):

        extra = []

        # handling weird blank extra items
        if json["extra"] == [] or json["extra"] is None:
            return name

        for extraEntry in json["extra"]:

            id = extraEntry
            extraDict = self.extras[id]

            extraName = extraDict["name"]

            if extraDict["type"] == 'DISTANCE':
                extraName += "\""

            extra.append(extraName)

            extraStr = ",".join(extra)

            return name + "(" + extraStr + ")"

    def createSkills(self, skillIDs):

        skills = []

        for skill in skillIDs:

            id = skill["id"]

            skillName = self.skillDict[id]["name"]

            if "extra" in skill:
                skillName = self.addExtra(skillName, skill)

            skills.append(skillName)

        if len(skills) > 0:
            return ",".join(skills)
        else:
            return ""

    def createEquips(self, equipIDs):

        equips = []

        for equipment in equipIDs:

            id = equipment["id"]

            equipName = self.equipDict[id]["name"]

            if "extra" in equipment:
                skillName = self.addExtra(equipName, equipment)

            equips.append(equipName)

        if len(equips) > 0:
            return ",".join(equips)
        else:
            return ""

    def getFactionColor(self, factionId):

        parentID = self.factions[factionId]['parent']

        factionColDict = {101:"PanO", 201:"YuJing", 301:"Ariadna", 401:"Haqqislam", 501:"Nomads", 601:"CA", 701:"Aleph", 801: "Tohaa", 901:"Mercs", 1001:"OTwelve", 1101:"JSA"}

        output = factionColDict[parentID]

        return output

    def createFTC(self, json, factionName):

        ftcData = ftChartStruct()
        ftcData.COUNT_DUO = json["spec"]['DUO']
        ftcData.COUNT_HARIS = json["spec"]['HARIS']
        ftcData.COUNT_CORE = json["spec"]['CORE']
        ftcData.FACTION = factionName

        if ftcData.COUNT_DUO == 256:
            ftcData.COUNT_DUO = "Unlimited"

        text = ""

        for ft in json['teams']:

            teamData = teamStruct()

            teamData.NAME = ft['name']
            types = ft['type']

            if len(types) > 1:
                teamData.FT_TYPES = ",".join(types)
            elif len(types) == 1:
                teamData.FT_TYPES = types[0]
            else:
                teamData.FT_TYPES = ""

            ftEntries = ""

            for unit in ft['units']:

                fteData = ftEntryStruct()

                fteData.NAME = unit['name']
                fteData.MIN = unit["min"]
                fteData.MAX = unit["max"]

                if len(unit["comment"]) > 0:
                    fteData.NAME += unit["comment"]

                fteText = self.fteTemplate(NAME=fteData.NAME, MIN=fteData.MIN, MAX=fteData.MAX)

                ftEntries += fteText + "\n"

            teamText = self.teamTemplate(NAME=teamData.NAME, FT_TYPES=teamData.FT_TYPES, FT_ENTRIES=ftEntries)

            text += teamText + "\n"

        output = self.fireteamChartTemplate(FACTION=ftcData.FACTION, FT_CONTENT=text, COUNT_DUO=ftcData.COUNT_DUO,
                                        COUNT_HARIS=ftcData.COUNT_HARIS, COUNT_CORE=ftcData.COUNT_CORE)

        return output

    def createOptions(self, json):

        output = ""

        for optionEntry in json:

            oData = optionStruct()

            oData.NAME = optionEntry["name"]
            oData.POINTS = optionEntry["points"]
            oData.SWC = optionEntry["swc"]

            # SKills

            skills = self.createSkills(optionEntry["skills"])

            # Equipment

            equipment = self.createEquips(optionEntry["equip"])

            # jam peripherals into the same field

            peripherals = []

            for peripheral in optionEntry["peripheral"]:

                periName = self.peripherals[peripheral["id"]]["name"]

                periStr = "Peripheral: " + periName

                if "q" in peripherals:

                    periQ = peripheral["q"]

                    if periQ > 1:
                        periStr += "(" + str(periQ) + ")"

                peripherals.append(periStr)

            peripheralsStr = ""

            if len(peripherals) > 0:
                peripheralsStr =  ",".join(peripherals)

            oData.SPECIAL = ",".join([skills,equipment,peripheralsStr])

            # weapons

            ranged = []
            melee = []



            for weapon in optionEntry["weapons"]:

                weaponDict = ""

                try:
                    weaponDict = self.weaponDict[weapon["id"]]

                except BaseException:
                    print("No-Entry Weapon caught, skipping")
                    continue

                weaponName = weaponDict["name"]

                if "extra" in weapon:
                    weaponName = self.addExtra(weaponName, weapon)

                if weaponDict["type"] == "CC":
                    melee.append(weaponName)
                else:
                    ranged.append(weaponName)

            oData.WEPM = ",".join(melee)
            oData.WEPR = ",".join(ranged)

            optText = self.optionTemplate(OPT_NAME=oData.NAME,
                              OPT_POINTS=oData.POINTS,
                              OPT_SWC=oData.SWC,
                              OPT_SPECIAL=oData.SPECIAL,
                              OPT_WEPR=oData.WEPR,
                              OPT_WEPM=oData.WEPM)
            optText += "\n"

            output += optText

        return output

    def createProfile(self, json, factionColor):

        pData = profileStruct()

        pData.NAME = "{" + json["name"] + "}"
        pData.AVA = json["ava"]
        if pData.AVA == -1:
            pData.AVA = "--"

        pData.BS = json["bs"]
        pData.CC = json["cc"]
        pData.PH = json["ph"]
        pData.WIP = json["wip"]
        pData.SIL = json["s"]
        pData.BTS = json["bts"]
        pData.ARM = json["arm"]
        pData.MOVA = json["move"][0]
        pData.MOVB = json["move"][1]
        pData.WOUNDS = json["w"]
        pData.FACTION = factionColor
        pData.TYPE = self.typeDict[json["type"]]["name"]

        # Check to see if the icon for this unit is already present, download it if not
        self.checkImg(json["logo"])
        pData.LOGO = stripLogoURL(json["logo"]).strip('.svg') + ".png"

        chars = self.getChars(json["chars"])

        if "Hackable" in chars:
            pData.HACK = "true"
        else:
            pData.HACK = "false"

        if "Regular" in chars:
            pData.TRAIN = "regular"
        elif "Irregular" in chars:
            pData.TRAIN = "irregular"
        elif "Peripheral" in chars:
            pData.TRAIN = "peripheral"

        if "Cube" in chars:
            pData.CUBE = "cube"
        elif "Cube 2.0" in chars:
            pData.CUBE = "cube2"
        else:
            pData.CUBE = "no"

        if "Impetuous" in chars:
            pData.IMPET = "true"
        else:
            pData.IMPET = "false"

        skillIDs = json["skills"]
        pData.SKILL = self.createSkills(skillIDs)

        equipIDs = json["equip"]
        pData.EQUIP = self.createEquips(equipIDs)

        return self.profileTemplate(NAME=pData.NAME,
                                    CLASS=pData.CLASS,
                                    MOVA=pData.MOVA,
                                    MOVB=pData.MOVB,
                                    CC=pData.CC,
                                    BS=pData.BS,
                                    PH=pData.PH,
                                    WIP=pData.WIP,
                                    ARM=pData.ARM,
                                    BTS=pData.BTS,
                                    WOUND=pData.WOUND,
                                    WTYPE=pData.WTYPE,
                                    HACK=pData.HACK,
                                    CUBE=pData.CUBE,
                                    SKILL=pData.SKILL,
                                    EQUIP=pData.EQUIP,
                                    FACTION=pData.FACTION,
                                    LOGO=pData.LOGO,
                                    TYPE=pData.TYPE,
                                    SIL=pData.SIL,
                                    AVA=pData.AVA,
                                    TRAIN=pData.TRAIN,
                                    IMPET=pData.IMPET)

    def updateExtras(self, json):

        for extra in json:

            if extra['id'] not in self.extras:

                self.extras[extra['id']]=extra

    def parseFactionJson(self, jsonData, factionID):


        # get faction specific dictionaries

        self.weaponDict = {}
        self.weaponDict = createDictFromArr(jsonData['filters']['weapons'])

        self.extras = {}
        self.extras = createDictFromArr(jsonData['filters']['extras'])

        self.skillDict = {}
        self.skillDict = createDictFromArr(jsonData['filters']['skills'])

        self.charDict = {}
        self.charDict = createDictFromArr(jsonData['filters']['chars'])

        self.peripherals = {}
        self.peripherals = createDictFromArr(jsonData['filters']['peripheral'])

        factionName = self.factions[factionID]["name"]

        print("Parsing Faction List: " + factionName)

        factionColor = self.getFactionColor(factionID)

        tex = ""

        if not self.typeDict:

            self.typeDict = createDictFromArr(jsonData['filters']['type'])

            self.classDict = createDictFromArr(jsonData['filters']['category'])

        for unit in jsonData['units']:

            # filter out mercs
            if int(unit['id'])>10000:
                continue

            unitTex = ""

            for troop in unit["profileGroups"]:

                troopTex = ""

                for profileData in troop["profiles"]:

                    profileTex = self.createProfile(profileData, factionColor)

                    troopTex += profileTex + "\n"

                optionTex = self.createOptions(troop["options"])

                newTroopTex = self.troopTemplate(TROOP_PROFILES=troopTex, TROOP_OPTIONS=optionTex)

                unitTex += newTroopTex + '\n'

            completeUnitTex = self.unitTemplate(UNIT_CONTENT=unitTex, UNIT_NAME=unit["name"])

            tex += completeUnitTex + "\n"

        FTC_tex = self.createFTC(jsonData["fireteamChart"], factionName)

        tex += FTC_tex

        self.checkImg(imgURL=self.factions[factionID]['logo'])
        logoName = stripLogoURL(self.factions[factionID]['logo'])
        logoName = logoName.strip('.svg') + ".png"


        tex = self.factionTemplate(FACTION=factionName, VERSION= jsonData['version'], LOGO = logoName, CONTENTS=tex)

        # LaTeX substituions
        tex = tex.replace('_','\\_')
        tex = tex.replace('&', '\\&')

        print("Done!")

        return tex

    def loadCachedArmyMeta(self, cachedIn):

        text = ""

        file = os.path.join(cachedIn,"metadeta.json")

        with open(file, 'r') as f:

            text = f.read()

        return text

    def loadCachedFaction(self,cachedIn, id):

        text = ""

        fn = str(id) + ".json"

        file = os.path.join(cachedIn,fn)

        with open(file,'r') as f:

            text = f.read()

        return text


    def __init__(self, set_outputDir, cacheOut, cachedIn, compileTex):
        self.outputDir = set_outputDir

        self.pngDir = os.path.join(self.outputDir, "logo")

        if not os.path.isdir(self.pngDir):
            os.mkdir(self.pngDir)

        self.jsonDir = ""

        if cacheOut:
            self.jsonDir = cacheOut

        # load metadata
        armyMetaData = {}

        if cachedIn:
            armyMetaData = self.loadCachedArmyMeta(cachedIn)
        else:
            armyMetaData = requests.get("https://api.corvusbelli.com/army/infinity/en/metadata", headers={'Origin': 'https://infinityuniverse.com/'}).text

            if cacheOut:

                fp = os.path.join(self.jsonDir,"metadata.json")

                with open(fp, 'w') as file:

                    file.write(armyMetaData)

            print("Metadata Loaded from CB API")

        jsonMeta = json.loads(armyMetaData)

        # dictionaries
        self.weaponDict = {}
        self.skillDict = {}
        self.equipDict = createDictFromArr(jsonMeta["equips"])
        self.factions = createDictFromArr(jsonMeta["factions"])
        self.extras =  {}
        self.peripherals = {}

        # templates
        self.factionTemplate = pyratemp.Template(factionTemplate)
        self.unitTemplate = pyratemp.Template(unitTemplate)
        self.troopTemplate = pyratemp.Template(troopTemplate)
        self.profileTemplate = pyratemp.Template(profileTemplate)
        self.optionTemplate = pyratemp.Template(optionTemplate)

        self.fireteamChartTemplate = pyratemp.Template(fireteamChartTemplate)

        self.teamTemplate = pyratemp.Template(teamTemplate)
        self.fteTemplate = pyratemp.Template(fteTemplate)

        # other dictionaries
        self.typeDict = {}
        self.charDict = {}
        self.classDict = {}

        print("Metadata Dictionaries Loaded")

        # Filter List
        excludeList = [901, 903, 907]

        # start parsing armies
        for faction in self.factions.values():

            factionId = faction['id']


            # filter out reinforcement/merc factions
            if '99' not in str(factionId) and factionId not in excludeList:

                factionData = {}

                if cachedIn:
                    factionData = self.loadCachedFaction(cachedIn, factionId)
                    print("Loaded Faction " + factionId + " from cache")
                else:
                    url = "https://api.corvusbelli.com/army/units/en/" + str(factionId)
                    factionData = requests.get(url, headers={'Origin': 'https://infinityuniverse.com/'}).text
                    print("Downloaded Faction " + str(factionId))
                    if cacheOut:

                        fn = str(factionId) + ".json"
                        path = os.path.join(self.jsonDir, fn)

                        with open(path, 'w') as f:

                            f.write(factionData)

                factionJson = json.loads(factionData)

                tex = self.parseFactionJson(factionJson, factionId)

                fn = self.factions[factionId]["name"] + ".tex"

                fn = fn.replace(' ', '_')

                file = os.path.join(self.outputDir, fn)

                with open(file, 'w') as f:
                    f.write(tex)
                    print(fn + " Written")

        # run pdftex
        if compileTex:
            misconfig = 0
            outputFiles = os.listdir(self.outputDir)
            outputTex = []

            for file in outputFiles:
                if ".tex" in file:
                    outputTex.append(file)

            styPath = os.path.join(self.outputDir, "sty")

            if os.path.isdir(styPath):
                files = os.listdir(styPath)

                if "InfinityPrinter.sty" not in files or "InfinityOptions.sty" not in files or "InfinityFT.sty" not in files:
                    misconfig+=1
                    print(".sty files not found")

            else:
                misconfig += 1
                print(".sty folder not found")

            iconPath = os.path.join(self.outputDir, "icons")
            if os.path.isdir(iconPath):
                files = os.listdir(iconPath)

                if ("peripheral.png" not in files or
                        "impetuous.png" not in files or
                        "hackable.png" not in files or
                        "cube2.png" not in files or
                        "regular.png" not in files or
                        "irregular.png" not in files):
                    misconfig+=1
                    print("icon files missing")

            else:
                misconfig += 1
                print("icon dir missing")

            if misconfig == 0:

                print("Starting LaTeX compilations")
                for file in outputTex:

                    pdfTexOut = subprocess.run(["pdflatex", file], capture_output=True, text=True, check=True)
                    print(pdfTexOut.stdout)

            else:

                print("LaTeX .sty files not detected - cancelling compilation")

    def __del__(self):
        print("Done Processing.")

if __name__ == "__main__":

    parser=argparse.ArgumentParser(prog="InfinityPrinter", description="Download Infinity Army Data and Print to PDF")

    parser.add_argument('output')
    parser.add_argument('-ci', help="Cached JSON Input Directory")
    parser.add_argument('-co', help="Cached JSON Output Directory")
    parser.add_argument('-t', help="Compile LaTeX with pdflatex",action='store_true')

    args = parser.parse_args()

    if os.path.isdir(args.output):
        print(f"Output Directory: {args.output}")
    else:
        raise NotADirectoryError(args.output)

    if args.ci and os.path.isdir(args.ci):
        print(f"Using Cached Input from: {args.output}")
    elif args.ci and not os.path.isdir(args.ci):
        raise NotADirectoryError(args.output)

    if args.co and os.path.isdir(args.co):
        print(f"Caching JSON data in: {args.output}")
    elif args.co and not os.path.isdir(args.co):
        raise NotADirectoryError(args.output)


    armyProcessor = processor(args.output, args.co, args.ci, args.t)