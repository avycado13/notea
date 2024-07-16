import datetime
import os

DIR = os.getenv("NOTEA_DIR", "Notes")


def main():
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    # get current date
    current_date = datetime.date.today()
    msg = ""
    title = input("Title: ")
    print("Notes please!")
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            break
        msg = msg + line
    if not title:
        f = open(DIR + "/" + str(current_date) + ".md", "a+")
    elif title:
        f = open(DIR + "/" + title + ".md", "a+")
    f.write(
            "\n"
            + f"""+++
                title = {title if title else str(current_date)}
                date = {current_date}
                draft = true
                +++
            """
    )
    f.write("\n" + msg)
    f.close()


if __name__ == "__main__":
    main()
