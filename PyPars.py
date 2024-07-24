# упорядоченная файлоориентированная автоматизация ТУ-9
import pyautogui #+pip install Pillow --upgrade       pip install opencv-python для pyautogui.locateOnScreen('link.png', region=(x, y-30, 600, 55), confidence=0.95)"
import time
import datetime
import os
from array import *
import re
import keyboard
import sys
def print_pressed_keys(e):
    global ex
    if e.event_type == "down" and (e.name == "right alt" or e.name == "alt gr"):
       ex = 1

keyboard.hook(print_pressed_keys)
# iter_cycle = 500  # сколько раз пройти
# sleep_step = 0.2
# iter_out = 2  # через сколько неудачных попыток на выход
# sleep_cycle = 0  # ожидание после цикла
# wait_to_brake = 20
# need_scroll = 0
def load_variables_from_file(file_path):
    variables = {
        "iter_cycle": 500,
        "sleep_step": 0.2,
        "iter_out": 2,
        "sleep_cycle": 0,
        "wait_to_brake": 20,
        "need_scroll": 0
    }

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            exec(file.read(), variables)

    return variables

# Путь к файлу
file_path = "1"

# Загрузка переменных
vars = load_variables_from_file(file_path)

# Доступ к переменным
iter_cycle = vars.get("iter_cycle")
sleep_step = vars.get("sleep_step")
iter_out = vars.get("iter_out")
sleep_cycle = vars.get("sleep_cycle")
wait_to_brake = vars.get("wait_to_brake")
need_scroll = vars.get("need_scroll")

ex = 0
#tgui временный объект поиска пнг
listfiles = []
branch = []  #  логическая ветка [номер ветки] [номер шага]
tb = 0  #
tmplist = []
path = os.getcwd()


# сбор актуальных файлов и сортировка
with os.scandir(path) as listOfEntries:
    for entry in listOfEntries:
        if entry.is_file():
            if entry.name[-3:] == "png" or entry.name[-3:] == "txt":
                listfiles.append(entry.name)
i = 0  # сортировка текстовых  listfiles.sort()
while i < len(listfiles)-1:
    if int(re.sub(r'\D*(\d+).+', r"\1", listfiles[i])) > int(re.sub(r'\D*(\d+).+', r"\1", listfiles[i+1])):
        listfiles[i], listfiles[i+1] = listfiles[i+1], listfiles[i]
        i = i - 2
    i = max(i+1, 0)
print(listfiles)

# разбивка на самостоятельные списки ветвлений
for u in range(0, 10):
    tmplist = []
    for i in listfiles:
        if len(i) > u:
            if (i[0:u] == '-' * u and u > 0 and not i[u] == "-") or (u == 0 and not i[0] == '-'):
                tmplist.append(i)
    branch.append(tmplist)

# работа
for i in range(1, iter_cycle): # сколько циклов
    for u in range(len(branch[tb])):  # номер шага
        time.sleep(sleep_step)
        if ex==1:
            sys.exit()
        if branch[tb][u][-3:] == "png":
            t1 = 0
            t = 0
            while t == 0:  # поиск фрагмента
                tgui = pyautogui.locateOnScreen(branch[tb][u])
                time.sleep(sleep_step)
                t1 = t1+1
                print(t1, tgui, branch[tb][u])
                if tgui is not None:
                    t = 1
                    if need_scroll == 1:
                        if os.path.isfile("scrol.png"):
                            if tgui.top > 800 and u == 0:  # down
                                #pyautogui.scroll(-300)
                                print("scroll+")
                                tgui1 = pyautogui.locateOnScreen("scrol.png")
                                pyautogui.moveTo(tgui1)
                                pyautogui.click()
                                time.sleep(sleep_step / 2)
                                tgui = pyautogui.locateOnScreen(branch[tb][u])
                                if tgui is None:
                                    t = 0
                if t1 > iter_out: #для смены ветки
                    t = 2
            if t == 2 and len(branch[tb+1]) > 0:
                tb = tb+1
                break
            if not re.search(r'\d+\+-\.', branch[tb][u]):  # если нет признака д+-(факт присутствия)
                if re.search(r'\d+\+\d*\.', branch[tb][u]) or re.search(r'\d+\.', branch[tb][u]) or re.search(r'\d+\+\+\.', branch[tb][u]):  # признак перемещения Д+ или Днан
                    b = re.sub(r'\D*\d+(\+(\d+))?.+', r"\2", branch[tb][u])  # снимаем с 1+2.пнг двойку
                    if len(b) > 0:
                        pyautogui.moveTo(tgui.left, tgui.top+int(b))  # если есть команда смещать
                    else:
                        pyautogui.moveTo(tgui)  # если нет
                if re.search(r'\d+\.', branch[tb][u]):  # признак клика Днан
                    pyautogui.click()
                if re.search(r'\d+\+\+\.', branch[tb][u]):  # признак клика до перемен
                    t = 0
                    while t == 0:
                        pyautogui.click()
                        t2gui = pyautogui.locateOnScreen(branch[tb][u])
                        time.sleep(sleep_step)
                        t1 = t1 + 1
                        if not tgui == t2gui:
                            t = 1
        if branch[tb][u][-3:] == "txt":
            with open(branch[tb][u], "r") as file:
                line = file.readline()
            if len(line) > 0:
                pyautogui.write(line)
            if re.search(r'\d+\+\.', branch[tb][u]):
                pyautogui.press('enter')

        print(branch[tb][u])
    print(datetime.datetime.now())
    time.sleep(sleep_cycle)
    if tb > 0 and not t == 2:
        tb=0
        #elif :
            #hh=0

print(branch[0][0], len(branch[0]))
