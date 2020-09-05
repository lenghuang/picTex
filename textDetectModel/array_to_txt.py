# Assume each line is either math or not

def arrayToTxt(page):

    #texFile = open("MyFile.txt", "w")

    docStart = """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\begin{document}\n"""

    #texFile.write(docStart)

    commands = {
                'cong': '\\cong',
                'iff': '\\iff',
                'implies': '\\implies',
                'comma': ',',
                'full_stop': '.',
                'greater': '>',
                'lesser': '<',
                'Naturals': '\\mathbb{N}',
                'Reals': '\\mathbb{R}',
                '+': '+',
                '-': '-',
                'ast': '*'
               }

    needContext = {'(':'\\left(', ')':'\\right)'}
    for j, line in enumerate(page):
        texLine = ""
        texLineMath = ""
        mathMode = False
        for i in range(len(line)):
            symbol = line[i][4]
            if symbol.isalpha() and len(symbol) == 1:
                if not mathMode:
                    texLine += " " + symbol
                    texLineMath += " " + symbol
                else:
                    if symbol == 'o' and "9" in texLineMath and "0" not in texLineMath:
                        symbol = "0"
                        texLine += " " + symbol
                        texLineMath += " " + symbol
                    elif symbol == "n":
                        symbol = "n"
                        texLine += " " + symbol
                        texLineMath += " " + symbol
                    elif symbol == 'o' and "n" in texLineMath:
                        symbol = "1)"
                        texLine += " " + symbol
                        texLineMath += " " + symbol
            elif symbol.isnumeric():
                mathMode = True
                texLine += " " + symbol
                texLineMath += " " + symbol
            elif symbol == 'sum':
                mathMode = True
                texLineMath += '\\sum'
                sumUpper = line[i][1] - 0.5 * line[i][3]
                sumLower = line[i][1] + 0.5 * line[i][3]
                widthLower = line[i][0] - 0.5 * line[i][2]
                widthUpper = line[i][0] + 0.5 * line[i][2]

                above = "" # text above summation symbol
                below = "" # text below summation symbol
                curr = i   # cursor variable for finding chars above+below

                # iterate through chars before + after summation to find 
                # everything above and below

                possible_chars = line
                if j > 0: possible_chars += page[j-1]
                if j < len(page)-1 : possible_chars += page[j+1]

                p_upper = list(filter(lambda x: x[1] < (sumUpper - x[3]/2) and
                                          widthLower < x[0] < widthUpper,
                                          possible_chars))
                p_lower = list(filter(lambda x: x[1] > sumLower - x[3] / 2 and
                                           widthLower < x[0] < widthUpper,
                                 possible_chars))
                (p_lower) = list(map(lambda x: x[4], p_lower))
                p_upper = list(map(lambda x: x[4], p_upper))
                above = "".join(p_upper)
                below = "".join(p_lower)

                '''
                while (curr >= 0): # before
                    if line[curr][1] < sumUpper: # if above sum symbol
                        above = line[curr][4] + above
                    elif line[curr][1] > sumLower: # below sum symbol
                        below = line[curr][4] + below
                    else: # normal character
                        break
                    curr -= 1
                while (curr < len(line)): # after
                    if line[curr][1] < sumUpper:
                        above += line[curr][4]
                    elif line[curr][1] > sumLower:
                        below += line[curr][4]
                    else:
                        break
                    curr += 1
                '''
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
                texLine += "\\"+symbol + " "
        if mathMode:
            #texFile.write("$" + texLineMath + "$")
            docStart += "\t $" + texLineMath + "$"
        else:
            #texFile.write(texLine)
            docStart += "\t" + texLine
        #texFile.write(" \\\\ \n")
        docStart += " \\\\ \n"

    #texFile.write("\n\\end{document}")
    #texFile.close()
    docStart += "\n\\end{document}"
    return docStart
