import datetime
import os
import argparse
from rich.prompt import Prompt

# Default directory for notes
DEFAULT_DIR = os.getenv("NOTEA_DIR", "Notes")

# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str, default=DEFAULT_DIR)
args = parser.parse_args()

def y_n_question(question):
    response = Prompt.ask(f"{question} (y/n)", choices=["y", "n"])
    return response.lower() == "y"

def main():
    # Determine directory
    notes_dir = args.dir
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    # Get current date
    current_date = datetime.date.today()

    # Determine draft status
    draft = 'true' if y_n_question("Draft?") else 'false'

    # Get note title and content
    title = Prompt.ask("Title")
    print("Notes please!")
    lines = []
    while True:
        try:
            line = Prompt.ask()
        except EOFError:
            break
        else:
            lines.append(line)
    msg = "\n".join(lines)

    # Define filename and path
    if not title:
        filename = f"{current_date}.md"
    else:
        filename = f"{title}.md"
    filepath = os.path.join(notes_dir, filename)

    # Write note to file
    with open(filepath, "a+") as f:
        f.write(
            "\n"
            + f"""+++
title = "{title if title else str(current_date)}"
date = {current_date}
draft = {draft}
+++
"""
        )
        f.write("\n" + msg)

if __name__ == "__main__":
    main()
