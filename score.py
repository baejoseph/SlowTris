score_update_rulset:[{}] = [{'movename': '',
                             'b2btspinscore': 0,
                             'tspinscore': 0,
                             'score': 0},
                            {'movename': 'single',
                             'b2btspinscore': 1200,
                             'tspinscore': 800,
                             'score': 100},
                            {'movename': 'double',
                             'b2btspinscore': 1800,
                             'tspinscore': 1200,
                             'score': 300},
                            {'movename': 'triple',
                             'b2btspinscore': 2400,
                             'tspinscore': 1600,
                             'score': 500}]


class Tally:
    def __init__(self)->None:
        self.reset()
        
    def reset(self)->None:
        self.score: int = 0
        self.backtoback: bool = False
        self.combo: int = -1
        self.streak: int = 0
        self.tspin: bool = False
        self.b2btext = ""
        self.tspintext = ""
        self.move_name = ""
    
    def move_down_points(self,lines:int)->None:
        self.score += lines

    def increment_combo(self)->None:
        self.combo += 1
        
    def reset_combo(self)->None:
        self.score += max(0,self.combo) * 50
        self.combo = -1
        
    def get_combo(self)->int:
        if self.combo > 0:
            return self.combo
        else: return None
    
    def increment_streak(self)->None:
        self.streak += 1
        
    def reset_streak(self)->None:
        self.streak = 0
        
    def get_streak(self)->int:
        if self.streak > 1 :
            return self.streak
        else: return None
        
    def is_tspin(self)->None:
        self.tspin = True
    
    def get_move_name(self)->(str):
        return self.b2btext, self.tspintext, self.move_name
                
    def update(self, lines_cleared:int)->None:
        if lines_cleared < 4:
            self.move_name = score_update_rulset[lines_cleared]['movename']
            if self.tspin:
                self.tspintext = "T-spin"
                if self.backtoback: 
                    self.b2btext = "back-to-back "
                    score = score_update_rulset[lines_cleared]['b2btspinscore']
                else: 
                    b2btext = ""
                    score = score_update_rulset[lines_cleared]['tspinscore']
                self.score += score
                self.backtoback = True
            else:
                self.tspintext = ""
                self.score += score_update_rulset[lines_cleared]['score']
                self.backtoback = False
                self.b2btext = ""
        if lines_cleared == 4: 
            self.tspintext = ""
            self.move_name = "tetris"
            if self.backtoback: 
                self.b2btext = "back-to-back "
                score = 1200
            else: 
                self.b2btext = ""
                score = 800
            self.score += score
            self.backtoback = True
        
    def get_score(self)->int:
        return self.score