import datetime
import os

DIR = os.getenv("NOTEA_DIR","Notes")
PREFIX = os.getenv("NOTEA_PREFIX")
def main():
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    # get current date
    current_date = datetime.date.today()
    msg = ""
    print("Notes please!")
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        msg = msg + line
    if not os.path.exists(DIR+str(current_date)+".md"):
        prefix = True
    f = open(DIR+"/"+str(current_date)+".md" ,"a+")
    if prefix:
        f.write("\n"+PREFIX)
    f.write("\n"+msg)
    f.close()
if __name__ == '__main__':
    main()