# -*- coding: utf-8 -*-

import os
import random
import cPickle as pickle

class CorpusCreator():
    """Class for creating a subcorpus of the given corpus. 
    Features: 
    1. retrieve list of documents having specified keywords
    2. create sample of fixed size (random or arbitrary sample)
    3. copy corresponding documents (metadata or pdf) to specified location
    """

    def __init__(self, source):
        self.source = source
        
    def copyNFiles(self, target, n):
        """Copy a specified number of n files to target."""
        for filename in os.listdir(self.source)[:n+1]:
            shutil.copy(os.path.join(self.source, filename), target)
            
    def copyFiles(self, target, filenames):
        """Copy a list of filenames from corpus to target."""
        for filename in filenames:
            shutil.copy(os.path.join(self.source, filename), target)
            
    def selectRandomFiles(self, n):
        """Create a sample of n randomly selected filenames."""
        selectedFilenames = set([])
        filenames = os.listdir(self.source)
        # random choice may choose the same file multiple times
        # thus, do not perform choice operation n times but instead perform
        # operation until n filenames are selected
        while len(selectedFilenames) < size:
            selectedFilenames.add(os.path.join(self.source, random.choice(filenames)))
        return selectedFilenames
   
    def loadMetadata(self, picklePath):
        """Unpickle metadata stored in picklePath."""
        pFile = open(picklePath, "r")
        data = pickle.load(pFile)
        pFile.close()
        return data
    
    def intersect(self, nestedList):
        return list(set.intersection(*map(set, nestedList)))
        
    def union(self, nestedList):
        return list(set.union(*map(set, nestedList)))
    
    def getFilenamesHavingTags(self, tags, dictionary, function):
        matchList = [dictionary.get(tag) for tag in tags]
        try:
            return function(matchList)
        # only one list = one category of tags specified
        except TypeError:
            return matchList
          
    def select(self, data, tagLists, intersectionIntra=True, intersectionInter=True):
        """Select all filenames having the specified tags. 
        If intersection flag is set (default), only entries having all specified
        tags are returned. Else, a union of entries having at least one of the 
        tags is returned. Intra: tags inside of one category, inter: tags of 
        different categories."""
        matches = []
        function = self.intersect
        if not intersectionIntra:
            function = self.union
        # number of dictionaries in data matches number of tag lists
        # so does the order
        for i in range(len(data)):
            if tagLists[i]:
                matches.append(self.getFilenamesHavingTags(tagLists[i], data[i], function))

        function = self.intersect
        if not intersectionInter:
            function = self.union
        
        try:
            return function(matches)
        # only one list = one category of tags specified
        except TypeError:
            return matches

        
if __name__=="__main__":
    picklePath = "./metadata.pickle"
    
    subjectTags = ["C00",\
    "empirisch-deskriptive Analyse",\
    "empirische Analyse", "Empirische Analyse", "empirische Analysen",\
    "Empirical Analysis", "empirical analysis",\
    "Empirical Analyses", "Empirical Analysis (Firm Panel)",\
    \
    "Empirische Forschung", "empirische Forschung", \
    "Empirische Bildungsforschung", "empirische Wirtschafts- und Sozialforschung",\
    "empirische Sozialforschung", "Empirische Kriminalitätsforschung",\
    "Empirical research", "empirical research", "Empirical Research",\
    "Empirical educational research", "empirical crime research",\
    "empirical economic and social research", "empirical accounting research",\
    "power empirical research",\
    \
    "Empirische Untersuchung", "empirische Untersuchung",\
    "Empirical investigation", "Empirical Investigation",\
    "empirical studies", "Empirical studies", "Empirical Studies",\
    \
    "empirische Überprüfung", "empirical test", "Empirical Test",\
    "Empirical Validation", "empirical validation", "empirical evaluation",\
    "empirical test of the theory of the firm",\
    \
    "Empirische Methode", "empirical methods", "empirical methodology",\
    "empirical macroeconomic methodology", "Empirical and Theoretical Methods",\
    \
    "Quantitative Empirie", "qualitative Empirie", "Empirie",\
    "Empirical", "empirical", "Empirics", "empiricism",\
    "empirical work", "empirical content",\
    "empirical evidence", "Empirical Evidence",\
    "Empirical Example",\
    "empirical synthesis",\
    \
    "empirical models", "empirical modelling", "empirical modeling",\
    "empirical model specification",\
    \
    "empirische Mikroökonomik", "empirical macroeconomics",\
    "Empirical economics", "empirical economics", "Empirical finance",\
    \
    "Empirische Befragung",\
    \
    "Theorie und Empirie der personellen Einkommensverteilung",\
    "Literaturempirie", "Empirical typology", ]

    #typeTags = ["doc-type:article", "doc-type:contributionToPeriodical",\
    #"doc-type:doctoralThesis", "doc-type:bookPart"] 
    
    typeTags = []
    ppnIdTags = []
    langTags = ["eng", "deu"]
    dateTags = []
    relationTags = []
    miscTags = []
    # boolean OR for tags in one category (e.g. subject tags) but AND for 
    # combination of tags of different categories
    intersectionIntra = False
    intersectionInter = True
    creator = CorpusCreator("")
    
    print creator.select(creator.loadMetadata(picklePath), [subjectTags, typeTags,\
    ppnIdTags, langTags, dateTags, relationTags, miscTags],\
    intersectionIntra, intersectionInter)
        
