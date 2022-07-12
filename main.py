import re
from turtle import width
import pygame
import random
import math

pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.minVal = min(lst)
        self.maxVal = max(lst)

        self.blockWidth = round((self.width - self.SIDE_PAD) / len(lst))
        self.blockHeight = math.floor((self.height - self.TOP_PAD) / (self.maxVal - self.minVal))
        self.start_x = self.SIDE_PAD // 2

def draw(drawInfo, algoName, ascending):
    drawInfo.window.fill(drawInfo.BACKGROUND_COLOR)

    title = drawInfo.LARGE_FONT.render(f"{algoName} - {'Ascending' if ascending else 'Descending'}", 1, drawInfo.GREEN)
    drawInfo.window.blit(title, (drawInfo.width/2 - title.get_width()/2 , 5))

    controls = drawInfo.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, drawInfo.BLACK)
    drawInfo.window.blit(controls, (drawInfo.width/2 - controls.get_width()/2 , 45))

    controls = drawInfo.FONT.render("I - Insertion Sort || B - Bubble Sort", 1, drawInfo.BLACK)
    drawInfo.window.blit(controls, (drawInfo.width/2 - controls.get_width()/2 , 75))

    drawList(drawInfo)
    pygame.display.update()

def drawList(drawInfo, colourPositions={}, clear_bg=False):
    lst = drawInfo.lst

    if clear_bg:
        clear_rect = (drawInfo.SIDE_PAD//2, drawInfo.TOP_PAD,
                        drawInfo.width - drawInfo.SIDE_PAD,
                        drawInfo.height - drawInfo.TOP_PAD)
        pygame.draw.rect(drawInfo.window, drawInfo.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = drawInfo.start_x + i * drawInfo.blockWidth
        y = drawInfo.height - (val - drawInfo.minVal) * drawInfo.blockHeight

        color = drawInfo.GRADIENTS[i % 3] 

        if i in colourPositions:
            color = colourPositions[i]

        pygame.draw.rect(drawInfo.window, color, (x, y, drawInfo.blockWidth, drawInfo.height))

    if clear_bg:
        pygame.display.update()

def generateStartingList(n, minVal, maxVal):
    lst = []

    for _ in range(n):
        val = random.randint(minVal, maxVal)
        lst.append(val)

    return lst

def bubbleSort(drawInfo, ascending=True):

    lst = drawInfo.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                drawList(drawInfo, {j: drawInfo.GREEN, j + 1: drawInfo.RED}, True)
                yield True
    
    return lst

def insertion_sort(drawInfo, ascending=True):
	lst = drawInfo.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			drawList(drawInfo, {i - 1: drawInfo.GREEN, i: drawInfo.RED}, True)
			yield True

	return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    minVal = 5
    maxVal = 100

    lst = generateStartingList(n, minVal, maxVal)
    drawInfo = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sortingAlgo = bubbleSort
    sortingAlgoName = "Bubble Sort"
    sortingAlgoGenerator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sortingAlgoGenerator)
            except StopIteration:
                sorting = False
        else:
            draw(drawInfo, sortingAlgoName, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generateStartingList(n, minVal, maxVal)
                drawInfo.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sortingAlgoGenerator = sortingAlgo(drawInfo, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sortingAlgo = insertion_sort
                sortingAlgoName = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sortingAlgo = bubbleSort
                sortingAlgoName = "Bubble Sort"

    pygame.quit()

if __name__ == "__main__":
    main()