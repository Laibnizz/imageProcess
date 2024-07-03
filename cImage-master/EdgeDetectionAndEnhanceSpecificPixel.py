from image import *
import math

def convolve(anImage, r, c, mask):
    sum = 0
    for row in range(r - 1, r + 2):
        for col in range(c - 1, c + 2):
            aPixel = anImage.getPixel(col, row)
            intensity = aPixel.getRed()
            sum = sum + intensity * mask[row - (r - 1)][col - (c - 1)]
    return sum

def blueYellowEdgeDetect(anImage):
    width = anImage.getWidth()
    height = anImage.getHeight()
    newImage = EmptyImage(width, height)

    blue = Pixel(0, 0, 255)
    yellow = Pixel(255, 255, 0)
    XMask = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    YMask = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    for r in range(1, height - 1):
        for c in range(1, width - 1):
            gX = convolve(anImage, r, c, XMask)
            gY = convolve(anImage, r, c, YMask)
            g = math.sqrt(gX ** 2 + gY ** 2)
            if g > 175:
                newImage.setPixel(c, r, blue)
            else:
                newImage.setPixel(c, r, yellow)

    return newImage

def redCyanEdgeDetect(anImage):
    width = anImage.getWidth()
    height = anImage.getHeight()
    newImage = EmptyImage(width, height)

    red = Pixel(255, 0, 0)
    cyan = Pixel(0, 255, 255)
    XMask = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    YMask = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    for r in range(1, height - 1):
        for c in range(1, width - 1):
            gX = convolve(anImage, r, c, XMask)
            gY = convolve(anImage, r, c, YMask)
            g = math.sqrt(gX ** 2 + gY ** 2)
            if g > 175:
                newImage.setPixel(c, r, red)
            else:
                newImage.setPixel(c, r, cyan)

    return newImage



def enhanceGreen1(anImage):
    width = anImage.getWidth()
    height = anImage.getHeight()
    newImage = EmptyImage(width, height)
    cnt = 0
    for r in range(height):
        for c in range(width):
            p = anImage.getPixel(c, r)
            newB = p.getBlue()
            newR = p.getRed()
            if p.getGreen() > p.getRed() and p.getGreen() > p.getBlue():
                cnt += 1
                if p.getGreen() * 2 > 255:
                    newG = p.getGreen()
                    np = Pixel(newR, newG, newB)
                    newImage.setPixel(c, r, np)
                else:
                    newG = p.getGreen() * 2
                    np = Pixel(newR, newG, newB)
                    newImage.setPixel(c, r, np)
                    
            else:
                newImage.setPixel(c, r, p)
            
    return newImage, cnt


def enhanceGreen2(anImage):
    width = anImage.getWidth()
    height = anImage.getHeight()
    newImage = EmptyImage(width, height)
    cnt = 0
    for r in range(height):
        for c in range(width):
            p = anImage.getPixel(c, r)
            newB = p.getBlue()
            newR = p.getRed()
            if p.getGreen() > p.getRed()*1.2 and p.getGreen() > p.getBlue()*1.2:
                cnt += 1
                if p.getGreen() * 2 > 255:
                    newG = p.getGreen()
                    np = Pixel(newR, newG, newB)
                    newImage.setPixel(c, r, np)
                    
                else:
                    newG = p.getGreen() * 2
                    np = Pixel(newR, newG, newB)
                    newImage.setPixel(c, r, np)
                    
            else:
                newImage.setPixel(c, r, p)
            
    return newImage, cnt

                    
def drawTheResult(oldImage, image1, image2, image3, image4, cnt1, cnt2):
    width = oldImage.getWidth()
    height = oldImage.getHeight()
    myWin = ImageWin(width * 2, height * 3, "Edge Detection")
    print('For the 1st enhance green: width =', width, ' height =', height, 'enhenced =', cnt1)
    print('For the 2nd enhance green: width =', width, ' height =', height, 'enhenced =', cnt2)
    oldImage.draw(myWin)
    image1.setPosition(0, height)
    image1.draw(myWin)
    image2.setPosition(width, height)
    image2.draw(myWin)
    image3.setPosition(0, height * 2)
    image3.draw(myWin)
    image4.setPosition(width, height * 2)
    image4.draw(myWin)
    myWin.exitOnClick()

oldImage = FileImage('lcastle.gif')
image1 = blueYellowEdgeDetect(oldImage)
image2 = redCyanEdgeDetect(oldImage)
image3, cnt1 = enhanceGreen1(oldImage)
image4, cnt2 = enhanceGreen2(oldImage)
drawTheResult(oldImage, image1, image2, image3, image4, cnt1, cnt2)
