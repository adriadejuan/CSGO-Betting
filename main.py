from since import gamesSinceDate
from today import gamesToday

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def chooseOptions():
    print("Menu:")
    print("1: Games today.")
    print("2: Games since given date.")
    a = int(input("Select option: "))
    return a

def getDate():
    date = str(input("Enter date (YYYY-MM-DD format): "))
    return date

if __name__ == '__main__':
    a = chooseOptions()
    if a==1:
        gamesToday()
    elif a==2:
        dateBreak = getDate()
        gamesSinceDate(dateBreak)
    else:
        print("Incorrect parameter.")

    #
    dateBreak = "2021-10-18"
