import os
from time import sleep

os.system('fswebcam --no-banner -r 1280x720 /tmp/mounts/SD-P1/capture-"%Y-%m-%d_%H%M%S".jpg')
