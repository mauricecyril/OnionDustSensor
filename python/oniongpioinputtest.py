import time 
import onionGpio 

gpioNum = 18

gpioObj	= onionGpio.OnionGpio(gpioNum) 

# set to input 
status 	= gpioObj.setInputDirection() 

# read and print the value once every 30 second 
loop = 1 
while loop == 1: 	
    value = gpioObj.getValue() 
    print 'GPIO%d input value: %d'%(gpioNum, int(value)) 	 	

    time.sleep(0.01)

