### CLASS MODULE THAT IS USED TO STORE AND VERIFY IF ANY CASTLING RULE HAS BEEN BROKEN IN A GAME.
class CastleCheck(): 
    # there are four types of castles we need to check for. 
    # white and black, king and queen side castles. 
    def __init__(self, wks, bks, wqs, bqs): 
        self.bqs = bqs
        self.bks = bks
        self.wqs = wqs
        self.wks = wks