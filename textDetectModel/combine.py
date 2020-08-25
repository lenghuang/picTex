from objectDetection import objectDetection
from predict import textPredict
from array_to_txt import arrayToTxt

def outputText(url, local=True):
    """
        ENSURES: returns a list of rows, where it's row is a list of objs
        sorted from left to right (center x position), where each obj is a list
        of size 5
        obj = [center x, center y, width, height, char]
        the char is the name of the folder we trained it with in the google
        drive
    """
    # bounding_list is a list of
    # [0: center x,
    #  1: center y,
    #  2: top left x,
    #  3: top left y,
    #  4: width,
    #  5: height,
    #  6: width + height,
    #  7: img]
    bounding_list = objectDetection(url, debug=True)

    page = []
    for row in bounding_list:
        temp_row = []
        for obj in row:
            img = obj[7]
            character_list = textPredict(img, is_path = False)
            center_x = obj[0]
            center_y = obj[1]
            width = obj[4]
            height = obj[5]
            char = character_list
            obj_temp = [center_x, center_y, width, height, char]
            temp_row.append(obj_temp)
        page.append(temp_row)

    # If you wanted the fourth row, first obj's character
    #char = page[3][0][4]
    return arrayToTxt(page)

if __name__ == "__main__":
    #print(outputText("https://i.stack.imgur.com/VfmOK.png"))
    print(outputText("examples/IMG_5496.jpeg"))

