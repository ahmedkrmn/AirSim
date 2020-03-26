import os.path as path
import time
import math

# Define road stripes for first square.
strip_1 = [[159, 161], [-6, 4]]
strip_2 = [[165, 173], [-11.5, -9.5]]

# Define the ranges for turning performance
Rang1_1 = [[169, 171], [-11.5, -9.5]]
Rang1_2 = [[171, 171.5], [-11.5, -9.5]]
Rang2_1 = [[168, 169], [-11.5, -9.5]]
Rang2_2 = [[171.5, 172.5], [-11.5, -9.5]]
Rang3_1 = [[167, 168], [-11.5, -9.5]]
Rang3_2 = [[172.5, 173], [-11.5, -9.5]]
Rang4_1 = [[166, 167], [-11.5, -9.5]]
Rang4_2 = [[173, 174], [-11.5, -9.5]]
Rang5_1 = [[164, 166], [-11.5, -9.5]]
Rang5_2 = [[174, 300], [-11.5, -9.5]]

# Define the speed sign place
Speed_sign = [[165, 173.5], [-116, -114]]
CrossedSpeedSign = False

# Define the stop sign place and the boundary flags for performance testing.
Stop_sign = [[165, 173.5], [-441, -439]]
CrossedStopSign = False
Boundary1 = [[165, 173.5], [-446, -444]]
Boundary2 = [[165, 173.5], [-470, -467]]
Boundary3 = [[165, 173.5], [-485, -482]]
Boundary4 = [[165, 173.5], [-500, -497]]

# Define a flag to indicate the subject reached the turn.
crossed_1 = False

#log_path = path.expanduser('~\\Documents\\AirSim\\airsim_rec.txt')
log_path = path.expanduser('rank1_road1_focused.txt')


def analyse():
    CrossedSpeedSign = False
    CrossedStopSign = False
    crossed_1 = False
    # Block execution until the airsim_rec file is created
    while not path.exists(log_path):
        time.sleep(1)
    perf_turn = 5
    perf_speed = 1
    perf_stop = 1
    print("RECORDING STARTED!")
    with open(log_path, 'r') as f:
        # loop on the recorded file line by line and split the line.
        cnt = 1
        for l in f.readlines():
            line = l.split()
            # Check whether the line is empty.
            if(len(line) == 0 or cnt):
                cnt = 0
                continue
                # Data extraction.
            time, x, y, z, Q_W,	Q_X, Q_Y, Q_Z, Throttle, Steering, Brake, Gear, Handbrake, RPM, Speed = line[0], float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(
                line[5]), float(line[6]), float(line[7]), float(line[8]), float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]), float(line[14])

            # ------------------------------- turning performance part-------------------------------------

            # Check whether we crossed the first line then we trigger the flag to track his turning performance.
            if(strip_1[0][0] <= x <= strip_1[0][1] and strip_1[1][0] <= y <= strip_1[1][1]):
                crossed_1 = True
                # Check whether we crossed the second line then we reset the flag and measure his performance of turning.
            if(strip_2[0][0] <= x <= strip_2[0][1] and strip_2[1][0] <= y <= strip_2[1][1]):
                if(crossed_1):
                    if(Rang1_1[0][0] <= x <= Rang1_1[0][1] and Rang1_1[1][0] <= y <= Rang1_1[1][1]):
                        perf_turn = 1
                        crossed_1 = False
                    elif(Rang1_2[0][0] <= x <= Rang1_2[0][1] and Rang1_2[1][0] <= y <= Rang1_2[1][1]):
                        perf_turn = 1
                        crossed_1 = False
                    elif(Rang2_1[0][0] <= x <= Rang2_1[0][1] and Rang2_1[1][0] <= y <= Rang2_1[1][1]):
                        perf_turn = 2
                        crossed_1 = False
                    elif(Rang2_2[0][0] <= x <= Rang2_2[0][1] and Rang2_2[1][0] <= y <= Rang2_2[1][1]):
                        perf_turn = 2
                        crossed_1 = False
                    elif(Rang3_1[0][0] <= x <= Rang3_1[0][1] and Rang3_1[1][0] <= y <= Rang3_1[1][1]):
                        perf_turn = 3
                        crossed_1 = False
                    elif(Rang3_2[0][0] <= x <= Rang3_2[0][1] and Rang3_2[1][0] <= y <= Rang3_2[1][1]):
                        perf_turn = 3
                        crossed_1 = False
                    elif(Rang4_1[0][0] <= x <= Rang4_1[0][1] and Rang4_1[1][0] <= y <= Rang4_1[1][1]):
                        perf_turn = 4
                        crossed_1 = False
                    elif(Rang4_2[0][0] <= x <= Rang4_2[0][1] and Rang4_2[1][0] <= y <= Rang4_2[1][1]):
                        perf_turn = 4
                        crossed_1 = False
                    elif(Rang5_1[0][0] <= x <= Rang5_1[0][1] and Rang5_1[1][0] <= y <= Rang5_1[1][1]):
                        perf_turn = 5
                        crossed_1 = False
                    elif(Rang5_2[0][0] <= x <= Rang5_2[0][1] and Rang5_2[1][0] <= y <= Rang5_2[1][1]):
                        perf_turn = 5
                        crossed_1 = False
                    #print(str(x) + " " +  str(y))
                        # Check whether the subject collided or stopped in the middle of turning.
                    if(Speed <= 3):
                        perf_turn = 5

                        # ------------------------------- Speed limit performance part-------------------------------------

                        # Check the speed limit performance
            if(Speed_sign[0][0] <= x <= Speed_sign[0][1] and Speed_sign[1][0] <= y <= Speed_sign[1][1]):
                CrossedSpeedSign = True
            if(CrossedSpeedSign and Speed > 20 and Speed <= 23):
                perf_speed = 2
                # print(Speed)
            if(CrossedSpeedSign and Speed > 23 and Speed <= 25):
                perf_speed = 3
            if(CrossedSpeedSign and Speed > 25 and Speed <= 30):
                perf_speed = 4
            if(CrossedSpeedSign and Speed > 30):
                perf_speed = 5

                # ------------------------------- stop sign performance part-------------------------------------

                # Check the speed limit performance
            if(CrossedStopSign and Boundary1[0][0] <= x <= Boundary1[0][1] and Boundary1[1][0] <= y <= Boundary1[1][1] and Speed > 5 and perf_stop < 2):
                perf_stop = 2
                # print(Speed)
            if(CrossedStopSign and Boundary2[0][0] <= x <= Boundary2[0][1] and Boundary2[1][0] <= y <= Boundary2[1][1] and Speed > 5 and perf_stop < 3):
                perf_stop = 3
            if(CrossedStopSign and Boundary3[0][0] <= x <= Boundary3[0][1] and Boundary3[1][0] <= y <= Boundary3[1][1] and Speed > 5 and perf_stop < 4):
                perf_stop = 4
            if(CrossedStopSign and Boundary4[0][0] <= x <= Boundary4[0][1] and Boundary4[1][0] <= y <= Boundary4[1][1] and Speed > 5 and perf_stop < 5):
                perf_stop = 5
            if(Stop_sign[0][0] <= x <= Stop_sign[0][1] and Stop_sign[1][0] <= y <= Stop_sign[1][1]):
                CrossedStopSign = True
                print(Speed)
            #print(str(x) + " " +  str(y))
            # print(Speed)
        print((perf_turn))
        print((perf_speed))
        print((perf_stop))
        return (perf_turn+perf_speed+perf_stop)/3


p = analyse()
print((p))
