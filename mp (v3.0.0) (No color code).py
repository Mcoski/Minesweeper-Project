import random as r # Random modules
import time as t # Time modules

win, lose, mine, flag, rounds, history = False, False, [], [], 0, [] # Declare Variables

def show(tmap): # Display Map
    for i in range(0, len(tmap)):
        for j in range(0, len(tmap)):
            print(tmap[i][j], end=" ")
        print("")

def coordinate(tmap): # Set Coordinate To The Map
        for i in range(0, len(tmap)): # Border Coordinate
            tmap[i][0] = str(i) # Left Column
            tmap[i][len(tmap)-1] = str(i) # Right Column
            tmap[len(tmap)-1][i] = str(i) #Bottom Column
            tmap[0][i] = str(i) # Top Column

            tmap[0][0] = "/" # Cross Out Corner
            tmap[len(tmap)-1][0] = "/"
            tmap[len(tmap)-1][len(tmap)-1] = "/"
            tmap[0][len(tmap)-1 ] = "/"

def create_map(w, h): # Create A n*n Default Solution & Answer Map
    global sol_map, ans_map
    sol_map = [[0 for i in range(w+2)]for j in range(h+2)] # Solution, won't show
    ans_map = [["N" for i in range(w+2)]for j in range(h+2)] # Answer, for user
    coordinate(sol_map)
    coordinate(ans_map)

print("This is the 'Minesweeper Project (v3.0.0)'!")
print("You will have 3 modes to choose: Beginner, Intermediate and Expert")
mode = int(input("Please enter which mode you want (0: Beginner, 1: Intermediate, 2: Expert): "))

while (mode != 0) and (mode != 1) and (mode != 2): # Re-enter for invalid input
    print("Invalid Input!")
    mode = int(input("Please enter which mode you want (0: Beginner, 1: Intermediate, 2: Expert):"))

if mode == 0: # Beginner Mode

    print("")
    print("You chose Beginner Mode!")
    create_map(9, 9)

    while len(mine) < 10: # Mine Generate
        x, y = r.randint(1, 9), r.randint(1, 9)
        if sol_map[x][y] != "#":
            sol_map[x][y] = "#"
            mine.append([x, y])
    mine.sort()

    # Mine Check (Core)
    for x in range(1, len(sol_map)-1):
        for y in range(1, len(sol_map)-1):
            if sol_map[x][y] == 0:
                if sol_map[x-1][y-1] == "#": sol_map[x][y] += 1
                if sol_map[x-1][y] == "#" : sol_map[x][y] += 1
                if sol_map[x-1][y+1] == "#": sol_map[x][y] += 1
                if sol_map[x][y+1] == "#": sol_map[x][y] += 1
                if sol_map[x+1][y+1] == "#": sol_map[x][y] += 1
                if sol_map[x+1][y] == "#": sol_map[x][y] += 1
                if sol_map[x+1][y-1] == "#": sol_map[x][y] += 1
                if sol_map[x][y-1] == "#": sol_map[x][y] += 1

    show(ans_map)
    start_time = t.time()
    while win == False and lose == False:
        command = input("Please enter your move: ")# Enter command 
        c = command
        while (c[0] != "m" and c[0] != "f" and c[0] != "r") or (len(command) != 3) or (not(c[1].isdigit() and c[2].isdigit())):
            print("Invalid Command!")
            command = input("Please enter your move: ")
            c = command
        
        if command[0] == "m": # Mine
            x, y = int(command[1]), int(command[2])
            if ans_map[x][y] == "F":
                print("Invalid for mining flagged blocks!")
            elif x < 1 or y < 1:
                print("Invalid Coordinate(s)!")
                if round == 0 or command[0] not in history:
                    lastx, lasty = 0, 0
            else:
                if rounds == 0 or command[0] not in history: # Bold and blue the current chose
                    ans_map[x][y] = str(sol_map[x][y])
                else:
                    ans_map[lastx][lasty] = sol_map[lastx][lasty]
                    ans_map[x][y] = str(sol_map[x][y])
                lastx, lasty = x, y
                if sol_map[x][y] == "#": # Lose Condition
                    ans_map[x][y] = str(sol_map[x][y])
                    lose = True
        
        if command[0] == "f": # Flag
            x, y = int(command[1]), int(command[2])
            if ans_map[x][y] != "N":
                print("Invalid for flagging mined blocks!")
            elif x < 1 or y < 1:
                print("Invalid Coordinate(s)!")
            elif ans_map[x][y] == "N":
                ans_map[x][y] = "F"
                flag.append([x, y])
                flag.sort()
                print(f"{9-len(mine)} mine(s) remain")
                if flag == mine: # Win Condition
                    win = True
        
        if command[0] == "r": # Remove Flag
            x, y = int(command[1]), int(command[2])
            if ans_map[x][y] != "F":
                print("Invalid for removing mined blocks!")
            elif x < 1 or y < 1:
                print("Invalid Coordinate(s)!")
            elif ans_map[x][y] == "F":
                ans_map[x][y] = "N"
                i = flag.index([x, y])
                flag.pop(i)
                print(f"{9-len(mine)} mine(s) remain")
        
        show(ans_map)
        rounds += 1
        history.append(command[0]) 
    
    if win == True: # Win-lose
        end_time = t.time()
        elapsed = round(end_time - start_time)
        minutes = round(elapsed/60)
        print("You Win!")
        print(f"You used {rounds} rounds and {elapsed} seconds/{minutes} minutes finish this game!")
    elif lose == True:
        print("You Lose!")
    
elif mode == 1:
    create_map(9, 9)
    show(sol_map)