from Arduino import Arduino
import time
board = Arduino(port="COM9")

board.Servos.attach(9)
board.Servos.write(9,180)