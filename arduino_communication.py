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
        self.board.Servos.detach(9)
        self.unlocked = True

a = ArduinoCommunication()
print("locked")
a.lock_door()
time.sleep(5)
print("unlocked")
a.unlock_door()
time.sleep(5)
print("locked")
a.lock_door()
time.sleep(5)
print("end")