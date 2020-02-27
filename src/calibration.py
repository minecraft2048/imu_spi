import serial
from time import sleep

accZ_up_total = 0.0
accZ_down_total = 0.0
g = 9.81


#Get data from Arduino board, with count as the how many data points will be collected each run
def acquire_data(ser_obj,count=10):
    accX = 0
    accY = 0
    accZ = 0
    with ser_obj as ser:
        while(b'restart' not in ser.readline()):
            pass
        print("Starting measurement")
        for i in range(count):
            rd = ser.readline().split(b'\t')
            accX += float(rd[0])
            accY += float(rd[1])
            accZ += float(rd[2])
            print(f"accX:{float(rd[0])} accY:{float(rd[1])} accZ:{float(rd[2])}")
    return (accX/count, accY/count, accZ/count)


print("Set the board right side up")
sleep(4)
_,_,accZ_up_avg = acquire_data(serial.Serial('/dev/ttyACM0',9600))
print("Flip the board Z axis down")
sleep(4)
_,_,accZ_down_avg = acquire_data(serial.Serial('/dev/ttyACM0',9600))
print("Flip the board Y axis down")
sleep(4)
_,accY_down_avg,_ = acquire_data(serial.Serial('/dev/ttyACM0',9600))
print("Flip the board Y axis up")
sleep(4)
_,accY_up_avg,_ = acquire_data(serial.Serial('/dev/ttyACM0',9600))
print("Flip the board X axis down")
sleep(4)
accX_down_avg,_,_ = acquire_data(serial.Serial('/dev/ttyACM0',9600))
print("Flip the board X axis up")
sleep(4)
accX_up_avg,_,_ = acquire_data(serial.Serial('/dev/ttyACM0',9600))



print(f"Avg accX up: {accX_up_avg} down: {accX_down_avg}")
print(f"Avg accY up: {accY_up_avg} down: {accY_down_avg}")
print(f"Avg accZ up: {accZ_up_avg} down: {accZ_down_avg}")

# http://cache.freescale.com/files/sensors/doc/app_note/AN4399.pdf page 8 algorithm
# TODO: Improve calibration algorithm

Wxx = 2*g/(accX_down_avg - accX_up_avg)
Vx =  -(accX_down_avg + accX_up_avg)*g/(accX_down_avg - accX_up_avg)

Wyy = 2*g/(accY_down_avg - accY_up_avg)
Vy =  -(accY_down_avg + accY_up_avg)*g/(accY_down_avg - accY_up_avg)

Wzz = 2*g/(accZ_down_avg - accZ_up_avg)
Vz =  -(accZ_down_avg + accZ_up_avg)*g/(accZ_down_avg - accZ_up_avg)

print(f"Calibration constants")
print(f"X axis scale: {Wxx} offset: {Vx}")
print(f"Y axis scale: {Wyy} offset: {Vy}")
print(f"Z axis scale: {Wzz} offset: {Vz}")
print(f"Running IMU with calibration constant, press ctrl-c to terminate")

with serial.Serial('/dev/ttyACM0',9600) as ser:
    while(b'restart' not in ser.readline()):
        pass
    print("Starting measurement")
    for i in range(10):
        rd = ser.readline().split(b'\t')
        accX = float(rd[0])
        accY = float(rd[1])
        accZ = ((float(rd[2]))*Wzz + Vz)
        print(f"accX:{accX} accY:{accY} accZ:{accZ}")
        accZ_up_total += accZ
