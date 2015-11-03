# -*- coding: utf-8 -*-

from MetadataIndexer import MetadataIndexer
             
class ssoarMetadataIndexer(MetadataIndexer):
    """Class for parsing ssoar metadata."""
       
    def getDcInfo(self, metadata):
        for dc in metadata.getchildren():
            yield {str(dc.attrib.get("element")) + "_" + str(dc.attrib.get("qualifier")) : dc.text}
                           
 
if __name__=="__main__":
    indexer = ssoarMetadataIndexer("../ssoarTags.json", "./ssoarMetaHandler.log")
    indexer.createMetaDicts("../ssoarMeta/")
    indexer.exportMetaDicts("../ssoarMetadata.pickle")
    indexer.exportTagLists("../tags.pickle")
