import sys, os
import datetime

# assumes python 3 (else import urllib2)
import urllib.request
import bs4
import re

import subprocess

goals = []
url2 = 'file://' + os.getcwd() + '/index.html'
htmlf = urllib.request.urlopen(url2)
soup = bs4.BeautifulSoup(htmlf, "lxml")
for res in soup.findAll('h1'):
    goals.append(res.get_text().strip())

goals = goals[1:] # nix 2018
# print("all goals: {0}".format(goals))
progress = dict.fromkeys(goals)

for goal, work_done in progress.items():
    has_worked = input("Have you worked on {0} today? (y/n) ".format(goal))
    if has_worked == "y":
        progress[goal] = input("What did you do? ").split(", ") # assume comma separation
    else:
        progress[goal] = "no work"

print("progress: {0}".format(progress))
now = datetime.datetime.now()
date = now.strftime("%b") + " " + str(now.day)

file = open("index.html", "r")
whole = file.read()
file.close()

# where all goal progress lists end
list_ends = [m.start() for m in re.finditer("</dl>", whole)]
offset = 0
for list_end, goal in zip(list_ends, goals):

    data = "\n<dt>{0}</dt>\n".format(date)
    if progress[goal] == "no work":
        color = "\"bg-danger\""
        data += "<dd>\n<p class={0}>\nno work\n</p>\n</dd>\n".format(color)
    else:
        color = "\"bg-success\""
        for deed in progress[goal]:
            data += "<dd>\n<p class={0}>\n{1}\n</p>\n</dd>\n".format(color, deed)

    print("data: {0}".format(data))
    whole = whole[:list_end - len("<\dl>") + offset] + data + whole[list_end - len("<\dl>") + offset:]
    offset += len(data)

file = open("index.html", "w")
file.write(whole)
file.close()

# assumes execution from repo
subprocess.call(['./day.sh', sys.argv[1], sys.argv[2]])
