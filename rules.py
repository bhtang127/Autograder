import os

def rule_file_counts(dir):
    fs = os.listdir(dir)
    if 'notebook1.ipynb' in fs and 'document1.md' in fs and 'README.md' in fs:
        return "10 / 10"
    else:
        return "0 / 10"