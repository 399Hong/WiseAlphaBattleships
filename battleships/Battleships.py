from random import randint
from enum import Enum
from colorama import Back,Fore
from os import system, name


class CellType(Enum):

    HIDDEN = 1
    COLD = 2
    WARM  = 3
    HOT = 4
    ENEMY = 5
    

class Battleships:
    def __init__(self, size: int = 8, maxAttempts : int  = 20, enemyNum:int = 2 ):
        self.__size = size # size of the board
        self.__maxAttempts = maxAttempts # maximum number of plays
        self.__boardStyle = "*" # board look and feel
    
        self.__enemyCoordinate = dict() # enemy coordinate, info format {id:(x,y)}
        # id is assigned based on the order of spawning
   
        
        self.__generateEnemies(enemyNum = enemyNum)
        self.__playBoard = [ [1] * size for i in range(size) ]
        #board for game play info
        

       
    def run(self, cheat:bool = True):
        for i in range(self.__maxAttempts):
            # clear terminal 
            if name == 'nt':
                system('cls')
            else:
                system('clear')

            print(f"You have {self.__maxAttempts - i } round(s) of ammo left ")
            if cheat:
                print(f"Cheat Mode Enabled! Enemy coordinates: {self.__enemyCoordinate}")
            
            self.__drawBoard()
            self.__instruction()

            x,y = self.__getTarget()
            outcome,toDelete = self.__calculateDistanceEnemyTarget(x,y)
            for id in toDelete:
                self.__removeEnemy(id)

            # evaluate the outcome, the highest(max) number will be the cellType show on the board
            self.__updatePlayBoard(x,y, max(outcome))

            if len(self.__enemyCoordinate) == 0:
                print(Fore.GREEN+"Congrats, You WON!")
                self.__drawBoard()
                return 
        print(Fore.RED+"You LOST")
        return
            
            


    def __calculateDistanceEnemyTarget(self, targetX:int, targetY:int) -> tuple:
        outcome = []
        toDelete = []
        for k,(x,y) in self.__enemyCoordinate.items():
            dist = abs(targetX - x) + abs(targetY - y)
            if dist == 0:
                outcome.append(CellType.ENEMY.value)
                toDelete.append(k)
            # 1-2 cells away hot
            elif dist == 1 or dist == 2:
                outcome.append(CellType.HOT.value)
            # 3-4 cells away warm
            elif dist == 3 or dist == 4:
                outcome.append(CellType.WARM.value)
            else:
                outcome.append(CellType.COLD.value)
       
        return (outcome,toDelete)
                
    def __removeEnemy(self, id:int):
        del self.__enemyCoordinate[id]

    def __generateEnemies(self, size: int = 8, enemyNum:int = 2):
        for i in range(enemyNum):
            x = randint(0, size - 1)
            y = randint(0, size - 1)
            # assume the ememies is stupid and may send all ships in the same cell
            self.__enemyCoordinate[i] = (x,y)
    
    def __getTarget(self) -> tuple:
        while True:
            try:
                x = int(input("Please enter the x-coordinate: "))
                y = int(input("Please enter the y-coordinate: "))
                # check for valid x y value
                if (x >= 0 and x < self.__size and y >= 0 and y <self.__size) :
                    return (x,y)
                print(f"Please enter the x and the y coordinate between 0 and {self.__size-1}")

            except:
                print(f"Please enter the x and the y coordinate as a number between 0 and {self.__size-1}")

    def __updatePlayBoard(self, x:int, y:int, info:int):
        self.__playBoard[x][y] = info

    # view
    def __fillCellColor(self, info:int) -> str:
        if  CellType(info) == CellType.HIDDEN:
            return "  "
        elif CellType(info) == CellType.COLD:
            return Back.WHITE+ "  " +Back.BLACK
        elif CellType(info) == CellType.WARM:
            return Back.MAGENTA + "  " +Back.BLACK
        elif CellType(info) == CellType.HOT:
            return Back.RED + "  " +Back.BLACK
        elif CellType(info) == CellType.ENEMY:
            return "XX"
    
    def __instruction(self):
        print(f"{self.__fillCellColor(CellType.COLD.value)} -> enemies are not detected nearby")
        print(f"{self.__fillCellColor(CellType.WARM.value)} -> enemies are 2 to 4 cells away")
        print(f"{self.__fillCellColor(CellType.HOT.value)} -> enemies are 2 to 4 cells away")
        print(f"{self.__fillCellColor(CellType.ENEMY.value)} -> You have hit the enemy")
        print()

    def __drawBoard(self):
        # print board labels to help user find a cell coordinate
        print(" "*5,end="")
        for i in range (self.__size):
            # align number labels
            print(str(i).ljust(3), end ="")
        print()


        boardBoundary = " "*3+"+—-"* self.__size +"+"
        # boundary format -> +—-+—-+—-+—-+—-+—-+—-+—-+

        # print upper bounday of the bord
        print(boardBoundary)

        # print the board
        for i in range (self.__size):
            #align num labels and the board
            print(str(i).ljust(3),end = "")
            for j in range (self.__size):
                info  = self.__playBoard[i][j]
                print(f"|{self.__fillCellColor(info)}", end = "")
            print("|")
            print(boardBoundary)
   

    


