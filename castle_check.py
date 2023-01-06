
### Class that checks if any castling rule has been broken for any of the four possible castling actions.
### This class is used to store the state of the rules of castle during game execution.
class CastleCheck(): 
    # there are four types of castles we need to check for. 
    # white and black, king and queen side castles. 
    def __init__(self, wks, bks, wqs, bqs): 
        self.bqs = bqs
        self.bks = bks
        self.wqs = wqs
        self.wks = wks
    





