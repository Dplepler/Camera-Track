# Camera-Track
Have you ever wanted a camera to track and follow your face? Probably not, but if you ever do: you can use this code, with a RaspberryPi.

What this code does is detect your beautiful/ugly face with OpenCV and calculate it's distance in pixels from the center of the camera.
Now we can translate these pixels into an angle for the X and Y servos to move with and voilà! Now you're the center of attention again :)

# How to use
- Connect the X axis servo to pin 11
- Connect the Y axis servo to pin 13
- Run DetectFace.py from your computer, and Servos.py from your RaspberryPi

# Note
Yes I didn't connect my camera to the RaspberryPi, sue me for hating on 0.5 FPH
