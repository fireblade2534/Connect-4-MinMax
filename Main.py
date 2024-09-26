import copy
class Board:
    def __init__(self,Board):
        self.Board=Board
    @staticmethod
    def CreateBlank(Width,Height):
        return Board([[" " for X in range(Width)] for Y in range(Height)])
    def CreateCopy(self):
        return copy.deepcopy(self)
class ConnectFour:
    @staticmethod
    def DropPiece(Board,Column:int,Piece:str):
        for Y in range(len(Board.Board) - 1,-1,-1):
            if Board.Board[Y][Column] == " ":
                Board.Board[Y][Column]=Piece
                break
        return Board
    
    @staticmethod
    def CheckWin(Board):
        for Y in range(0,len(Board.Board)-4):

    @staticmethod
    def _FormatPiece(Piece):
        if Piece == "R":
            return "🔴"
        if Piece == "Y":
            return "🟡"
        if Piece == " ":
            return "  "

    @staticmethod
    def Render(Board):
        Width=len(Board.Board[0])
        Height=len(Board.Board)
        Output=[]
        for Y in range(Height):
            Output.append("|".join([ConnectFour._FormatPiece(Board.Board[Y][X]) for X in range(Width)]))
        print(f"\n{('--+'*Width)[:-1]}\n".join(Output))



B=Board.CreateBlank(7,6)
ConnectFour.DropPiece(B,4,"R")
ConnectFour.DropPiece(B,3,"Y")
ConnectFour.DropPiece(B,3,"R")
ConnectFour.Render(B)
