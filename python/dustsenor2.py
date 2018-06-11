import time
import os
import onionGpio
import math

gpioNum = 18

gpioObj	= onionGpio.OnionGpio(gpioNum) 

# set to input 
status 	= gpioObj.setInputDirection() 

# read and print the value once every 30 second 
loop = 1 
while loop == 1: 	
    value = gpioObj.getValue() 
#    print 'GPIO%d input value: %d'%(gpioNum, int(value)) 	 	

    interval = low_ticks + high_ticks

    if interval > 0:
        ratio = float(low_ticks)/float(interval)*100.0
        conc = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62;
    else:
        ratio = 0
        conc = 0.0

    start_tick = None
    last_tick = None
    low_ticks = 0
    high_ticks = 0


    if start_tick is not None:
        ticks = tickDiff(last_tick, tick)
        last_tick = tick

    if level == 0: # Falling edge.
        high_ticks = high_ticks + ticks

    elif level == 1: # Rising edge.
        low_ticks = low_ticks + ticks
        
#    else: # timeout level, not used
#        pass
    
    else:
        start_tick = tick
        last_tick = tick
 
    '''
    Convert concentration of PM2.5 particles per 0.01 cubic feet to µg/ metre cubed
    this method outlined by Drexel University students (2009) and is an approximation
    does not contain correction factors for humidity and rain
    '''
    # Assume all particles are spherical, with a density of 1.65E12 µg/m3
    densitypm25 = 1.65 * math.pow(10, 12)
        
    # Assume the radius of a particle in the PM2.5 channel is .44 µm
    rpm25 = 0.44 * math.pow(10, -6)
        
    # Volume of a sphere = 4/3 * pi * radius^3
    volpm25 = (4/3) * math.pi * (rpm25**3)
        
    # mass = density * volume
    masspm25 = densitypm25 * volpm25
        
    # parts/m3 =  parts/foot3 * 3531.5
    # µg/m3 = parts/m3 * mass in µg
    concentration_ugm3 = concentration_pcf * 3531.5 * masspm25
        
    return concentration_ugm3

    '''
    Convert concentration of PM2.5 particles in µg/ metre cubed to the USA 
    Environment Agency Air Quality Index - AQI
    https://en.wikipedia.org/wiki/Air_quality_index
    Computing_the_AQI
    https://github.com/intel-iot-devkit/upm/pull/409/commits/ad31559281bb5522511b26309a1ee73cd1fe208a?diff=split
    '''
        
    cbreakpointspm25 = [ [0.0, 12, 0, 50],\
                         [12.1, 35.4, 51, 100],\
                         [35.5, 55.4, 101, 150],\
                         [55.5, 150.4, 151, 200],\
                         [150.5, 250.4, 201, 300],\
                         [250.5, 350.4, 301, 400],\
                         [350.5, 500.4, 401, 500], ]
                        
    C=ugm3
        
    if C > 500.4:
        aqi=500

    else:
        for breakpoint in cbreakpointspm25:
            if breakpoint[0] <= C <= breakpoint[1]:
                Clow = breakpoint[0]
                Chigh = breakpoint[1]
                Ilow = breakpoint[2]
                Ihigh = breakpoint[3]
                aqi=(((Ihigh-Ilow)/(Chigh-Clow))*(C-Clow))+Ilow
        
    return aqi


    # Use 30s for a properly calibrated reading.
    time.sleep(30)
    
    # get the gpio, ratio and concentration in particles / 0.01 ft3
    g, r, c = value.read()
      
    if (c==1114000.62):
        print "Error\n"
        continue

    print "Air Quality Measurements for PM2.5:"
    print "  " + str(int(c)) + " particles/0.01ft^3"

    # convert to SI units
    concentration_ugm3=s.pcs_to_ugm3(c)
    print "  " + str(int(concentration_ugm3)) + " ugm^3"
      
    # convert SI units to US AQI
    # input should be 24 hour average of ugm3, not instantaneous reading
    aqi=s.ugm3_to_aqi(concentration_ugm3)
      
    print "  Current AQI (not 24 hour avg): " + str(int(aqi))
    print ""

    
# Follow guide on how to install fswebcam https://onion.io/taking-photos-with-a-usb-webcam-on-the-omega/
# SD Card Path    /tmp/mounts/SD-P1/
# Trigger FSWebcam to take photo
# os.system('fswebcam --no-banner -r 1280x720 /tmp/mounts/SD-P1/capture-"%Y-%m-%d_%H%M%S".jpg')


