from Arduino import Arduino
import time

class ArduinoCommunication:
    def __init__(self):
        self.board = Arduino(port="COM9")
        self.board.Servos.attach(9)
        self.board.Servos.write(9,180)

        self.unlocked = False
    
    def lock_door(self):
        if self.unlocked:
            self.board.Servos.attach(9)
            self.board.Servos.write(9, 180)
            self.unlocked = False

    def unlock_door(self):
        if not self.unlocked:
            self.board.Servos.detach(9)
            self.unlocked = True