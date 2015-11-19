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
A json file like this can be used to specify the documents to select for creating a corpus:
```
{
    "picklePath":"./ssoarMetadata.pickle",
    "intersectionIntra":"False",
    "intersectionInter":"True",
    "select":
        {
            "subject_methods":["empirisch-quantitativ"],
            "language_None":["de"],
            "contributor_corporateeditor":["Deutsche Gesellschaft für Soziologie (DGS)"]
        },
    "sample":
        {
            "size":"100"
        },
    "createLinks":
        {
            "source":"../pdf",
            "target":"../subsets/de_empirisch-quantitativ_dgs_100"
        } 
}
```
```
picklePath: location of the index file created by either econStorMetadataIndexer or ssoarMetadataIndexer, e.g. ./ssoarMetadata.pickle
intersectionIntra: if the tags of one category are to be connected with boolean OR (meaning that documents having any of these tags should be selected), intersectionIntra should be set to False. Else, they will be connected with AND (meaning that only documents having all of these tags should be selected). 
intersectionInter: intersectionInter defines how tag sets of different categories are to be connected. If set to True, documents must match all of the specified categories, if set to False, they only need to match any of the given categories.
```
Example: ...

```
select: command for selecting documents
sample (optional): create a random sample of the given size from all selected documents
createLinks (optional): create symbolic links to the created sample on the filesystem (linux only!)
```

Create a subcorpus with given specifications
---------------------------------------------
Call CorpusCreator with the json file:
```
python CorpusCreator.py <jsonFile>
```
```
jsonFile: path to the json file, e.g. ./examples/ssoarSample.json
```
