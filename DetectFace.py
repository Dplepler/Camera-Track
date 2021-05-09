
# Import Module
import numpy as np  # Numpy is for Array Handler
# Main Module Import From OpenCV Module
import cv2
import socket
import sys  # System
import time

SERVER_PORT = 1308

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_sock:
    listening_sock.bind(('', SERVER_PORT))
    listening_sock.listen(1)
    client_soc, client_address = listening_sock.accept()

    with client_soc:
       

        # Path Here Live Detection Face Capture File
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Open Frontal Camera ( Live Web Camera )
        video_camera = cv2.VideoCapture(1)
        
        
        width  = video_camera.get(3)  # Get width and height of screen
        height = video_camera.get(4)  

        # Params for the PID function
        Px, Ix, Dx = -1 / 160, 0, 0
        Py, Iy, Dy = -0.2 / 100, 0, 0
 
        # Params to be changed later for PID function
        integral_x, integral_y = 0, 0
        differential_x, differential_y = 0, 0
        prev_x, prev_y = 0, 0

        # Live Streaming Face Detection
        while True:
            # Face Frame
            ret, frame = video_camera.read()
            # Face Frame For Detected Face
            grayfaces = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Multi Scale For Multi Faces
            faces = faceCascade.detectMultiScale(
                grayfaces,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(40, 40),
                # resize = (600, 600),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            
            # Created Rectangle For Face
            for (x, y, w, h) in faces:
           
                move_x = ((width / 4) - (x + w) / 2) + 50
                move_y = ((height / 4) - (y + h) / 2) + 50
           
           
                # Calculating integral and differentials values
                integral_x += move_x
                integral_y += move_y

                differential_x = prev_x - move_x
                differential_y = prev_y - move_y

                # Saving previous X and Y
                prev_x = move_x
                prev_y = move_y
                
                # PID function to calculate servo movement
                valx = Px * move_x + Dx * differential_x + Ix * integral_x
                valy = Py * move_y + Dy * differential_y + Iy * integral_y

                # Rounding results
                valx = round(valx, 2)
                valy = round(valy, 2)
                msg = "%+.2f %+.2f" % (valx, valy)
           
                # Send values to client in a static sized format
                client_soc.send(msg.encode())
                tmp = client_soc.recv(1)
                
                
                # Draw red rectangle around face (optional)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 225), 2)
                
            # Show Image For Live Face Detected
            # windows function
            cv2.imshow('FaceDetection', frame)

            # Exit Function
            # Exit program if q pressed

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    

# Destroyed Open Windows And Kill Memory Storage
cv2.destroyAllWindows()