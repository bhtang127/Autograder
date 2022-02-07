# Autograder
This is a grading assistant for course ds4ph. 

Requirement: pandas

```
Usage: python3 autograder.py [-h] [-i ID] [-d DIRECTORY] [-r RULE] [-p PREFIX] [-l LOG]

optional arguments:
  -h, --help            show this help message and exit
  -i ID                 Path to the CSV file containing students' first name, last name and
                        github username
  -d DIRECTORY          Path to the folder containing all assignments
  -r RULE, --rule RULE  Path to the file containing all autograding rules. It can be none
  -p PREFIX, --prefix PREFIX
                        The name of the file with scores will be prefix_scores.csv, this file
                        will be generated in your current directory
  -l LOG, --log LOG     The name and path for the logging file (default: scores.log)
```


