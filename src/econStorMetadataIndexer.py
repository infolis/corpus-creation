# -*- coding: utf-8 -*-

from MetadataIndexer import MetadataIndexer
import sys

class econStorMetadataIndexer(MetadataIndexer):
    """Class for parsing econStor metadata."""

    def getDcInfo(self, metadata):
        for dc in metadata.getchildren():
            yield {dc.tag : dc.text}


def usage():
    print "usage: econStorMetadataIndexer.py <jsonTagFile> <logFile> <metaDir> <targetFile>"
    
    
if __name__=="__main__":
    try:
        tags, log, metaDir, target = sys.argv[1:]
    except ValueError:
        usage()

    indexer = econStorMetadataIndexer(tags, log)
    indexer.createMetaDicts(metaDir)
    print "created indices for elements: "
    for key in indexer.tagDictionaries.keys():
        print key
    indexer.exportMetaDicts(target)
