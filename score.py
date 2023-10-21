
class Tally:
    def __init__(self)->None:
        self.score: int = 0
        self.backtoback: bool = False
        self.combo: int = 0
        self.tspin: bool = False
        self.b2btext = ""
        self.move_name = ""
    
    def move_down_points(self,lines:int)->None:
        self.score += lines

    def is_combo(self)->None:
        self.combo += 1
        
    def broke_combo(self)->None:
        self.combo = 0
        
    def is_tspin(self)->None:
        self.tspin = True
    
    def get_move_name(self)->(str):
        return self.b2btext, self.move_name
                
    def update(self, lines_cleared:str)->str:
        if lines_cleared == 1:
            self.move_name = "single"
            if self.tspin:
                if self.backtoback: 
                    self.b2btext = "back-to-back "
                    score = 1200
                else: 
                    b2btext = ""
                    score = 800
                self.score = score
                self.backtoback = True
            else:
                self.score += 100
                self.backtoback = False
                self.b2btext = ""
        if lines_cleared == 2: 
            self.move_name = "double"
            if self.tspin:
                if self.backtoback: 
                    self.b2btext = "back-to-back "
                    score = 1800
                else: 
                    self.b2btext = ""
                    score = 1200
                self.score = score
                self.backtoback = True
            else:
                self.score += 300
                self.backtoback = False
                self.b2btext = ""
        if lines_cleared == 3:
            self.move_name = "triple"
            if self.tspin:
                if self.backtoback: 
                    self.b2btext = "back-to-back "
                    score = 2400
                else: 
                    self.b2btext = ""
                    score = 1600
                self.score = score
                self.backtoback = True
            else:
                self.score += 500
                self.backtoback = False
                self.b2btext = ""
        if lines_cleared == 4: 
            self.move_name = "tetris"
            if self.backtoback: 
                self.b2btext = "back-to-back "
                score = 1200
            else: 
                self.b2btext = ""
                score = 800
            self.score += score
            self.backtoback = True
        return self.get_move_name()
        
    def get_score(self)->int:
        return self.score