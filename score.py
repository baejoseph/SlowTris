
class Tally:
    def __init__(self)->None:
        self.score: int = 0
        self.backtoback: bool = False
        self.combo: int = 0
        self.tspin: bool = False
    
    def move_down_points(self,lines:int)->None:
        self.score += lines

    def is_combo(self)->None:
        self.combo += 1
        
    def broke_combo(self)->None:
        self.combo = 0
        
    def is_tspin(self)->None:
        self.tspin = True
                
    def update(self, lines_cleared:str)->str:        
        if lines_cleared == 1:
            if self.tspin:
                if self.backtoback: 
                    b2btext = "back to back "
                    score = 1200
                else: 
                    b2btext = ""
                    score = 800
                self.score = score
                self.backtoback = True
                return f"{b2btext}T-spin single"
            else:

                self.score += 100
                self.backtoback = False
                return 'single'
        if lines_cleared == 2: 
            if self.tspin:
                if self.backtoback: 
                    b2btext = "back to back "
                    score = 1800
                else: 
                    b2btext = ""
                    score = 1200
                self.score = score
                self.backtoback = True
                return f"{b2btext}T-spin double"
            else:
                self.score += 300
                self.backtoback = False
                return 'double'
        if lines_cleared == 3:
            if self.tspin:
                if self.backtoback: 
                    b2btext = "back to back "
                    score = 2400
                else: 
                    b2btext = ""
                    score = 1600
                self.score = score
                self.backtoback = True
                return f"{b2btext}T-spin triple"
            else:
                self.score += 500
                self.backtoback = False
                return 'triple'
        if lines_cleared == 4: 
            if self.backtoback: 
                b2btext = "back to back "
                score = 1200
            else: 
                b2btext = ""
                score = 800
            self.score += score
            self.backtoback = True
            return f"{b2btext}tetris"
        
    def get_score(self)->int:
        return self.score