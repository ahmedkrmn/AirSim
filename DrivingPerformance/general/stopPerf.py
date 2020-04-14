# Helper function to get the stop sign performance with moving left. 
def StopSignLeft(stopPlace, flag, x, y, Speed, prev_perf):
	place = stopPlace[1][0]
    Boundary1 = [[stopPlace[0][0], stopPlace[0][1]], [place-13, place-3]]
    Boundary2 = [[stopPlace[0][0], stopPlace[0][1]], [place-36, place-26]]
    Boundary3 = [[stopPlace[0][0], stopPlace[0][1]], [place-51, place-41]]
    Boundary4 = [[stopPlace[0][0], stopPlace[0][1]], [place-66, place-56]]
    if(stopPlace[0][0] <= x <= stopPlace[0][1] and stopPlace[1][0] <= y <= stopPlace[1][1]):
        flag = True
    if(flag and Boundary1[0][0] <= x <= Boundary1[0][1] and Boundary1[1][0] <= y <= Boundary1[1][1] and Speed>5 and prev_perf<2):
        return 2    
    if(flag and Boundary2[0][0] <= x <= Boundary2[0][1] and Boundary2[1][0] <= y <= Boundary2[1][1] and Speed > 5 and prev_perf < 3):
        return 3
    if(flag and Boundary3[0][0] <= x <= Boundary3[0][1] and Boundary3[1][0] <= y <= Boundary3[1][1] and Speed > 5 and prev_perf < 4):
        return 4
    if(flag and Boundary4[0][0] <= x <= Boundary4[0][1] and Boundary4[1][0] <= y <= Boundary4[1][1] and Speed > 5 and prev_perf < 5):
        return 5