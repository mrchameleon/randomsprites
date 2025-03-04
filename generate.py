from datetime import datetime, timezone
import PIL, random, sys
from PIL import Image, ImageDraw

origDimension = 1500

r = lambda: random.randint(50,255)
rc = lambda: ('#%02X%02X%02X' % (r(),r(),r()))
listSym = []

def create_square(border, draw, randColor, element, size):
    if (element == int(size/2)):
        draw.rectangle(border, randColor)
    elif (len(listSym) == element+1):
        draw.rectangle(border,listSym.pop())
    else:
        listSym.append(randColor)
        draw.rectangle(border, randColor)

def create_invader(border, draw, size):
    x0, y0, x1, y1 = border
    squareSize = (x1-x0)/size
    randColors = [rc(), rc(), rc(), (0,0,0), (0,0,0), (0,0,0)]
    incrementer = 1
    element = 0

    for y in range(0, size):
        incrementer *= -1
        element = 0
        for x in range(0, size):
            topLeftX = x*squareSize + x0
            topLeftY = y*squareSize + y0
            botRightX = topLeftX + squareSize
            botRightY = topLeftY + squareSize


            create_square((topLeftX, topLeftY, botRightX, botRightY), draw, random.choice(randColors), element, size)
            if (element == int(size/2) or element == 0):
                incrementer *= -1;
            element += incrementer


def main(size, invaders, imgSize):
    origDimension = imgSize
    origImage = Image.new('RGB', (origDimension, origDimension))
    draw = ImageDraw.Draw(origImage)

    invaderSize = origDimension/invaders
    print(invaderSize)
    padding = invaderSize/size
    print(padding)
    # Will eventually create many
    finalBotRightX = 0
    finalBotRightY = 0
    for x in range(0, invaders):
        for y in range(0, invaders):
            topLeftX = x*invaderSize + padding
            topLeftY = y*invaderSize + padding
            botRightX = topLeftX + invaderSize - padding*2
            botRightY = topLeftY + invaderSize - padding*2
            
            finalBotRightX = botRightX
            finalBotRightY = botRightY
            create_invader((topLeftX, topLeftY, botRightX, botRightY), draw, size)

    utc_dt = datetime.now(timezone.utc)
    iso_date = utc_dt.strftime('%Y%m%dT%H%M%S')
    origImage.save(f"export/{iso_date}_invader-"+str(size)+"x"+str(size)+"-"+str(invaders)+"-"+str(imgSize)+".jpg")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
