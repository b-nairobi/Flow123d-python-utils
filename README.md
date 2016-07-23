# Cobertura Report Merger

Takes file in cobertura format merges them to one combined report.

## Usage
```
Usage: coverage_merge_script.py [options] [file1 file2 ... filen]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o FILE, --output=FILE
                        output file xml name
  -p FILE, --path=FILE  xml location, default current directory
  -l LOGLEVEL, --log=LOGLEVEL
                        Log level DEBUG, INFO, WARNING, ERROR, CRITICAL
  -f, --filteronly      If set all files will be filtered by keep rules
                        otherwise all given files will be merged and filtered.
  -s SUFFIX, --suffix=SUFFIX
                        Additional suffix which will be added to filtered
                        files so they original files can be preserved
  -k NAME, --keep=NAME  preserves only specific packages. e.g.:
                        'python merge.py -k src.la.*'
                        will keep all packgages in folder src/la/ and all
                        subfolders of this folders.
                        There can be mutiple rules e.g.:
                        'python merge.py -k src.la.* -k unit_tests.la.'
                        Format of the rule is simple dot (.) separated names
                        with wildcard (*) allowed, e.g:
                        package.subpackage.*

If no files are specified all xml files in current directory will be selected.
Useful when there is not known precise file name only location
```
