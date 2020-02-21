# solr-import-export-json
A tool to import and export json documents from Apache SOLR

## Requirements
Python 3
```
python3 -v
Python 3.7.4
```

## Installation
```
make install
```
# Usage

use solr_export to export a solr_url to a file
```
venv/bin/python -m src.solr_export --help
Usage: solr_export.py [OPTIONS]

  Export solr collection to a file

Options:
  -s, --solr_url TEXT         SOLR URL, including the collection eg.
                              http://localhost:8983/solr/example
  -f, --file_path TEXT        Output File Path
  -r, --rows INTEGER          Number of rows per batch
  -e, --exclude_pattern TEXT  Exclude
  -d, --debug / --no-debug    Debug
  --help                      Show this message and exit.
```

use solr_import to import a file into a solr instance
```
venv/bin/python -m src.solr_import --help
Usage: solr_import.py [OPTIONS]

  Import to a solr collection from a file

Options:
  -s, --solr_url TEXT       SOLR URL, including the collection eg.
                            http://localhost:8983/solr/example
  -f, --file_path TEXT      Output File Path
  -r, --rows INTEGER        Number of rows per batch
  -d, --debug / --no-debug  Debug
  --help                    Show this message and exit.
```