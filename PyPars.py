# упорядоченная файлоориентированная автоматизация ТУ-9
import pyautogui #pip install opencv-python для pyautogui.locateOnScreen('link.png', region=(x, y-30, 600, 55), confidence=0.95)"
import time
import os
from array import *
import re

sleep_step = 0.4
sleep_cycle = 1
wait_to_brake = 10
iter_cycle = 85
need_scroll = 1

#tgui временнвй объект поиска пнг
listfiles = []
branch = []#  логическая ветка [номер ветки] [номер шага]
tb = 0#
tmplist =[]
path = os.getcwd()


# сбор актуальных файлов и сортировка
with os.scandir(path) as listOfEntries:
    for entry in listOfEntries:
        if entry.is_file():
            if entry.name[-3:] == "png" or entry.name[-3:] == "txt":
                listfiles.append(entry.name)
listfiles.sort()

# разбивка на самостоятельные списки ветвлений
for u in range(0, 10):
    tmplist = []
    for i in listfiles:
        if len(i) > u:
            if (i[0:u] == '-' * u and u > 0 and not i[u] == "-") or (u == 0 and not i[0] == '-'):
                tmplist.append(i)
    branch.append(tmplist)

# работа
for i in range(iter_cycle): # сколько раз
    for u in range(len(branch[tb])):  # номер шага
        if branch[tb][u][-3:] == "png":
            t = 0
            while t == 0:  # поиск фрагмента
                tgui = pyautogui.locateOnScreen(branch[tb][u])
                time.sleep(sleep_step)
                if tgui is not None:
                    t = 1
            

            print(branch[tb][u])
        #elif :
            #hh=0

print(branch[0][0], len(branch[0]))
