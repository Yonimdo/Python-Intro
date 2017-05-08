from collections import defaultdict
from pathlib import Path
import sys


if len(sys.argv)>1:
    print("\n\nPresenting files from: "+sys.argv[1]+"\n\n------------------\n")
    folder = Path(sys.argv[1])
else:
    print("Presenting files from: local folder\n\n------------------\n")
    folder = Path(".")

def create_file_date():
    return {
        'Total Size': 0,
        'Count': 0,
    }

def main():
    files = defaultdict(create_file_date)
    for f in folder.iterdir():
        if f.is_file():
            f_type = files[str(f).split(".")[-1]] if "." in str(f) else files["."]
            f_type['Total Size'] += f.stat().st_size
            f_type['Count'] += 1
    for f_key in sorted(files):
        print("{:7} : {:<3} {:20}".format(f_key, files[f_key]['Count'], files[f_key]['Total Size']))


main()
