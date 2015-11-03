# -*- coding: utf-8 -*-

from MetadataIndexer import MetadataIndexer

class econStorMetadataIndexer(MetadataIndexer):
    """Class for parsing econStor metadata."""

    def getDcInfo(self, metadata):
        for dc in metadata.getchildren():
            yield {dc.tag : dc.text}

if __name__=="__main__":
    indexer = econStorMetadataIndexer("../econStorTags.json", "./econStorMetadataIndexer.log")
    indexer.createMetaDicts("../econStorMeta/")
    indexer.exportMetaDicts("../econStorMetadata.pickle")
    indexer.exportTagLists("../econStorTags.pickle")
