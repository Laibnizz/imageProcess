from image import *
import math
import numpy as np
import matplotlib.image as mping
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib as cm

def drawImage(anImage, width, height, processType):
    myWin = ImageWin(width, height, processType)
    anImage.draw(myWin)
    myWin.exitOnClick()

    return

def convolve(anImage, r, c, mask):
    sumRed = 0
    sumGreen = 0
    sumBlue = 0

    sumKernel = 0
    for row in range(3):
        for col in range(3):
            sumKernel += mask[row][col]
    
    for row in range(r - 1, r + 2):
        for col in range(c - 1, c + 2):
            aPixel = anImage.getPixel(col, row)
            
            sumRed += aPixel.getRed() * mask[row - (r - 1)][col - (c - 1)]
            sumGreen += aPixel.getGreen() * mask[row - (r - 1)][col - (c - 1)]
            sumBlue += aPixel.getBlue() * mask[row - (r - 1)][col - (c - 1)]

            Red = sumRed // sumKernel
            Green = sumGreen // sumKernel
            Blue = sumBlue // sumKernel

            if Red > 255:
                Red = 255
            elif Red < 0:
                Red = 0

            if Green > 255:
                Green = 255
            elif Green < 0:
                Green = 0

            if Blue > 255:
                Blue = 255
            elif Blue < 0:
                Blue = 0

    newPixel = Pixel(Red, Green, Blue)
            
    return newPixel

def mirrorVertical(oldImage):
    width = oldImage.getWidth()
    height = oldImage.getHeight()
    center = width // 2 #Number from zero

    newImage = EmptyImage(width, height)
    
    #Mirror
    for row in range(height):
        for col in range(center + 1):
            oldPixel = oldImage.getPixel(col, row)
            newImage.setPixel(col, row, oldPixel)
            newImage.setPixel(width - 1 -col, row, oldPixel)

    drawImage(newImage, width, height, 'Mirroring on the vertical axis')
    
    return

def mirrorHorizontal(oldImage):
    width = oldImage.getWidth()
    height = oldImage.getHeight()
    center = height // 2 #Number from zero
    newImage = EmptyImage(width, height)
    
    #Mirror
    for row in range(center + 1):
        for col in range(width):
            oldPixel = oldImage.getPixel(col, row)
            newImage.setPixel(col, row, oldPixel)
            newImage.setPixel(col, height - 1 - row, oldPixel)

    drawImage(newImage, width, height, 'Mirroring on the horizontal axis')
    
    return

def blurring(oldImage):
    width = oldImage.getWidth()
    height = oldImage.getHeight()
    newImage = EmptyImage(width, height)

    mask = [[1, 2, 1], [2, 1, 2], [1, 2, 1]]

    for row in range(1, height - 1):
        for col in range(1, width - 1):
            convolutionPixel = convolve(oldImage, row, col, mask)
            newImage.setPixel(col, row, convolutionPixel)

    drawImage(newImage, width, height, 'Blurring')
    
    return

def sharpening(oldImage):
    width = oldImage.getWidth()
    height = oldImage.getHeight()
    newImage = EmptyImage(width, height)

    mask = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]

    for row in range(1, height - 1):
        for col in range(1, width - 1):
            convolutionPixel = convolve(oldImage, row, col, mask)
            newImage.setPixel(col, row, convolutionPixel)

    drawImage(newImage, width, height, 'Sharpening')

    return

def SVDImage(n, oldImage):
    U, S, VT = np.linalg.svd(oldImage)
    SVD = np.zeros((U.shape[0], VT.shape[1]))
    for i in range(0, n):
        SVD[i, i] = S[i]

    newImage = np.matmul(U, SVD)
    newImage = np.matmul(newImage, VT)
    newImage[newImage > 255] = 255
    newImage[newImage < 0] = 0
    newImage = newImage.astype('uint8')
    
    return newImage

print("The purpose of this program is to process image.")

fileName = 'test.gif'
print('h means mirroring on the horizontal axis')
print('v means mirroring on the vertical axis')
print('b means blurring by using blurK')
print('s means sharpening by using sharpenK')

hvbsString = input("Enter h, v, b, s:")

anImage = FileImage(fileName)

for ch in hvbsString:
    if ch == 'h':
        mirrorHorizontal(anImage)
    elif ch == 'v':
        mirrorVertical(anImage)
    elif ch == 'b':
        blurring(anImage)
    elif ch == 's':
        sharpening(anImage)

imageForSVD = mping.imread(fileName)

R = imageForSVD[:, :, 0]
G = imageForSVD[:, :, 1]
B = imageForSVD[:, :, 2]

n = int(input('Enter the number of the sigma you want for SVD:'))
    
RedImg = SVDImage(n, R)
GreenImg = SVDImage(n, G)
BlueImg = SVDImage(n, B)

newImage = np.stack([RedImg, GreenImg, BlueImg], axis = 2)
plt.imshow(newImage)
plt.show()
