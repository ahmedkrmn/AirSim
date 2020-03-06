# Define road stripes for first square
strip_1 = [[-22, -20], [-8, 3]]
strip_2 = [[-48, -32], [16, 18]]
strip_3 = [[-52, -51], [-8, 5]]

crossed_1 = False
stupid = False
with open('airsim_rec.txt', 'r') as f:
    sign = 0
    f.readline()
    while(1):
        line = f.readline().split()
        if(len(line) == 0):
            break
        x, y = float(line[1]), float(line[2])
        if(strip_1[0][0] <= x <= strip_1[0][1] and strip_1[1][0] <= y <= strip_1[1][1]):
            crossed_1 = True
            print("STRIP 1")
        if(strip_2[0][0] <= x <= strip_2[0][1] and strip_2[1][0] <= y <= strip_2[1][1]):
            if(crossed_1):
                stupid = True
                print("PLEASE FOLLOW THE RULES!!")
        if(strip_3[0][0] <= x <= strip_3[0][1] and strip_3[1][0] <= y <= strip_3[1][1]):
            crossed_1 = False
            print("STRIP 3")
