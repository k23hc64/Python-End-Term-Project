import turtle
import random
import time
import tkinter as tk

snake = None
fruit = None
old_fruit = []
scoring = None
screen = None
score = 0
delay = 0.1
difficulty = "Medium"
paused = False  
pause_message = None

def start_game():
    root.withdraw()

    show_difficulty_screen()

def show_difficulty_screen():
    difficulty_window = tk.Toplevel()
    difficulty_window.title("Select Difficulty")
    difficulty_window.geometry("400x300")
    difficulty_window.configure(bg="lightblue")  

    label = tk.Label(difficulty_window, text="Select Difficulty Level", font=("Courier", 18, "bold"), bg="lightblue")
    label.pack(pady=20)

    easy_button = tk.Button(difficulty_window, text="Easy", command=lambda: set_difficulty("Easy", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
    easy_button.pack(pady=10)

    medium_button = tk.Button(difficulty_window, text="Medium", command=lambda: set_difficulty("Medium", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
    medium_button.pack(pady=10)

    hard_button = tk.Button(difficulty_window, text="Hard", command=lambda: set_difficulty("Hard", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
    hard_button.pack(pady=10)

def set_difficulty(level, window):
    global difficulty, delay
    difficulty = level
    window.destroy()   

     if difficulty == "Easy":
        delay = 0.15
    elif difficulty == "Medium":
        delay = 0.1
    elif difficulty == "Hard":
        delay = 0.05

     start_game_with_difficulty()

 def start_game_with_difficulty():
    global snake, fruit, old_fruit, scoring, screen, score, delay, paused, pause_message

     global screen
    screen = turtle.Screen()
    screen.title('SNAKE GAME')
    screen.setup(width=700, height=700)
    screen.bgcolor("lightblue")   
    screen.tracer(0)

     create_border()

     score = 0
    snake = turtle.Turtle()
    snake.speed(0)
    snake.shape('square')
    snake.color("black")
    snake.penup()
    snake.goto(0, 0)
    snake.direction = 'stop'

     fruit = turtle.Turtle()
    fruit.speed(0)
    fruit.shape('circle')
    fruit.color('red')
    fruit.penup()
    fruit.goto(30, 30)

     old_fruit = []

     scoring = turtle.Turtle()
    scoring.speed(0)
    scoring.color("black")
    scoring.penup()
    scoring.hideturtle()
    scoring.goto(0, 300)
    scoring.write("Score :", align="center", font=("Courier", 24, "bold"))

     pause_message = turtle.Turtle()
    pause_message.speed(0)
    pause_message.hideturtle()

     screen.listen()
    screen.onkeypress(snake_go_up, "Up")
    screen.onkeypress(snake_go_down, "Down")
    screen.onkeypress(snake_go_left, "Left")
    screen.onkeypress(snake_go_right, "Right")

     screen.onkeypress(toggle_pause, "space")   

     game_loop()

 def create_border():
    turtle.speed(5)
    turtle.pensize(4)
    turtle.penup()
    turtle.goto(-310, 250)
    turtle.pendown()
    turtle.color('black')
    turtle.forward(600)
    turtle.right(90)
    turtle.forward(500)
    turtle.right(90)
    turtle.forward(600)
    turtle.right(90)
    turtle.forward(500)
    turtle.penup()
    turtle.hideturtle()

 def snake_go_up():
    if snake.direction != "down":
        snake.direction = "up"

def snake_go_down():
    if snake.direction != "up":
        snake.direction = "down"

def snake_go_left():
    if snake.direction != "right":
        snake.direction = "left"

def snake_go_right():
    if snake.direction != "left":
        snake.direction = "right"

def snake_move():
    if snake.direction == "up":
        y = snake.ycor()
        snake.sety(y + 20)

    if snake.direction == "down":
        y = snake.ycor()
        snake.sety(y - 20)

    if snake.direction == "left":
        x = snake.xcor()
        snake.setx(x - 20)

    if snake.direction == "right":
        x = snake.xcor()
        snake.setx(x + 20)

 def toggle_pause():
    global paused
    paused = not paused

    if paused:
         pause_message.clear()  
        pause_message.penup()
        pause_message.goto(0, 260)   
        pause_message.color("darkred") 
        pause_message.write("Paused", align="center", font=("Courier", 24, "bold"))  
    else:
         pause_message.clear()

 def game_over(score):
    screen.clear()
    screen.bgcolor('lightblue')   
    scoring.goto(0, 0)
    scoring.write(f"GAME OVER\nYour Score: {score}", align="center", font=("Courier", 30, "bold"))

 def game_loop():
    global score, delay, old_fruit, paused

    while True:
        screen.update()

        if paused:
            time.sleep(0.1)   
            continue

         if snake.distance(fruit) < 20:
            x = random.randint(-290, 270)
            y = random.randint(-240, 240)
            fruit.goto(x, y)
            score += 1
            scoring.clear()
            scoring.write(f"Score: {score}", align="center", font=("Courier", 24, "bold"))
            delay -= 0.001

             new_fruit = turtle.Turtle()
            new_fruit.speed(0)
            new_fruit.shape('square')
            new_fruit.color('red')
            new_fruit.penup()
            old_fruit.append(new_fruit)

         for index in range(len(old_fruit) - 1, 0, -1):
            a = old_fruit[index - 1].xcor()
            b = old_fruit[index - 1].ycor()
            old_fruit[index].goto(a, b)

        if len(old_fruit) > 0:
            a = snake.xcor()
            b = snake.ycor()
            old_fruit[0].goto(a, b)

        snake_move()

         if snake.xcor() > 280 or snake.xcor() < -300 or snake.ycor() > 240 or snake.ycor() < -240:
            game_over(score)
            break

         for segment in old_fruit:
            if segment.distance(snake) < 20:
                game_over(score)
                break

        time.sleep(delay)

root = tk.Tk()
root.title("Snake Game")
root.geometry("400x300")
root.configure(bg="lightblue")   

 start_button = tk.Button(root, text="Start Game", command=start_game, width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
start_button.pack(pady=50)

 exit_button = tk.Button(root, text="Exit", command=root.quit, width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
exit_button.pack(pady=10)

 root.mainloop()
