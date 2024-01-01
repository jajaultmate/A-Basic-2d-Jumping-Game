import pgzrun
import random

#Parameters for the size of the game window
WIDTH = 1280
HEIGHT = 720

#We establish a value for the ground of the game, where the player stands
ground = HEIGHT - 100

#We create the player and the enemy
player = Actor("player_default1transparent", (150, ground)) #Create a character icon called player #You can choose y = ground instead of 500
enemy = Actor("minetransparent", (WIDTH, ground))


#We create variables for gravity, speed, number of points and difficulty of the game
gravity = 1.0
speed = 0
points = 0
difficulty = 5

#Variable for ending the game if player has lost
game_over = False
#Variable to check if the user chooses to duck
player_ducking = False

#Function "draw()" that paints the board. Consists of determining background color, showing the player and enemy as well as show points
def draw():
    global points               #Bring the variable points inside the function to be used
    screen.fill((90, 170, 250)) #Create background color
    player.draw()               #Show the player
    enemy.draw()                #Show the enemy
    screen.draw.text(str(points), (640, 150), fontsize = 80)    #Print out the number of points for the user


#"Main" function that takes care of the game as a whole. It determines if the user has lost or not and therefore runs the game or not
def update():
    global game_over                    #Bring the varaible "game_over" from outside to be used in the function
    if game_over == False:              #If-statement that if false let's the game keep running, otherwise freezes the game
        update_player()
        update_enemy()
        update_difficulty()

    if player.colliderect(enemy) == True:   #If-statement to check if user has collided with enemy, therefore ending the game
        game_over = True
        player.image = "player_default1deadtransparent"

def update_difficulty():
    global difficulty, points

    if points < 5:              #Depending on how many points the user collects, the difficulty gets harder(enemies move faster on x-axis)
        difficulty = 10
    elif points < 10:
        difficulty = 12
    elif points < 20:
        difficulty = 16
    elif points < 30:
        difficulty = 20
    else:
        difficulty = 25

#Function dedicated for the enemy
def update_enemy():
    global difficulty, points
    enemy.x -= difficulty   #Subtract the value of difficulty variable from the x coordinate value of enemy starting point. This makes it move at the speed depending on the difficulty of the game
    enemy.angle += 5        #Rotate the enemy icon for visual effects
    if enemy.x < 0:         #If-statement responsible for "respawning" the enemy when it leaves the screen from right to left
        enemy.x = WIDTH     #Reset the position of enemy icon when it has left the screen
        points += 1         #Add one point as the user has successfully dodged the enemy
        enemy.y = random.choice([ground, ground - 80])

#Function dedicated for the player(user)
def update_player():
    global speed
    if speed > 0:           #If-statements to add a bit of animation depending on what state the player icon is on. Jumping
        player.image = "player_jumpingtransparent"
    elif  speed < 0:        #Falling
        player.image = "player_default2transparent"
    elif player_ducking == True:    #If user's character is ducking then change image of character
        player.image = "player_duckingalttransparent"
    else:                   #Reset to default when back on ground
        player.image = "player_default1transparent"
    player.y += speed      #Increases the rate of the vertical fall of the player icon keeping it on the ground simulating gravity
    speed += gravity       #Increase the speed with constant of gravity, the greater the distance of the fall the faster you fall
    if player.y > ground:  #If-statement that prevents the player from falling off the ground
        speed = 0          #Resets the speed to 0 to prevent further falling


#Function responsible for taking care of the keybinds of the game, specifically when key is pressed(not held down) Or when Held Down, I am confused
def on_key_down(key):
    global speed, player_ducking
    if key == keys.UP and speed == 0 and player_ducking == False:   #If-statement to check if user is pressing the Up arrow key, speed is 0 and player character is not ducking
        speed -= 25         #Make speed negative which leads to the player icon instead launch upwards, instead of the gravity holding him on the ground
    if key == keys.DOWN and speed == 0:     #If player presses down arrow and their character is on the ground(no speed meaning they are not moving on the y-axis) the character ducks
        player_ducking = True
        player.y += 30

def on_key_up(key):
    global player_ducking
    if key == keys.DOWN and player_ducking == True:
        player_ducking = False
        player.y -= 30

pgzrun.go()