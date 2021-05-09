import RPi.GPIO as GPIO
import time
import socket

SERVER_PORT = 1308
SERVER_IP = "xxx.xxx.xxx.xxx"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to remote computer 
server_address = (SERVER_IP, SERVER_PORT)
sock.connect(server_address)


GPIO.setmode(GPIO.BOARD)   # Setting up pin board

GPIO.setup(11, GPIO.OUT)   # Servo 1 connected to pin 11
GPIO.setup(13, GPIO.OUT)   # Servo 2 connected to pin 13
servo1 = GPIO.PWM(11, 50)  
servo2 = GPIO.PWM(13, 50)

x = 7                     # Starting angle X
y = 2                     # Starting angle Y

servo1.start(x)
servo2.start(y)

time.sleep(0.1)

servo1.ChangeDutyCycle(0)    
servo2.ChangeDutyCycle(0)

while True:
    
    try:
        msg = sock.recv(11).decode()   # Get info message from server
    
    except:
        break                          # If server closed, leave
    try:
        msg_list = msg.split(' ')      # Split message to get an array of position values
        new_x = float(msg_list[0])     # X
        new_y = float(msg_list[1])     # Y
        new_x *= -1                    # Reverse X and Y because my servos are also reversed for some reason
        new_y *= -1
    except:                            # If wrong message was delievered just continue getting messages
        continue
  
    if abs(new_x) < 0.2:               # If change in X is too little, don't bother making the servo shake
        servo1.ChangeDutyCycle(0)
        
    else:
        
        x += new_x                     # Add the angle to move to X
        x = round(x, 2)                # Only two digits after floating point
        
        if x < 15 and x > 0:           # If servo can move
   
            servo1.ChangeDutyCycle(x)  # Change angle
            time.sleep(0.15)        
            servo1.ChangeDutyCycle(0)  # Make servos steady
        
        else:
            x -= new_x                 # If servo can't move, move it back to last position
            
    if abs(new_y) < 0.05:              # If change is too little in Y...
        servo2.ChangeDutyCycle(0)
        
        
    else:
            
        y += new_y
        y = round(y, 2)
        

        if y < 15 and y > 0:
       
            servo2.ChangeDutyCycle(y)
            time.sleep(0.15)
            servo2.ChangeDutyCycle(0)
        else:
            y -= new_y
   
    sock.send("1".encode())

servo1.stop()
servo2.stop()
GPIO.cleanup()
