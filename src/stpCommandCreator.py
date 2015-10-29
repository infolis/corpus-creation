# -*- coding: utf-8 -*-

import json

class stpCommandCreator:
    """Class for creating SearchTermPosition json commands for a list of 
    da|ra dataset titles."""

    algorithm = "io.github.infolis.algorithm.SearchTermPosition"
    phraseSlop = 0
    jsonIn = ""
    outputFile = ""
    searchQueries = []
    
    def __init__(self, jsonIn, outputFile):
        self.jsonIn = jsonIn
        self.outputFile = outputFile
        
    def writeToFile(self, commands):
        with open(self.outputFile, "w") as f:
            for command in commands:
                f.write(command)
            
    def createCommand(self, searchTerms):
        for term in searchTerms:
            self.searchQueries.append(term)
        return json.dumps({"algorithm":self.algorithm,\
            "phraseSlop":self.phraseSlop,\
            "searchQueries":self.searchQueries}, sort_keys=True, indent=4)
            
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
        return titles
    
if __name__=="__main__":
    c = stpCommandCreator("./dara_datasets_with_oecd.json",\
    "./stpCmdDaraTitles.json")
    c.writeToFile(c.createCommand(c.getTitleSet(c.parseDaraJson(c.getDaraJson()))))
