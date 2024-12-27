import datetime
import os
import argparse
from rich.prompt import Prompt
import subprocess
import tempfile

# Default directory for notes
DEFAULT_DIR:str = os.getenv("NOTEA_DIR", "Notes")

# Set up argument parser
parser:argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str, default=DEFAULT_DIR)
args:argparse.Namespace = parser.parse_args()

def edit_text(initial_text:str = '') -> str:
    editor:str = os.getenv('EDITOR', 'vi')  # Default to 'vi' if $EDITOR is not set
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.tmp') as temp_file:
        temp_file.write(initial_text)
        temp_file.flush()
        try:
            subprocess.run([editor, temp_file.name], check=True)
        except FileNotFoundError:
            print(f"Editor '{editor}' not found.")
        except subprocess.CalledProcessError:
            print(f"An error occurred while trying to open the file with {editor}.")
        
        temp_file.seek(0)
        return temp_file.read()

def y_n_question(question):
    response = Prompt.ask(f"{question} (y/n)", choices=["y", "n"])
    return response.lower() == "y"

def main() -> None:
    # Determine directory
    notes_dir:str = args.dir
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    # Get current date
    current_date:datetime.date = datetime.date.today()

    # Determine draft status
    draft:str = 'true' if y_n_question("Draft?") else 'false'

    # Get note title and content
    title:str = Prompt.ask("Title")
    print("Notes please!")
    msg:str = edit_text(initial_text='')

    # Define filename and path
    if not title:
        filename:str = f"{current_date}.md"
    else:
        filename = f"{title}.md"
    filepath:str = os.path.join(notes_dir, filename)

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
    print("Done!")

if __name__ == "__main__":
    main()
