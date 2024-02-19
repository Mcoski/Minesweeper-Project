import random as r # Random modules
import time as t # Time modules

class color: # Colour Code
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

win, lose, mine, flag, rounds, history = False, False, [], [], 0, [] # Declare Variables

def show(tmap): # Display Map
    for i in range(0, len(tmap)):
        for j in range(0, len(tmap)):
            print(tmap[i][j], end=" ")
        print("")

def coordinate(tmap): # Set Coordinate To The Map
        for i in range(0, len(tmap)): # 4-sides Border Coordinate
            tmap[i][0] = color.BOLD + color.GREEN + str(i) + color.END # Left Column
            tmap[i][len(tmap)-1] = color.BOLD + color.GREEN + str(i) + color.END # Right Column
            tmap[len(tmap)-1][i] = color.BOLD + color.GREEN  + str(i) + color.END #Bottom Column
            tmap[0][i] = color.BOLD + color.GREEN + str(i) + color.END # Top Column

            tmap[0][0] = color.BOLD + color.GREEN + "/" + color.END # Cross Out Corner
            tmap[len(tmap)-1][0] = color.BOLD + color.GREEN + "/" + color.END
            tmap[len(tmap)-1][len(tmap)-1] = color.BOLD + color.GREEN + "/" + color.END
            tmap[0][len(tmap)-1 ] = color.BOLD + color.GREEN + "/" + color.END

def create_map(w, h): # Create A n*n Default Solution & Answer Map
    global sol_map, ans_map
    sol_map = [[0 for i in range(w+2)]for j in range(h+2)] # Solution, won't show
    ans_map = [["N" for i in range(w+2)]for j in range(h+2)] # Answer, for user
    coordinate(sol_map) # Both Sol & Ans Also Need To Add Coordinates
    coordinate(ans_map)

print(color.PURPLE + "This is the 'Minesweeper Project (v3.0.0)'!" + color.END)
print(color.PURPLE + "You will have 3 modes to choose: Beginner, Intermediate and Expert" + color.END)
mode = int(input(color.PURPLE + "Please enter which mode you want (0: Beginner, 1: Intermediate, 2: Expert): " + color.END)) # Mode Choose

while (mode != 0) and (mode != 1) and (mode != 2): # Re-enter for invalid input
    print(color.RED + "Invalid Input!" + color.END)
    mode = int(input(color.PURPLE + "Please enter which mode you want (0: Beginner, 1: Intermediate, 2: Expert):" + color.END))

if mode == 0: # Beginner Mode

    print("")
    print(color.PURPLE + "You chose Beginner Mode!" + color.END)
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

    show(ans_map) # Show Initial Map
    start_time = t.time() # Starting Time
    while win == False and lose == False: # Start Guessing
        command = input(color.PURPLE + "Please enter your move: " + color.END)# Enter command 
        c = command
        while (c[0] != "m" and c[0] != "f" and c[0] != "r") or (len(command) != 3) or (not(c[1].isdigit() and c[2].isdigit())):
            print(color.RED + "Invalid Command!" + color.END)
            command = input(color.PURPLE + "Please enter your move: " + color.END)
            c = command
        
        if command[0] == "m": # Mine
            x, y = int(command[1]), int(command[2])
            if ans_map[x][y] == color.RED + "F" + color.END: # Mining Flagged Block Error
                print(color.RED + "Invalid for mining flagged blocks!" + color.RED)
            elif x < 1 or y < 1: # Invalid Coordinates
                print(color.RED + "Invalid Coordinate(s)!" + color.END)
                if round == 0 or command[0] not in history:
                    lastx, lasty = 0, 0
            else:
                if rounds == 0 or command[0] not in history: # Bold and blue the current chose
                    ans_map[x][y] = color.BOLD + color.BLUE + str(sol_map[x][y]) + color.END
                else:
                    ans_map[lastx][lasty] = sol_map[lastx][lasty] 
                    ans_map[x][y] = color.BOLD + color.BLUE + str(sol_map[x][y]) + color.END
                lastx, lasty = x, y
                if sol_map[x][y] == "#": # Lose Condition
                    ans_map[x][y] = color.RED + color.BOLD + str(sol_map[x][y]) + color.END
                    lose = True
        
        if command[0] == "f": # Flag
            x, y = int(command[1]), int(command[2])
            if ans_map[x][y] != "N": # Flagging Mined Block Error
                print(color.RED + "Invalid for flagging mined blocks!" + color.END)
            elif x < 1 or y < 1: # Invalid Coordinates
                print(color.RED + "Invalid Coordinate(s)!" + color.END)
            elif ans_map[x][y] == "N":
                ans_map[x][y] = color.RED + "F" + color.END
                flag.append([x, y]) # Add To Flag List for compare
                flag.sort() # Sorting for compare (values same but wrong sequence will be False)
                print(f"{9-len(mine)} mine(s) remain")
                if flag == mine: # Win Condition
                    win = True
        
        if command[0] == "r": # Remove Flag
            x, y = int(command[1]), int(command[2])
            if ans_map[x][y] != color.RED + "F" + color.END: # Removing Mined Block Error
                print(color.RED + "Invalid for removing mined blocks!" + color.END)
            elif x < 1 or y < 1: # Invalid Coordinates
                print(color.RED + "Invalid Coordinate(s)!" + color.END)
            elif ans_map[x][y] == color.RED + "F" + color.END:
                ans_map[x][y] = "N"
                i = flag.index([x, y]) # Find Misplaced Flag Index
                flag.pop(i) # Pop out the Flag
                print(f"{9-len(mine)} mine(s) remain")
        
        show(ans_map) # Show Current Map Status
        rounds += 1 # Add round
        history.append(command[0]) # Add Process 
    
    if win == True: # Win-lose
        end_time = t.time() # Ending Time
        elapsed = round(end_time - start_time) # Seconds Passed
        minutes = round(elapsed/60) # Minutes Passed
        print(color.YELLOW + color.BOLD + "You Win!" + color.END)
        print(color.YELLOW + f"You used {rounds} rounds and {elapsed} seconds/{minutes} minutes finish this game!" + color.END)
    elif lose == True:
        print(color.RED + "You Lose!" + color.END)
