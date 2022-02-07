import os
import sys
import subprocess
import logging
import argparse
from sys import platform
import pandas as pd


def explore(path):
    # explorer would choke on forward slashes
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    path = os.path.normpath(path)
    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
        

def open_folder(dir):
    """Open folder `dir` in system GUI
    Args:
        dir (str): folder directory to open
    """
    if platform.startswith("linux"):
        os.system("nautilus " + dir)
    elif platform == "darwin":
        os.system("open " + dir)
    else:
        explore(dir)


if __name__ ==  "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", type=str, metavar="ID",
        help="Path to the CSV file containing students' first name, last name and github username"
    )
    parser.add_argument(
        "-d", type=str, default="./", metavar="DIRECTORY",
        help="Path to the folder containing all assignments"
    )
    parser.add_argument(
        "-r", "--rule", type=str,
        help="Path to the file containing all autograding rules. It can be none"
    )
    parser.add_argument(
        "-p", "--prefix",  type=str, default="hw",
        help="The name of the file with scores will be prefix_scores.csv, this file will be generated in your current directory"
    )
    parser.add_argument(
        "-l", "--log",  type=str, default="scores.log",
        help="The name and path for the logging file (default: scores.log)"
    )
    args = parser.parse_args()
    
    
    # logging config
    logging.basicConfig(filename=args.log, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("Starting Scoring!")
    
    
    # creating the file storing scores
    if not args.i or not os.path.exists(args.i):
        raise ValueError("Id Files Not Found")
    
    records_dir = args.prefix + "_scores.csv"
    id_name = pd.read_csv(args.i)
    id_name["last name"] = id_name["last name"].str.capitalize()
    id_name = id_name.sort_values("last name")
    records = pd.DataFrame({
        "last name": id_name["last name"], 
        "first name": id_name["first name"], 
        "github username": id_name["github username"], 
        "score": None,
        "note": ""
    })
    if os.path.exists(records_dir):
        records_old = pd.read_csv(records_dir, dtype={"note": str}).sort_values("last name")
        # if there is recording exists, merge that version in
        # and do not re-score
        if "score" in records_old:
            try:
                records = pd.merge(
                    id_name[["last name", "first name", "github username"]],
                    records_old,
                    how="left",
                    on=["last name", "first name", "github username"]
                ).sort_values("last name")
                logging.info("Merged existing records")
            except:
                pass
    
    records.to_csv(records_dir, index=False)  # initial save
    
    
    # scoring and recording student one by one
    if not args.d or not os.path.isdir(args.d):
        raise ValueError("Assignments Not Found")
    
    print("Starting Grading Process ----\n")
    
    ## checking which ids are not in the folder and which ids 
    ## are in the folder but not in records
    id_in_records = records["github username"].to_list()
    id_in_directory = [
        gid for gid in os.listdir(args.d) if os.path.isdir(os.path.join(args.d, gid))
    ]
    
    d_n_r = [gid for gid in id_in_directory if gid not in id_in_records]
    print("Following ids in assignments directory will not be graded (n=%d): "%(len(d_n_r)))
    logging.info("Following ids in assignments directory will not be graded (n=%d): "%(len(d_n_r)))
    print(", ".join(d_n_r))
    logging.info(", ".join(d_n_r))
    print()
    
    r_n_d = [gid for gid in id_in_records if gid not in id_in_directory]
    print("Following ids are not found in assignments directory (n=%d): "%(len(r_n_d)))
    logging.info("Following ids are not found in assignments directory (n=%d): "%(len(r_n_d)))
    print(", ".join(r_n_d))
    logging.info(", ".join(r_n_d))
    print()
    
    assigments = [gid for gid in id_in_records if gid in id_in_directory]
    print("Will begin scoring %d assingments\n"%(len(assigments)))
    logging.info("Will begin scoring %d assingments\n"%(len(assigments)))

    confirm = input("Please Confirm (y/n): ")
    if confirm.strip() and not confirm.lower().strip().startswith("y"):
        logging.error("Stop by user")
        sys.exit("Stop by user")
    
    # start grading: (AUTOGRADING: whether autograde all questions)
    if args.rule and os.path.exists(args.rule):
        sys.path.append(os.path.dirname(args.rule))
        rules = __import__(os.path.basename(args.rule).split(".")[-2])
        rule_names = [f for f in dir(rules) if f.lower().startswith("rule")]
        auto = input("\nAre there questions not covered by autograding rules (should we not autograde whole assignments)? (y/n) ")
        if auto.strip() and not auto.lower().strip().startswith("y"):
            AUTOGRADING = True
        else:
            AUTOGRADING = False
        print()
    else:
        rule_names = []
        AUTOGRADING = False
    
    for i, gid in enumerate(id_in_records):
        if gid not in id_in_directory:
            continue
        print("Start grading id `%s` (%d out of %d):"%(gid, i+1, len(assigments)))
        path_i = os.path.join(args.d, gid)
        score_i, full_score, note_i = 0, 0, ""
        for fn in rule_names:
            score_str = getattr(rules, fn)(path_i)
            print("  Checking %s: %s"%(fn, score_str))
            score_i += float(score_str.split("/")[0])
            full_score += float(score_str.split("/")[1])
        if AUTOGRADING and score_i > 0 and score_i == full_score:
            print("Total score for id %s is %.1f / %.1f\n"%(gid, score_i, full_score))
            records.at[i, "score"] = score_i
        else:
            open_folder(path_i.replace(" ", "\ "))
            confirm = False
            while not confirm:
                score_i = input("What should be the total score for id %s: "%(gid))
                note_i = input("Any note for id %s? Please enter: "%(gid))
                confirm = input("Please Confirm (y/n): ")
                if confirm.strip() and not confirm.lower().strip().startswith("y"):
                    confirm = False
                else:
                    confirm = True
            records.at[i, "score"] = score_i
            records.at[i, "note"] = str(note_i)
            print()
        logging.info(",  ".join([
            records.at[i, "last name"], records.at[i, "first name"], gid, str(score_i), str(note_i)
        ]))
        records.to_csv(records_dir, index=False)
        
    print("Grading Successful!")
    logging.info("Success")
        
        
        
    