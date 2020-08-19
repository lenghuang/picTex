from combine import *
# Assume each line is either math or not

def arrayToTxt():
    page = outputText("examples/u.jpg")

    texFile = open("MyFile.txt", "w")

    docStart = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\begin{document}\n
"""

    texFile.write(docStart)

    commands = {'cong':'\\cong', 'iff':'\\iff', 'implies':'\\implies', 
                'geq':'\\geq', 'leq':'\\leq', 'neq':'\\neq'}
    needContext = {'(':'\\left(', ')':'\\right)'}
    for line in page:
        texLine = ""
        texLineMath = ""
        mathMode = False
        for i in range(len(line)):
            symbol = line[i][4]
            if symbol.isalpha():
                texLine += symbol
                texLineMath += symbol
            elif symbol.isnumeric():
                mathMode = True
                texLine += symbol
                texLineMath += symbol
            elif symbol == 'sum':
                mathMode = True
                texLineMath += '\\sum'
                sumUpper = line[i][1] - 0.5 * line[i][3]
                sumLower = line[i][1] + 0.5 * line[1][3]
                above = "" # text above summation symbol
                below = "" # text below summation symbol
                curr = i   # cursor variable for finding chars above+below

                # iterate through chars before + after summation to find 
                # everything above and below
                while (curr >= 0): # before
                    if line[curr][1] < sumUpper:
                        above = line[curr][4] + above
                    elif line[curr][1] > sumLower:
                        below = line[curr][4] + below
                    else: 
                        break
                    curr -= 1
                while (curr < length(line)): #after
                    if line[curr][1] < sumUpper:
                        above += line[curr][4]
                    elif line[curr][1] > sumLower:
                        below += line[curr][4]
                    else:
                        break
                    curr += 1
                
                # add above and below info to tex code
                if below != "":
                    texLineMath += '_{' + below + '}'
                if above != "":
                    texLineMath += '^{' + above + '}'
                
            elif symbol in needContext:
                texLine += symbol
                texLineMath += needContext[symbol]
            elif symbol in commands:
                mathMode = True
                texLineMath += commands[symbol]
            else: # some other ASCII-representable symbol
                texLine += symbol
        if mathMode:
            texFile.write("$" + texLineMath + "$")
        else: 
            texFile.write(texLine)
        texFile.write(" \\\\ \n")


    texFile.write("\n\\end{document}")
    texFile.close()
    return

arrayToTxt()