class Position:
    pid = None
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    rect = None
    paint = None
    psd = None

    @staticmethod
    def MySwapAll():
        if Position.x1 > Position.x2:
            temp = Position.x1
            Position.x1 = Position.x2
            Position.x2 = temp
        if Position.y1 > Position.y2:
            temp = Position.y1
            Position.y1 = Position.y2
            Position.y2 = temp


pos = Position
