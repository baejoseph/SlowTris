color = (int,int,int)

class Colors: 
    
    dark_grey:color = (26,31,40)
    green:color = (47,230,23)
    red:color = (232,18,18)
    orange:color = (226,116,17)
    yellow:color = (237,234,4)
    purple:color = (116,0,247)
    cyan:color = (21,204,209)
    blue:color = (13,64,216)
    white:color = (255,255,255)
    dark_blue:color = (44, 44, 127)
    light_blue:color = (59, 85, 162)
    
    @classmethod
    def get_cell_colors(cls)->[color]:
        return [cls.dark_grey,
                cls.orange, 
                cls.blue, 
                cls.cyan, 
                cls.yellow, 
                cls.green, 
                cls.purple, 
                cls.red]