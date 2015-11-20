# -*- coding:utf-8 -*-
import re
import csv


def find_flag(lines, flag):
    return [l for l in lines if l.find(flag) > -1]


f = open('123.txt', 'r')
log = f.readlines()
f.close()
flags = ['p2pguard', 'p2pclient', 'p2pdownload']
for i in flags:
    f = open(i+'.txt', 'w')
    for k in find_flag(log, i):
        k = k.strip()
        f.write(re.sub('\s+', '\t', k)+'\n')
    f.close()


'''
def get_part(file, mark):
    s = None
    f = 0
    part = []
    line = file.readline()
    while line:
        if -1 < line.find(mark):
            if f == 0:
                s = line
                f += 1
            else:
                part.append(s)
                s = line
        else:
            s = "{0}{1}".format(s, line)
        line = file.readline()
    part.append(s)
    return part


def get_first_rex(string,  regex):
    r = re.compile(regex)
    return r.findall(string)[0]

if __name__ == '__main__':
    logfile = open('123.txt', 'r')
    first = "Mem"
    log = get_part(logfile, first)
    logfile.close()
    # print(log[1])
    cpuREX = r"CPU:([0-9]+)%"
    memREX = r"Mem:([0-9]+)K"
    excl = open("321.csv", 'w', newline='')
    firstline = ['log', 'cpu', 'Mem']
    csvwriter = csv.writer(excl, dialect='excel')
    csvwriter.writerow(firstline)
    for o in log:
        row = []
        x = o.replace(" ", "")
        cpu = get_first_rex(x, cpuREX)
        mem = get_first_rex(x, memREX)
        #row.append(o)
        row.append(" ")
        row.append(cpu)
        row.append(mem)
        csvwriter.writerow(row)
    excl.close()
'''
