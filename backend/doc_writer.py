from datetime import datetime

FILE = "../docs/updates.md"

def write_docs(summary):

    with open(FILE, "a") as f:
        f.write("\n\n")
        f.write(f"## Update {datetime.now()}\n")
        f.write(summary)