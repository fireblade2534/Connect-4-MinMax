import copy
class Board:
    def __init__(self,Board):
        self.Board=Board
    @staticmethod
    def CreateBlank(Width,Height):
        return Board([[" " for X in range(Width)] for Y in range(Height)])
    def CreateCopy(self):
        return copy.deepcopy(self)
    
def _AllSame(List):
    return len(set(List)) == 1
class ConnectFour:
    WinNumber=4
    @staticmethod
    def DropPiece(Board,Column:int,Piece:str):
        for Y in range(len(Board.Board) - 1,-1,-1):
            if Board.Board[Y][Column] == " ":
                Board.Board[Y][Column]=Piece
                break
        return Board
    
    
    @staticmethod
    def _CheckDiagonals(Board):
        Width=len(Board.Board[0])
        Height=len(Board.Board)
        CounterX=0
        while CounterX <= Width - ConnectFour.WinNumber or CounterX == 0:
            
            CounterY=0
            while CounterY <= Height - ConnectFour.WinNumber or CounterY == 0:
                
                ListRD=[]
                for A in range(0,ConnectFour.WinNumber):
                    #print(CounterX + A, CounterY + A,"R")
                    ListRD.append(Board.Board[CounterY + A][CounterX + A])
               


                ListLD=[]
                for A in range(0,ConnectFour.WinNumber):
                    #print(CounterX + A, len(self.Board[CounterX]) - (CounterY + A) - 1,"L")
                    ListLD.append(Board.Board[Height - (CounterY + A) - 1][CounterX + A])


                if _AllSame(ListLD) and ListLD[0] != " ":
                    return [True,ListLD[0]]
                if _AllSame(ListRD) and ListRD[0] != " ":
                    return [True,ListRD[0]]
                CounterY+=1
            CounterX+=1
        return [False]
    
    @staticmethod
    def _CheckRow(Board):
        Width=len(Board.Board[0])
        Height=len(Board.Board)
        CounterX=0
        while CounterX <= Width - ConnectFour.WinNumber or CounterX == 0:
            for Y in range(Height):
                List=[]
                for A in range(ConnectFour.WinNumber):
                    List.append(Board.Board[Y][CounterX + A])
                #print(List)
                if _AllSame(List) and List[0] != " ":
                    return [True,List[0]]
            CounterX+=1
        return [False]

    @staticmethod
    def _CheckCol(Board):
        Width=len(Board.Board[0])
        Height=len(Board.Board)
        CounterY=0
        while CounterY <= Height - ConnectFour.WinNumber or CounterY == 0:
            for X in range(Width):
                List=[]
                for A in range(ConnectFour.WinNumber):
                    List.append(Board.Board[CounterY + A][X])
                #print(List)
                if _AllSame(List) and List[0] != " ":
                    return [True,List[0]]
            CounterY+=1
        return [False]

    @staticmethod
    def _IsFull(Board):
        for X in Board.Board:
            for Y in X:
                if Y == " ":
                    return [False]
        return [True," "]

    @staticmethod
    def CheckWin(Board):
        DiaCheck=ConnectFour._CheckDiagonals(Board)
        if DiaCheck[0] == True:
            return DiaCheck
        
        RowCheck=ConnectFour._CheckRow(Board)
        if RowCheck[0] == True:
            return RowCheck
        
        ColCheck=ConnectFour._CheckCol(Board)
        if ColCheck[0] == True:
            return ColCheck
        
        FullCheck=ConnectFour._IsFull(Board)
        if FullCheck[0] == True:
            return FullCheck
        
        return [False]

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
print(ConnectFour.CheckWin(B))
