import copy
import math
import time
class TranspositionTable:
    def __init__(self,Size:int=81):
        

class BoardState:
    def __init__(self,State:str,Width:int,Height:int,WinLength:int=4):
        self.State=str(State)
        self.Width=Width
        self.Height=Height
        self.WinLength=WinLength
    def ColFull(self,Column:int):
        return self.State.count(str(Column+1)) >= self.Height
    
    def BoardFull(self):
        return len(self.State) >= self.Width * self.Height
    
    def MoveNumber(self):
        return len(self.State)

    @staticmethod
    def _TranslateToBoard(State:str,Width:int,Height:int):
        Board=[[0 for X in range(Width)] for Y in range(Height)]
        for N,Move in enumerate(State):
            for Y in range(Height - 1,-1,-1):
                if Board[Y][int(Move)-1] == 0:
                    Board[Y][int(Move)-1]=1 if N%2==0 else 2
                    break
        return Board

    

    def IsWinningMove(self,Move:int):
        Move=Move+1
        NewState=self.State+str(Move)
        MovePos=(Move-1,self.Height-self.State.count(str(Move))-1,1 if len(self.State)%2==0 else 2)
        Board=BoardState._TranslateToBoard(NewState,self.Width,self.Height)
        #print(MovePos)
        #BoardState(NewState,self.Width,self.Height).Render()
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
class NegMaxSolver:
    MoveOrder=[]
    @staticmethod
    def InitMoveOrder(Width:int):
        for X in range(0,Width):
            NegMaxSolver.MoveOrder.append((Width//2)+(-X//2 if X%2==0 else math.ceil(X/2)))
    @staticmethod
    def NegMax(Board:BoardState,Alpha:int,Beta:int):
        ColumnStates=[Board.ColFull(X) for X in range(Board.Width)]
        #print("Col States",ColumnStates)
        if all(ColumnStates) == True:
            return 0
        
        for X in range(0,Board.Width):
            if ColumnStates[NegMaxSolver.MoveOrder[X]] == False:
                if Board.IsWinningMove(NegMaxSolver.MoveOrder[X]):
                    return (((Board.Width*Board.Height)+1)-Board.MoveNumber())//2

        Max=(((Board.Width*Board.Height)-1)-Board.MoveNumber())//2
        if Beta > Max:
            Beta=Max
            if Alpha >= Beta:
                return Beta
    
        for X in range(0,Board.Width):
            if ColumnStates[NegMaxSolver.MoveOrder[X]] == False:
                
                NewBoard=BoardState(f"{Board.State}{NegMaxSolver.MoveOrder[X]+1}",Board.Width,Board.Height,Board.WinLength)
                
                Score=-NegMaxSolver.NegMax(NewBoard,-Beta,-Alpha)
                if Score >= Beta:
                    return Score
                if Score > Alpha:
                    Alpha=Score
        return Alpha
    @staticmethod
    def Solve(Board:BoardState):
        Min=-(((Board.Width*Board.Height))-Board.MoveNumber())//2
        Max=(((Board.Width*Board.Height)+1)-Board.MoveNumber())//2

        while Min < Max:
            Med = Min + (Max - Min)//2
            if Med <= 0 and Min//2 < Med:
                Med = Min//2
            elif Med >= 0 and Max//2 > Med:
                Med = Max//2
            Score = NegMaxSolver.NegMax(Board, Med, Med + 1)
            if Score <= Med:
                Max = Score
            else:
                Min = Score
        return Min
NegMaxSolver.InitMoveOrder(7)
#print(NegMaxSolver.MoveOrder)
#exit()
"""
B=BoardState("3642756176227637211322113551637574556",7,6)
print(NegMax(B,-(6*7)//2,(6*7)//2))
exit()
"""

Failed=[]
Tested=0
TotalTime=0
StartTime=time.time()
for X in open("Test_L2_R1","r").readlines():
    XSplit=X.split(" ")
    #if abs(int(XSplit[1])) < 6:
    B=BoardState(XSplit[0],7,6)
    State=NegMaxSolver.Solve(B)#NegMax(B,-1,1)#-(6*7)//2,(6*7)//2)
    Tested+=1
    if State != int(XSplit[1]):
        Failed.append([B,State,int(XSplit[1])])
    print("Done",Tested,State,int(XSplit[1]))
print("Tested:",Tested)
print("Failed:",len(Failed))
print("Average Time:",(time.time() - StartTime)/Tested)
#Without iterative deepening - N/A,N/A
