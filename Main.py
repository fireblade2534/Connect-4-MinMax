import copy
class BoardState:
    def __init__(self,Board):
        self.Board=Board
    @staticmethod
    def CreateBlank(Width,Height):
        return BoardState([[" " for X in range(Width)] for Y in range(Height)])
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
    def ColFull(Board,Column):
        for Y in Board.Board:
            if Y[Column] == " ":
                return False
        return True

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

def NegMax(Board:BoardState,MoveNumber:int):
    Width=len(Board.Board[0])
    Height=len(Board.Board)
    ColumnStates=[ConnectFour.ColFull(Board,X) for X in range(Width)]
    if all(ColumnStates) == True:
        return 0
    
    BestScore=-Width * Height 
    #In the future implement it so that it only checks around the dropped peice for if its a win
    for X in range(0,Width):
        if ColumnStates[X] == False:
            NewBoard=Board.CreateCopy()
            ConnectFour.DropPiece(NewBoard,X,"Y" if MoveNumber%2 == 0 else "R")
            if ConnectFour.CheckWin(NewBoard)[0] == True:
                return (((Width*Height)+1)-MoveNumber)//2
            Score=-NegMax(NewBoard,MoveNumber+1)
            if Score > BestScore:
                BestScore=Score
    return BestScore




B=BoardState.CreateBlank(7,6)

Moves="75662564375666511575212332122171447733"
for N,X in enumerate(Moves):
    ConnectFour.DropPiece(B,int(X)-1,"Y" if N%2==0 else "R")
ConnectFour.Render(B)
print(NegMax(B,len(Moves)))
#print(ConnectFour.CheckWin(B))
