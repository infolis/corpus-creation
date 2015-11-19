corpus-creation
================
Tools for creating custom subsets of a given corpus


Parse metadata and write to an index
-------------------------------------

For econStor metadata:
```
python econStorMetadataIndexer.py ./resources/econStorTags.json <logFile> <metaDir> <targetFile>
```

For SSOAR metadata:

```
python ssoarMetadataIndexer.py ./resources/ssoarTags.json <logFile> <metaDir> <targetFile>
```
```
logFile: path to a file to use as log, e.g. ./metaIndexer.log

metaDir: path to the metadata dump, e.g. ./ssoar_meta

targetFile: path to a file to use as index, e.g. ./ssoarMetadata.pickle
```

Create a json file specifying which documents from the corpus to select and which actions to perform on them
-------------------------------------------------------------------------------------------------------------
...


Create a subcorpus with given specifications
---------------------------------------------
...

