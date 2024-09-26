import copy
class BoardState:
    def __init__(self,State:str,Width:int,Height:int,WinLength:int=4):
        self.State=str(State)
        self.Width=Width
        self.Height=Height
        self.WinLength=WinLength
    def ColFull(self,Column:int):
        return self.State.count(str(Column)) >= self.Width
    
    def BoardFull(self):
        return len(self.State) >= self.Width * self.Height
    
    @staticmethod
    def _TranslateToBoard(State:str,Width:int,Height:int):
        Board=[[0 for X in range(Width)] for Y in range(Height)]
        for N,Move in enumerate(State):
            for Y in range(len(Board) - 1,-1,-1):
                if Board[Y][int(Move)-1] == 0:
                    Board[Y][int(Move)-1]=1 if N%2==0 else 2
                    break
        return Board

    

    def IsWinningMove(self,Move:int):
        NewState=self.State+str(Move)
        MovePos=(Move-1,self.Height-self.State.count(str(Move))-1,1 if len(self.State)%2==0 else 2)
        Board=BoardState._TranslateToBoard(NewState,self.Width,self.Height)
        
        if NewState.count(str(Move)) > 3:
            if Board[MovePos[1]+1][MovePos[0]] == MovePos[2] and Board[MovePos[1]+2][MovePos[0]] == MovePos[2] and Board[MovePos[1]+3][MovePos[0]] == MovePos[2]:
                return True
        
        RowN=0
        DiaN1=0
        DiaN2=0
        #print(MovePos)
        for OX in range(-3,4):
            NewX=MovePos[0]+OX
            NewY=MovePos[1]+OX
            if NewX >= 0 and NewX < self.Width:
                if Board[MovePos[1]][NewX] == MovePos[2]:
                    RowN+=1
                else:
                    RowN=0
                if RowN >= self.WinLength:
                    return True
                
                
                if NewY >=0 and NewY < self.Height:
                    #print(NewX,NewY)
                    if Board[NewY][NewX] == MovePos[2]:
                        DiaN1+=1
                    else:
                        DiaN1=0
                    if DiaN1 >= self.WinLength:
                        return True
            NewX=MovePos[0]-OX     
            if NewX >= 0 and NewX < self.Width:
                if NewY >=0 and NewY < self.Height:
                    if Board[NewY][NewX] == MovePos[2]:
                        DiaN2+=1
                    else:
                        DiaN2=0
                    if DiaN2 >= self.WinLength:
                        return True
        return False
    @staticmethod
    def _FormatPiece(Piece):
        if Piece == 1:
            return "🔴"
        if Piece == 2:
            return "🟡"
        if Piece == 0:
            return "  "
    
    def Render(self):
        Board=BoardState._TranslateToBoard(self.State,self.Width,self.Height)
        Output=[]
        for Y in range(self.Height):
            Output.append("|".join([BoardState._FormatPiece(Board[Y][X]) for X in range(self.Width)]))
        print(f"\n{('--+'*self.Width)[:-1]}\n".join(Output))

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




#B=BoardState.CreateBlank(7,6)
Moves="1224334534"
B=BoardState(Moves,7,6)
B.Render()

#CHECK OTHER DIAG
Move=4
print(B.IsWinningMove(Move))
B.State+=str(Move)
B.Render()

"""
for N,X in enumerate(Moves):
    ConnectFour.DropPiece(B,int(X)-1,"Y" if N%2==0 else "R")
ConnectFour.Render(B)
print(NegMax(B,len(Moves)))
"""

