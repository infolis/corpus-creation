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
For selecting documents, a picklePath must be given that points to the index file created by either econStorMetadataIndexer or ssoarMetadataIndexer. If the tags of one category are to be connected with boolean OR (meaning that documents having any of these tags should be selected), intersectionIntra should be set to False. Else, they will be connected with AND (meaning that only documents having all of these tags should be selected). Analogical, intersectionInter is used to define the connector of tags in different categories. If set to True, documents having a combination of the tags are selected, if set to False, all documents having any of the tags are selected. 

Example:

Possible operations are 
- select:
- sample:
- createLinks:


Create a subcorpus with given specifications
---------------------------------------------
Call CorpusCreator with the json file:
```
python CorpusCreator.py <jsonFile>
```
```
jsonFile: path to the json file, e.g. ./examples/ssoarSample.json
```
