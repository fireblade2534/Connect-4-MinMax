import copy
import math
import time
from collections import OrderedDict

class TranspositionTable:
    def __init__(self,Size:int=256):
        self.Size=Size
        self.Table=OrderedDict()

    def Put(self,Index,Value):
        if Index in self.Table:
            self.Table.move_to_end(Index)
        self.Table[Index]=Value
        if len(self.Table) > self.Size:
            self.Table.popitem(last=False)

    def Get(self,Index):
        if Index in self.Table:
            self.Table.move_to_end(Index)
            return self.Table[Index]
        return 0

class BoardState:
    def __init__(self,State:str,Width:int,Height:int,WinLength:int=4):
        self.State=str(State)
        self.Width=Width
        self.Height=Height
        self.WinLength=WinLength
        self.MinScore=-(((Width*Height))//2)+3
        self.MaxScore=(((Width*Height)+1)//2)-3
        self.Board=BoardState._TranslateToBoard(self.State,self.Width,self.Height)
    def ColFull(self,Column:int):
        return self.State.count(str(Column+1)) >= self.Height
    
    def BoardFull(self):
        return len(self.State) >= self.Width * self.Height
    
    def MoveNumber(self):
        return len(self.State)

    @staticmethod
    def _TranslateToBoard(State:str,Width:int,Height:int):
        Board=[["0" for X in range(Width)] for Y in range(Height)]
        for N,Move in enumerate(State):
            for Y in range(Height - 1,-1,-1):
                if Board[Y][int(Move)-1] == "0":
                    Board[Y][int(Move)-1]="1" if N%2==0 else "2"
                    break
        return Board

    

    def IsWinningMove(self,Move:int):
        Move+=1
        NewState=self.State+str(Move)
        MovePos=(Move-1,self.Height-self.State.count(str(Move))-1,"1" if len(self.State)%2==0 else "2")
        #Board=BoardState._TranslateToBoard(self.State,self.Width,self.Height)
        
        #print(MovePos)
        #BoardState(self.State,self.Width,self.Height).Render()
        #print("\n")
        #BoardState(NewState,self.Width,self.Height).Render()
        #print(Move)
        if NewState.count(str(Move)) > 3:
            if self.Board[MovePos[1]+1][MovePos[0]] == MovePos[2] and self.Board[MovePos[1]+2][MovePos[0]] == MovePos[2] and self.Board[MovePos[1]+3][MovePos[0]] == MovePos[2]:
                return True
        
        RowN=0
        DiaN1=0
        DiaN2=0
        #print(MovePos)
        for OX in range(-self.WinLength+1,self.WinLength):
            if OX != 0:
                NewX=MovePos[0]+OX
                NewY=MovePos[1]+OX
                if NewX >= 0 and NewX < self.Width:
                    if self.Board[MovePos[1]][NewX] == MovePos[2]:
                        RowN+=1
                    else:
                        RowN=0
                    if RowN >= self.WinLength-1:
                        #print("ROW1")
                        return True
                    
                    
                    if NewY >=0 and NewY < self.Height:
                        #print(NewX,NewY)
                        if self.Board[NewY][NewX] == MovePos[2]:
                            DiaN1+=1
                        else:
                            DiaN1=0
                        if DiaN1 >= self.WinLength-1:
                            #print("DIA1")
                            return True
                NewX=MovePos[0]-OX     
                if NewX >= 0 and NewX < self.Width:
                    if NewY >=0 and NewY < self.Height:
                        if self.Board[NewY][NewX] == MovePos[2]:
                            DiaN2+=1
                        else:
                            DiaN2=0
                        if DiaN2 >= self.WinLength-1:
                            #print("DIA2")
                            return True
        return False
    @staticmethod
    def _FormatPiece(Piece):
        if Piece == "1":
            return "🔴"
        if Piece == "2":
            return "🟡"
        if Piece == "0":
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
    def NegMax(Board:BoardState,Alpha:int,Beta:int,TransTable:TranspositionTable):
        ColumnStates=[Board.ColFull(X) for X in range(Board.Width)]
        #print("Col States",ColumnStates)
        if all(ColumnStates) == True:
            return 0
        
        for X in NegMaxSolver.MoveOrder:#range(0,Board.Width):
            if ColumnStates[X] == False:
                if Board.IsWinningMove(X):
                    return (((Board.Width*Board.Height)+1)-Board.MoveNumber())//2
        
        #TempHash=BoardState._TranslateToBoard(Board.State,Board.Width,Board.Height)
        Hash=[]
        for X in Board.Board:
            Hash+=X#[str(Y) for Y in X]
        Hash="".join(Hash)
        Max=(((Board.Width*Board.Height)-1)-Board.MoveNumber())//2
        
        Transvalue=int(TransTable.Get(Hash))
        if Transvalue != 0:
            Max=Transvalue + Board.MinScore - 1
        
        if Beta > Max:
            Beta=Max
            if Alpha >= Beta:
                return Beta
    
        for X in NegMaxSolver.MoveOrder:
            if ColumnStates[X] == False:
                
                NewBoard=BoardState(f"{Board.State}{X+1}",Board.Width,Board.Height,Board.WinLength)
                
                Score=-NegMaxSolver.NegMax(NewBoard,-Beta,-Alpha,TransTable)
                if Score >= Beta:
                    return Score
                if Score > Alpha:
                    Alpha=Score
        TransTable.Put(Hash,Alpha - Board.MinScore + 1)
        return Alpha
    @staticmethod
    def Solve(Board:BoardState,Weak:bool=False,TableSize:int=81):
        TransTable=TranspositionTable(TableSize)
        Min=-(((Board.Width*Board.Height))-Board.MoveNumber())//2
        Max=(((Board.Width*Board.Height)+1)-Board.MoveNumber())//2
        if Weak:
            Min=-1
            Max=1
        while Min < Max:
            Med = Min + (Max - Min)//2
            if Med <= 0 and Min//2 < Med:
                Med = Min//2
            elif Med >= 0 and Max//2 > Med:
                Med = Max//2
            Score = NegMaxSolver.NegMax(Board, Med, Med + 1,TransTable)
            if Score <= Med:
                Max = Score
            else:
                Min = Score
        return Min
NegMaxSolver.InitMoveOrder(7)

#B=BoardState("6672375354252731116762237724",7,6)
#print(NegMaxSolver.Solve(B,False))
#exit()


Failed=[]
Tested=0
TotalTime=0
StartTime=time.time()
for X in open("Test_L2_R1","r").readlines():
    XSplit=X.split(" ")
    #if abs(int(XSplit[1])) < 6:
    B=BoardState(XSplit[0],7,6)
    State=NegMaxSolver.Solve(B,False)#NegMax(B,-1,1)#-(6*7)//2,(6*7)//2)
    Tested+=1
    if State != int(XSplit[1]):
        Failed.append([B,State,int(XSplit[1])])
    print("Done",Tested,State,int(XSplit[1]))
print("Tested:",Tested)
print("Failed:",len(Failed))
print("Average Time:",(time.time() - StartTime)/Tested)
#Test_L2_R1:
#Without iterative deepening - N/A,N/A
#With iterative deepening - 1.0694399
#With transpositiona table v1 - 1.2
#With Claude compute board list in init - 0.407150009
#With fixed tranposition table - 0.2904
#With O1 transposition table - 0.2765
#With strings in board list - 0.2647