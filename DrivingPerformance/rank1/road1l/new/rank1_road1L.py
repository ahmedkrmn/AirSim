import os.path as path
import time
import math
from TurningPerf import *
from speedPerf import *
from stopPerf import *
from ContinousPerf import *

#log_path = path.expanduser('~\\Documents\\AirSim\\airsim_rec.txt')
log_path = path.expanduser('rank1_road1l_focused.txt')


def analyse():
    # Define road stripes for first square.
    line1_1 = [[159, 161], [-6, 4]]
    line1_2 = [[165, 173], [-11.5, -9.5]]
    # Define the speed sign place
    Speed_sign = [[165, 173.5], [-120, -105]]
    # Define the stop sign place and the boundary flags for performance testing.
    Stop_sign = [[165, 173.5], [-441, -439]]
    # Define road lane boundaries to compute deviation from the road.
    Deviation1 = [[0, 165], [-6, 2]]
    Deviation2 = [[165, 173], [-600, -9]]


    ContinousPerf = []
    LastContPerf = 1
    CrossedSpeedSign = False
    CrossedStopSign = False
    crossedTurn1 = False
        
    TurnPerf = []
    SpeedPerf = 1
    StopPerf = 1
    TotalDevPerf = 0
    print("RECORDING STARTED!")
    with open(log_path, 'r') as f:
        # loop on the recorded file line by line and split the line.
        cnt = 0
        for l in f.readlines():
            line = l.split()
			# Check whether the line is empty.
            if(len(line) == 0 or cnt<10):
                cnt+=1
                continue
			# Data extraction.
            time, x, y, z, Q_W,	Q_X, Q_Y, Q_Z, Throttle, Steering, Brake, Gear, Handbrake, RPM, Speed  = float(line[0]), float(line[1]), float(line[2]),float(line[3]),float(line[4]),float(line[5]),float(line[6]),float(line[7]),float(line[8]),float(line[9]),float(line[10]),float(line[11]),float(line[12]),float(line[13]),float(line[14])

            cnt+=1
			#------------------------------- turning performance part-------------------------------------
            TurnPerfTemp,crossedTurn1 = UpLeftLeftLane(line1_1, line1_2, crossedTurn1, x, y)
            if(TurnPerfTemp!=0):
                TurnPerf.append(TurnPerfTemp)
            

            # ------------------------------- Speed limit performance part-------------------------------------
            SpeedPerf,CrossedSpeedSign = SpeedSign(Speed_sign, CrossedSpeedSign, x, y, Speed, SpeedPerf)
           

			#------------------------------- stop sign performance part-------------------------------------
            StopPerf,CrossedStopSign = StopSignLeft(Stop_sign, CrossedStopSign, x, y, Speed, StopPerf)
			


			#------------------------------- continous deviation performance part-------------------------------------
            if(crossedTurn1):
                ContinousPerf.append([time,LastContPerf])
                TotalDevPerf+=LastContPerf
                continue
            LastContPerfTemp1 = upwardLeft(Deviation1,x,y)
            LastContPerfTemp2 = leftwardDown(Deviation2,x,y)
            if(LastContPerfTemp1!=0):
                LastContPerf = LastContPerfTemp1
                ContinousPerf.append([time,LastContPerf])
            if(LastContPerfTemp2!=0):
                LastContPerf = LastContPerfTemp2
                ContinousPerf.append([time,LastContPerf])        
            TotalDevPerf+=LastContPerf
#=============================================result================================================
        DevPerf = math.ceil(TotalDevPerf/(cnt-10))
        print("performance turn: " + str(sum(TurnPerf)))
        print("performance speed: " + str(SpeedPerf))
        print("performance stop: " + str(StopPerf)) 
        print("performance deviation: " + str(DevPerf))
        return (DevPerf+SpeedPerf+StopPerf+sum(TurnPerf))/4,ContinousPerf



p,CP = analyse()
#print(CP)
outfile = open("Rank1Road1LFocusedResult.txt","w+")
outfile.write("RANK: 1\n")
outfile.write("OVERALL PERFORMANCE: " + str(100-(p/5)*100) + "%\n")
outfile.write("EPOCH TIMESTAMP(Every ~1000 ms)      Performance( Scale: 1-5)\n")
for i in CP:
    outfile.write(str(i[0]) + "                        " + str(i[1]) + "\n")
