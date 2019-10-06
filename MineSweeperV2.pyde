import random
import time

CELLSX = 30
CELLSY = CELLSX/2
SIZEW = CELLSX * 28
SIZEH = CELLSY * 28
RAD = 15
BOMBS = 100
RUNNING = True


hexcountx = (SIZEW/(RAD))
hexcounty = (SIZEH/(RAD))


class Cell:
    def __init__(self, bomb = False, vis = False, flagged = False, hood = 0):
        self.bomb = bomb
        self.visible = vis
        self.flagged = flagged
        self.hood = hood
    
    
class Hexagon(Cell):
    hexa = []
    def __init__(self, cx, cy, r, i, j):
        Cell.__init__(self)
        self.x = cx
        self.y = cy
        self.radi = r
        self.icount = i
        self.jcount = j
    
    
    def getShape(self):
        return self.hexa

    
    def changeValues(self, cx, cy, r, i, j):
        self.x=cx
        self.y=cy
        self.radi=r
        self.icount = i
        self.jcount = j
        
        vertx = [] 
        verty = [] 
        
        for k in range(6):
            vertx.append(self.x + self.radi * cos(radians(360.0 / 6 * k)))
            verty.append(self.y + self.radi * sin(radians(360.0 / 6 * k)))
        self.hexa = [(vertx[0], verty[0]), (vertx[1], verty[1]),(vertx[2], verty[2]),(vertx[3], verty[3]),(vertx[4], verty[4]),(vertx[5], verty[5])]


    def display(self):
        if self.visible and self.flagged == False:
            fill(125, 85,0)
        elif self.visible == False and self.flagged:
            fill(125, 0, 0)
        else:
            fill(220, 150, 0)
        beginShape()
        for i in range(6):
            vertex(self.x + self.radi * cos(radians(360.0 / 6 * i)), self.y + self.radi * sin(radians(360.0 / 6 * i)))
        endShape(CLOSE)
    
        if self.visible and self.flagged == False and self.bomb == False and self.hood > 0:
            fill(0)
            textAlign(CENTER)
            textSize(15)
            text(self.hood, self.x, self.y)
            
        if self.bomb and self.visible:
            fill(0)
            ellipse(self.x, self.y , 10, 10)
            fill(255,255,255)
            ellipse(self.x, self.y - 2, 3, 3)

      
    def getHood(self):
        if self.jcount % 2 == 0:
            return  [(0, 1), (0, 2), (0, -1), (-1, -1), (0, -2), (-1, 1)]
        else:
            return [(0, 1), (0, 2), (0, -1), (1, -1), (0, -2), (1, 1)]
    
    
    def revealHood(self):
        hood = self.getHood()
        for (i,j) in hood:
            if  0 <= self.icount + i < CELLSY and 0 <= self.jcount + j < CELLSX:
                print(self.icount +i, self.jcount + j)
                if hexagon[self.icount+i][self.jcount+j].bomb != True and hexagon[self.icount+i][self.jcount+j].visible != True and self.bomb != True:
                    hexagon[self.icount+i][self.jcount+j].getVision()
    
    
    def getVision(self):
        self.visible = True
        if self.bomb == True:
            endGame()
        if self.hood == 0:
            self.revealHood()
    
class Button:
    def __init__(self, type):
        self.type = type        
        
    def display(self):
        if self.type == "reset":
            fill(190,190,190)
            rect(SIZEW /2 - CELLSX, 10, 30, 30)

class Timer:
    def __init__(self):
        self.startTime = time.time()
    
    def restart(self):
        self.startTime = time.time()
    
    def display(self):
        fill(0)
        textSize(25)
        text(int(time.time() - self.startTime), SIZEW - CELLSX * 1.2 , CELLSY * 2.5)
    
                                
class Menu:
    def display(self):
        rect(0, 0, SIZEW - 1, CELLSX * 2)


#initing a 2d array of Hex objects.
hexagon = [[Hexagon(0, 0, 0, 0, 0) for i in range(CELLSX)] for j in range(CELLSY)]  
menu = Menu()
reset = Button("reset")
gameTimer = Timer()


def setup():
    size(SIZEW, SIZEH + 80)
    background(100,100,100)
    smooth(2)
    
def main():
    icount = 2 #hex grid x starting point.
    for i in hexagon:
        jcount = 2 #hex grid y starting point
        for j in i:
            if ((jcount % 2) == 0):
                #putting actualy values into the 2d of hex
                j.changeValues((3 * RAD * icount), (.866 * RAD * (jcount + 4)), RAD, icount -2, jcount -2)
            else:
                j.changeValues(3 * RAD * (icount + .5), .866 * RAD * (jcount + 4), RAD, icount -2, jcount -2)
            #making sure nothing from the last game comes through
            j.visible = False
            j.flagged = False
            j.bomb = False
            gameTimer.restart()
            jcount += 1
        icount += 1
    
    for i in range(BOMBS):
        randx = random.randint(0, CELLSX - 1)
        randy = random.randint(0, CELLSY - 1)
        if hexagon[randy][randx].bomb == False:
            hexagon[randy][randx].bomb = True
        else:
            i -= 1
         
    for i in hexagon:
        for j in i:
            neighbourhoodBombs = 0
            hood = j.getHood()
            for (x,y) in hood:
                if 0 <= x + j.icount < CELLSY and 0 <= y + j.jcount < CELLSX:
                    if hexagon[x+j.icount][y+j.jcount].bomb == True:
                        neighbourhoodBombs += 1 
            j.hood = neighbourhoodBombs


def draw():
    menu.display()
    reset.display()
    gameTimer.display()
    for i in hexagon:  
        for j in i:
            j.display()
    if RUNNING == False:
        noLoop()
    
    
def checkInside(x, y, hex):
    length = len(hex)
    inside = False

    x1,y1 = hex[0]
    for i in range(length+1):
        x2,y2 = hex[i % length]
        if y > min(y1,y2):
            if y <= max(y1,y2):
                if x <= max(x1,x2):
                    if y1 != y2:
                        xs = (y-y1)*(x2-x1)/(y2-y1)+x1
                    if x1 == x2 or x <= xs:
                        inside = not inside
        x1,y1 = x2,y2

    return inside


def endGame():
    global RUNNING
    for i in hexagon:
        for j in i:
            if j.bomb:
                j.flagged = False
                j.visible = True
    RUNNING = False


def menuClick(x, y):
    if 390 <= x <= 420 and 12 <= y <= 42:
        global RUNNING 
        RUNNING = True
        loop()
        main()

                    
    
def mousePressed():
    if mouseY <= 60:
        menuClick(mouseX, mouseY)
    elif mouseButton == LEFT:
        for i in hexagon:
            for j in i:
                if checkInside(mouseX, mouseY, j.getShape()) and j.flagged == False:
                    j.getVision()

    else:
      for i in hexagon:
            for j in i:
                if point_inside_polygon(mouseX, mouseY, j.getShape()) and j.visible == False:
                    if j.flagged == True:
                        j.flagged = False
                    else:
                        j.flagged = True

if __name__ == '__main__':
    main()
    
