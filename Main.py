class ConnectFour:
    def __init__(self,Width:int,Height:int):
        self.Width=Width
        self.Height=Height
        self.Board=[[" " for X in range(Height)] for Y in range(Width)]

    def DropPiece(self,Column:int,Piece:str):
        for Y in range(self.Height - 1,-1,-1):
            if self.Board[Y] == " ":
                self.Board[Y]=Piece
                break
    
    def CheckWin(self,)