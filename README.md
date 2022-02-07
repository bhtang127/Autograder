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

Description: This grading assistant requires at least one CSV file input through `-i` and one folder input through `-d`. The CSV file should contain at least three columns `last name`, `first name` and `github username`. They are the assignments we want to grade. And the folder should contain all students' assignments, each in a subfolder named by his/her github id. This can be easily done through github [Classroom Assistant](https://github.com/education/classroom-assistant), where you can batch download assignments repo in required form.

User can also input a rule file from `-r` or `--rule`. It should be a python3 file containing some functions named like `rule_*` (names should start with the word "rule"). Those functions should take a str path as input, which refers to student's repo, then do some checking and return student's score. The function should return scores in string format `[student score] / [total score]`. For example `4.5 / 5`. And once `-r` is passed in, the grader will run all `rule_*` functions for every student.

Once the `autograder` is called. First it will check and print out which ids are in the id file but not in the directory (missing repo) and which ids are in the directory but not in the id file (will not be graded). Then it will ask the user to confirm. If input "y" or "Y" or just empty line, the autograder will continue. Otherwise it will stop. After confirming, if `-r` is passed in, the program will ask `Are there questions not covered by autograding rules (should we not autograde whole assignments)? (y/n)`. If negative, the grader will autograde all students' assignments. And when someone didn't get full scores, it will open his repo folder and ask `What should be the total score for this id`, `Any note for this is`, `Please confirm`. These questions will be asked for every student's repo if you didn't pass `-r` in or answered positive in question `Are there questions not covered by autograding rules`.

After grading every repo, it will update the records file in current directory named `[prefix]_scores.csv`, where *prefix* is passed in through `-p` (default: hw). And logging into log file specified by argument `-l` (default: scores.log). 

Don't worry that you might need to regrade students if the program accidentally exits. If the records CSV file is in the current directory, the program will only grade the students who has not yet be graded.


Example: `python3 autograder.py -i ../githubID.csv -d ../ds4ph/ds4ph\ homework\ 1-02-06-2022-09-09-24 --rule rules.py`



