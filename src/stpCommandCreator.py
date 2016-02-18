# -*- coding: utf-8 -*-

import json

class stpCommandCreator:
    """Class for creating SearchTermPosition json commands for a list of 
    da|ra dataset titles."""

    algorithm = "io.github.infolis.algorithm.SearchTermPosition"
    phraseSlop = 0
    
    def __init__(self, outputFile):
        self.outputFile = outputFile
        
    def writeToFile(self, commands):
        with open(self.outputFile, "w") as f:
            for command in commands:
                f.write(command)
            
    def createCommand(self):
        return json.dumps({"algorithm":self.algorithm,\
            "phraseSlop":self.phraseSlop}, sort_keys=True, indent=4)
            
class daraJsonParser:
    """Class for parsing the json response of a dara solr query."""
       
    def __init__(self, jsonIn, csvOut):
        self.jsonIn = jsonIn
        self.csvOut = csvOut
        
    def getDaraJson(self):
        return json.load(open(self.jsonIn, "r"))
        
    def parseDaraJson(self, json):
        for item in json.get("response").get("docs"):
            yield item

    def getTitleSet(self, jsonGeneratorObj):
        titles = set([])
        for item in jsonGeneratorObj:
            titles.add("".join(item.get("title_en", "")))
            titles.add("".join(item.get("title_de", "")))
        titles.remove("")
        return titles
        
    def writeCsv(self, data):
        with open(self.csvOut, "w") as f:
            f.write("\n".join(data).encode("utf-8"))
            
    def writeTitlesToCsv(self):
        self.writeCsv(self.getTitleSet(self.parseDaraJson(self.getDaraJson())))
        
    
if __name__=="__main__":
    parser = daraJsonParser(sys.argv[1], "./daraTitles.csv")
    parser.writeTitlesToCsv()
    
    cc = stpCommandCreator("./stpCall.json")
    cc.writeToFile(cc.createCommand())
