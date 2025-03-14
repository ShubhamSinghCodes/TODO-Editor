import time
import jinja2
import ctypes
from os import system, name
import keyboard
from colorama import Fore, Style

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
environment = jinja2.Environment()
to_replace = ['─', '═', '║', '╔', '╗', '╚', '╝', '╟', '╠', '╢', '╣', '╶', ' => ', '#After ']
template = """╔{{"═"* (length)}}╗
║TODO:{{" "* (length-5)}}║
╠{{"═"* (length)}}╣{% for item in todos %}
║╶{{ item }}║
╟{{"─"* (length)}}╢{% endfor %}
║╶{{lastitem}}║
╚{{"═"* (length)}}╝
"""
template = environment.from_string(template)


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def render():
    global menu, pos, torender
    if torender:
        clear()
        print(f"{Style.RESET_ALL}Navigate with arrow keys (up and down arrows to move, right arrow to select.)")
        print(menu["head"])
        for ind, action in enumerate(menu["contents"]):
            if ind == pos:
                print(f"{Fore.BLUE} ->{action}{Fore.RESET}")
            else:
                print(f" ->{action}")

def handle(event):
    global torender, menu, pos
    if event == "Append":
        toinsert = input("Enter Todo item: ")
        for invalid in to_replace:
            toinsert = toinsert.replace(invalid, "")
        if toinsert not in ["Append", "Delete", "Read", "Replace", "Close", "", *contents]:
            contents.insert(0, toinsert)
        torender = False
    elif event == "Delete":
        menu = {"head": "Delete index:", "contents": contents}
        pos = 0
    elif event == "Read":
        clear()
        print(contents_raw)
        torender = False
        time.sleep(10)
    elif event == "Replace":
        replacables=[]
        for item in contents:
            for r in contents:
                if r != item:
                    replacables.append(f"{item} => {r}")
        menu = {"head": f"Replace index:\n{contents_raw}\n", "contents": replacables}
        pos = 0
    elif event == "Reorder":
        replacables=[]
        for item in contents:
            for r in contents:
                if r != item:
                    replacables.append(f"{item} => {contents.index(r)} #After {r}")
        menu = {"head": f"Reorder index:\n{contents_raw}\n", "contents": replacables}
        pos = 0
    elif event == "Close":
        quit()
    elif " #After " in event:
        items = event.split(" #After ")
        items = items[0].split(" => ")
        contents.insert(int(items[1]),contents.pop(contents.index(items[0])))
        torender = False
    elif " => " in event:
        items = event.split(" => ")
        temp = contents.index(items[1])
        contents[contents.index(items[0])] = items[1]
        contents[temp] = items[0]
        torender = False
    elif event in contents:
        contents.remove(event)
        torender = False


while True:
    with open(r"C:\Users\singh\Shubham and Kritika\Shubham\Python\_TODOS\TODO.txt", "r", encoding="utf8") as f:
        contents_raw = f.read()
        contents = contents_raw
        for item in to_replace:
            contents = contents.replace(item, "")
        contents = [item.strip() for item in contents.split("\n") if (item.strip() != 'TODO:' and item != "")]
    menu = {"head": "Action:", "contents": ["Append", "Delete", "Read", "Replace", "Reorder", "Close"]}
    pos = 0
    torender = True
    while torender:
        render()
        k = keyboard.read_key()
        if k == "down":
            pos += 1
            pos %= len(menu["contents"])
        elif k == "up":
            pos -= 1
            pos %= len(menu["contents"])
        if k == "right":
            handle(menu["contents"][pos])
        time.sleep(0.5)
    clear()
    length = max([len(item) for item in contents]) + 1
    todos = [item.ljust(length - 1) for item in contents[:-1]]
    lastitem = contents[-1].ljust(length - 1)
    with open(r"C:\Users\singh\Shubham and Kritika\Shubham\Python\_TODOS\TODO.txt", "w", encoding="utf8") as f:
        f.write(template.render(length=length, lastitem=lastitem, todos=todos))
