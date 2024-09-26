import copy
class Board:
    def __init__(self,Board):
        self.Board=Board
    @staticmethod
    def CreateBlank(Width,Height):
        return Board([[" " for X in range(Height)] for Y in range(Width)])
    def CreateCopy(self):
        return copy.deepcopy(self)
class ConnectFour:

    def DropPiece(self,Column:int,Piece:str):
        for Y in range(self.Height - 1,-1,-1):
            if self.Board[Y] == " ":
                self.Board[Y]=Piece
                break
    
    def CheckWin(self):
        pass
print("Few")