# Helper function to get the speed sign performance with moving left. 
def StopSignLeft(speedPlace, flag, x, y, Speed, prev_perf):
	if(SpeedPlace[0][0] <= x <= SpeedPlace[0][1] and SpeedPlace[1][0] <= y <= SpeedPlace[1][1]):
        flag = True
    if(flag and Speed>20 and Speed<=23 and prev_perf<2):
    	flag = False
        return 2,flag
    if(flag and Speed>23 and Speed<25 and prev_perf<3):
        flag = False
        return 3,flag
    if(flag and Speed>=25 and Speed<=30 and prev_perf<4):
        flag = False
        return 4,flag
    if(flag and Speed>30 and prev_perf<5):
        flag = False
        return 5,flag