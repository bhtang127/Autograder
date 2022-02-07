import os
import re

# def rule_file_counts(dir):
#     fs = os.listdir(dir)
#     if 'notebook1.ipynb' in fs and 'document1.md' in fs and 'README.md' in fs:
#         return "10 / 10"
#     else:
#         return "0 / 10"

def rule_quiz_answer(dir):
    total_score, cur = 3, 3
    try:
        with open(os.path.join(dir, "README.md")) as f:
            raw_text = "".join(f.readlines())
            if not re.findall("\[x\] The Teams Site", raw_text):
                cur -= 0.5
            if not re.findall("\[x\] Send a chat over Teams", raw_text):
                cur -= 0.5
            if not re.findall("\[x\] Weekly projects", raw_text):
                cur -= 0.5
            if not re.findall("\[x\] Mondays at 5 PM", raw_text):
                cur -= 0.5
            if not re.findall("\[x\] Github classroom", raw_text):
                cur -= 0.5
            if not re.findall("\[x\] On the General channel on the Teams site", raw_text):
                cur -= 0.5
        return "%.2f / %.2f"%(cur, total_score)
    except:
        return "0 / %.2f"%(total_score)
    

def rule_notebook_4_plus_4(dir):
    total_score, cur = 2, 2
    try:
        with open(os.path.join(dir, "notebook1.ipynb")) as f:
            raw_text = "".join(f.readlines())
            if not re.findall('"cell_type": "code"', raw_text):
                cur -= 2
            elif not re.findall('"8[\n]*"', raw_text) and not re.findall('"8\.[0]+"', raw_text):
                cur -= 2
        return "%.2f / %.2f"%(cur, total_score)
    except:
        return "0 / %.2f"%(total_score)
    

def rule_notebook_text_cell(dir):
    total_score, cur = 1, 1
    try:
        with open(os.path.join(dir, "notebook1.ipynb")) as f:
            raw_text = "".join(f.readlines())
            if not re.findall('"cell_type": "markdown"', raw_text) \
                and not re.findall('"cell_type": "raw"', raw_text):
                cur -= 1
        return "%.2f / %.2f"%(cur, total_score)
    except:
        return "0 / %.2f"%(total_score)
    
    
def rule_markdown_title(dir):
    total_score, cur = 1, 1
    try:
        with open(os.path.join(dir, "document1.md")) as f:
            raw_text = "".join(f.readlines())
            if not re.findall(r'[ \t]*#[ \t]*[Ss][Ee][Cc]', raw_text):
                cur -= 1
        return "%.2f / %.2f"%(cur, total_score)
    except:
        return "0 / %.2f"%(total_score)


def rule_markdown_subtitle(dir):
    total_score, cur = 1, 1
    try:
        with open(os.path.join(dir, "document1.md")) as f:
            raw_text = "".join(f.readlines())
            if not re.findall(r'[ \t]*##[ \t]*[Ss]', raw_text):
                cur -= 1
        return "%.2f / %.2f"%(cur, total_score)
    except:
        return "0 / %.2f"%(total_score)


def rule_markdown_bold_text(dir):
    total_score, cur = 1, 1
    try:
        with open(os.path.join(dir, "document1.md")) as f:
            raw_text = "".join(f.readlines())
            if not re.findall('\*\*[a-zA-Z0-9_,\.!\- \t]+\*\*', raw_text)\
               and not re.findall('__[a-zA-Z0-9_,\.!\- \t]+__', raw_text):
                cur -= 1
        return "%.2f / %.2f"%(cur, total_score)
    except:
        return "0 / %.2f"%(total_score)


def rule_markdown_italicized_text(dir):
    total_score, cur = 1, 1
    try:
        with open(os.path.join(dir, "document1.md")) as f:
            raw_text = "".join(f.readlines())
            if not re.findall('[^\*]\*[a-zA-Z0-9_,\.!\- \t]+\*', raw_text)\
               and not re.findall('[^_]_[a-zA-Z0-9_,\.!\- \t]+_', raw_text):
                cur -= 1
        return "%.2f / %.2f"%(cur, total_score)
    except:
        return "0 / %.2f"%(total_score)