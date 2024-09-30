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
        self.Moves=len(self.State)
        self.Columns=[(Height + 1) * i for i in range(Width)]
        self.Board=[0,0]
        self.TranslateToBoard()

        self.BitShifts=[1,self.Height,self.Height+1,self.Height+2]
    def ColFull(self,Column:int):
        return self.Columns[Column] - ((self.Height + 1)*Column)  >= self.Height
    
    def BoardFull(self):
        return self.Moves >= self.Width * self.Height
    
    def MoveNumber(self):
        return self.Moves

    def GetMask(self):
        return self.Board[0] | self.Board[1]

    def TranslateToBoard(self):

        for N,Move in enumerate(self.State):
            #((self.Width * self.Columns[int(Move) - 1]) + (int(Move) - 1))
            self.Board[N%2]|=1 << self.Columns[int(Move)-1]
            
            self.Columns[int(Move) - 1]+=1

    def GetNonLoseMove(self,Move:int):
        TempBitboard=[self.Board[0],self.Board[1]]
        TempColumns=copy.copy(self.Columns)
        TempBitboard[self.Moves%2]|=1 << TempColumns[Move]
        TempColumns[Move]+=1
        for X in NegMaxSolver.MoveOrder:
            if BoardState.IsWinningMove(X,TempBitboard,TempColumns,self.BitShifts,self.Moves+1):
                return False
        return True
        
    @staticmethod
    def IsWinningMove(Move:int,Board:list,Columns:list,BitShifts:list,Moves:int):
        Move=int(Move)
        TempBitBoard=Board[Moves%2] | (1 << Columns[Move])
        
        for Shift in BitShifts:
            Test = TempBitBoard & (TempBitBoard >> Shift)
            if Test & (Test >> 2 * Shift):
                return True
        return False
    def Render(self):
        Output=[]
        for Y in range(self.Height-1,-1,-1):
            Row=[]
            for X in range(self.Width):
                Pos=1 << ((self.Height + 1) * X)+Y
                if self.Board[0] & Pos == Pos:
                    Row.append("🔴")
                elif self.Board[1] & Pos == Pos:
                    Row.append("🟡")
                else:
                    Row.append("  ")
            Output.append("|".join(Row))
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
            return 0,-1
        
        for X in NegMaxSolver.MoveOrder:#range(0,Board.Width):
            if ColumnStates[X] == False:
                if BoardState.IsWinningMove(X,Board.Board,Board.Columns,Board.BitShifts,Board.Moves):
                    #print(X,Board.MoveNumber())
                    return (((Board.Width*Board.Height)+1)-Board.MoveNumber())//2,X
        
        #TempHash=BoardState._TranslateToBoard(Board.State,Board.Width,Board.Height)
        Hash=hash(tuple(Board.Board))
        """Hash=[]
        for X in Board.Board:
            Hash+=X#[str(Y) for Y in X]
        Hash="".join(Hash)"""
        Max=(((Board.Width*Board.Height)-1)-Board.MoveNumber())//2
        
        Transvalue=int(TransTable.Get(Hash))
        if Transvalue != 0:
            Max=Transvalue + Board.MinScore - 1
        
        if Beta > Max:
            Beta=Max
            if Alpha >= Beta:
                return Beta,-1
        BestMove=-1
        for X in NegMaxSolver.MoveOrder:
            if ColumnStates[X] == False:
                #if Board.GetNonLoseMove(X):
                NewBoard=BoardState(f"{Board.State}{X+1}",Board.Width,Board.Height,Board.WinLength)
                
                Score,_=NegMaxSolver.NegMax(NewBoard,-Beta,-Alpha,TransTable)
                Score=-Score
                if Score >= Beta:
                    return Score,X
                if Score > Alpha:
                    Alpha=Score
                    BestMove=X
        TransTable.Put(Hash,Alpha - Board.MinScore + 1)
        return Alpha,BestMove
    @staticmethod
    def Solve(Board:BoardState,Weak:bool=False,TableSize:int=81):
        TransTable=TranspositionTable(TableSize)
        Min=-(((Board.Width*Board.Height))-Board.MoveNumber())//2
        Max=(((Board.Width*Board.Height)+1)-Board.MoveNumber())//2
        if Weak:
            Min=-1
            Max=1
        BestMove=-1
        while Min < Max:
            Med = Min + (Max - Min)//2
            if Med <= 0 and Min//2 < Med:
                Med = Min//2
            elif Med >= 0 and Max//2 > Med:
                Med = Max//2
            Score,Move = NegMaxSolver.NegMax(Board, Med, Med + 1,TransTable)
            if Score <= Med:
                Max = Score
            else:
                Min = Score
                BestMove=Move
        return Min,BestMove
NegMaxSolver.InitMoveOrder(7)

B=BoardState("123372255534145111472522133344",7,6)
B.Render()
print(NegMaxSolver.Solve(B,False))
exit()
Failed=[]
Tested=0
TotalTime=0
StartTime=time.time()
for X in open("Test_L2_R1","r").readlines():
    XSplit=X.split(" ")
    #if abs(int(XSplit[1])) < 6:
    B=BoardState(XSplit[0],7,6)
    State=NegMaxSolver.Solve(B,False,TableSize=8024)#NegMax(B,-1,1)#-(6*7)//2,(6*7)//2)
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
#With transpostion table size 1024 - 0.1632602
#With in built hash function - 0.14249
#With bitboard - 0.07

#Test_L1_r1:
#Inital - N/A