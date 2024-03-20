import RPi.GPIO as GPIO
import time

s2 = 19 #Raspberry pi pin 35
s3 = 13 #Raspberry pi pin 33
out = 26 #Raspberry pi pin 37

NUM_CYCLES = 10

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(out, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)

def read_value(a0, a1):
    GPIO.output(s2, a0)
    GPIO.output(s3, a1)
    
    time.sleep(0.1) #Gibe the sensore some time to adjust
    
    #Wait for a full cycle( this will make sure we only count full cycles)
    GPIO.wait_for_edge(out, GPIO.FALLING)
    GPIO.wait_for_edge(out, GPIO.RISING)
    
    start = time.time()
    
    GPIO.wait_for_edge(out, GPIO.FALLING)
    
    #The time that passed while waiting for the out to change
    return(time.time() - start) * 1000000

def loop():
    while True:
        r = (int(read_value(GPIO.LOW, GPIO.LOW)))//3 * 3
        print("r =", int(read_value(GPIO.LOW, GPIO.LOW)))
        time.sleep(0.1)
        
        g = (int(read_value(GPIO.HIGH, GPIO.HIGH)))//3 * 3
        print("g =", int(read_value(GPIO.HIGH, GPIO.HIGH)))
        time.sleep(0.1)
        
        b = (int(read_value(GPIO.LOW, GPIO.HIGH)))//3 * 3
        print("b =", int(read_value(GPIO.LOW, GPIO.HIGH)))
        time.sleep(0.1)
        
        if (b > g) and (b > r):
            print("Blue")
        elif (g > b) and (g > r):
            print("Green")
        elif (r > g) and (r > b):
            print("Red")
        elif (r in range(g , g + 11) or r in range(g - 11 , g)) and (b < r):
            print("Yellow")
        
        time.sleep(1)

if __name__=='__main__':
    setup()
    
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()