from os import listdir
import os
import csv
import shutil

os.chdir("C:\\Users\\zacan\\Downloads\\161627_369455_bundle_archive")
print(len(listdir(os.getcwd() + "\\hasy-data")))

commands = {
    ',':'comma',
    '.':'full_stop',
    '>':'greater',
    '<':'lesser',
    '\\mathbb{N}':'Naturals',
    '\\mathbb{R}':'Reals',
    '+': '+',
    '-': '-',
    '*' : 'ast',
    '|' : 'long_bar',
    '\\|' : 'long_bar'
}

with open('hasy-data-labels.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    i = 0
    for row in reader:
        if 0 < i:
            symbol = row[2]
            if symbol in commands:
                symbol = commands[symbol]

            if not os.path.exists('data\\'+symbol):
                os.makedirs('data\\'+symbol)

            src = os.getcwd() + "\\hasy-data\\" + row[0][10:]
            destination = os.getcwd() + "\\data\\" + symbol +"\\" + row[0][10:]
            shutil.copyfile(src, destination)
        else:
            i += 1