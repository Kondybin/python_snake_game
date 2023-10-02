from tkinter import *
from tkinter import colorchooser
import random
import json

settings = {
    "GAME_WIDTH": 650,
    "GAME_HEIGHT": 650,
    "ELEMENT_SIZE": 50,
    "SNAKE_SIZE": 3,
    "GAME_SPEED_VALUES": {
        1: 500,
        2: 450,
        3: 400,
        4: 350,
        5: 300,
        6: 250,
        7: 200,
        8: 150,
        9: 100,
        10: 50
    },
    "game_speed": None,
    "snake_color": None,
    "food_color": None,
    "background_color": None,
    "is_window_border": None,
    "settings_changed": False,
    "direction": None,
    "pause_pressed": False
}

score = None

window = None
sets_window = None
snake_color_button = None
food_color_button = None
bg_color_button = None
canvas = None
score_label = None
check_var = None

snake = None
food = None
    
class Snake:
    def __init__(self):
        global settings
        self.body_parts = []
        self.coordinates = [[0, 300] for i in range(0, settings["SNAKE_SIZE"])]
        for x, y in self.coordinates:
            body_part = canvas.create_rectangle(x, y, x + settings["ELEMENT_SIZE"], y + settings["ELEMENT_SIZE"], fill=settings["snake_color"], tag = "snake")
            self.body_parts.append(body_part)


class Food:
    def __init__(self, snake_coords):
        global canvas
        global settings
        while True:
            x = random.randint(0, (settings["GAME_WIDTH"]/settings["ELEMENT_SIZE"]) - 1) * settings["ELEMENT_SIZE"]
            y = random.randint(0, (settings["GAME_HEIGHT"]/settings["ELEMENT_SIZE"]) - 1) * settings["ELEMENT_SIZE"]
            if (x, y) not in snake_coords:
                # prevent food appears at snake location
                break
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + settings["ELEMENT_SIZE"], y + settings["ELEMENT_SIZE"], fill = settings["food_color"], tag ="food")


def main():
    global canvas
    global window
    global score
    global score_label
    global snake
    global food
    global settings
    if window:
        window.destroy()
    window = Tk()
    window.title("Python CS50 snake game")
    window.resizable(False, False)
    window.focus_force()
    
    init_user_settings()

    frame = Frame(window)
    frame.pack(fill=BOTH)
    set_frame = Frame(frame, relief=RAISED)
    set_frame.pack(side=LEFT, padx=15)
    Button(set_frame, text="New game", command=new_game, font=('andy', 25)).pack(side=LEFT)
    Button(set_frame, text="Settings", command=open_settings_window, font=('andy', 25)).pack(side=LEFT)
    score_label = Label(frame, text = f"Score:  {score}", font=('andy', 36))
    score_label.pack(side=LEFT)
    canvas = Canvas(window, bg=settings["background_color"], height=settings["GAME_HEIGHT"], width=settings["GAME_WIDTH"])
    canvas.pack()
    window.update()
    window.geometry(get_centered_window_params(window))

    snake = Snake()
    food = Food(snake.coordinates)

    bind_button_pressed()
    next_move() 
    window.mainloop()


def init_user_settings():
    global score
    global window
    global settings
    score = 0
    settings["direction"] = "right"
    with open("settings.json") as f:
        user_settings = json.load(f)
        settings["game_speed"] = user_settings["GAME_SPEED"]
        settings["snake_color"] = user_settings["SNAKE_COLOR"]
        settings["food_color"] = user_settings["FOOD_COLOR"]
        settings["background_color"] = user_settings["BACKGROUND_COLOR"]
        settings["is_window_border"] = IntVar(window, value=user_settings["IS_WINDOW_BORDER"])


def bind_button_pressed():
        global window
        window.bind("<Left>", lambda event: change_direction("left"))
        window.bind("<Right>", lambda event: change_direction("right"))
        window.bind("<Up>", lambda event: change_direction("up"))
        window.bind("<Down>", lambda event: change_direction("down"))
        window.bind("<space>", lambda event: change_pause_state())


def on_sets_window_close():
    global sets_window
    save_settings()
    sets_window.destroy()
    change_pause_state()


def save_settings():
    global settings
    if(settings["settings_changed"]):
        with open("settings.json", "w") as f:
            user_settings = {
                "GAME_SPEED": settings["game_speed"],
                "SNAKE_COLOR": settings["snake_color"],
                "FOOD_COLOR": settings["food_color"],
                "BACKGROUND_COLOR": settings["background_color"],
                "IS_WINDOW_BORDER": settings["is_window_border"].get()
            } 
            f.write(json.dumps(user_settings, indent=4))   


def get_centered_window_params(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    return format_window_geometry(screen_width, window_width, screen_height, window_height)


def format_window_geometry(screen_width, window_width, screen_height, window_height):
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    return f"{window_width}x{window_height}+{x}+{y}"


def open_settings_window():
    global window
    global sets_window
    global snake_color_button
    global food_color_button
    global bg_color_button
    global snake
    global food
    global check_var
    global settings

    sets_window = Toplevel(window, height = 235, width=235)
    sets_window.title("Game settings")
    sets_window.update()
    sets_window.geometry(get_centered_window_params(sets_window))
    sets_window.grab_set()
    sets_window.protocol("WM_DELETE_WINDOW", on_sets_window_close)

    snake_color_label = Label(sets_window, text = f"Snake color", font=('andy', 16))
    snake_color_label.grid(row = 0, column = 0)
    snake_color_button = Button(sets_window, command=on_snake_color_changed, bg = settings["snake_color"], padx=10)
    snake_color_button.grid(row = 0, column = 1)
    food_color_label = Label(sets_window, text = f"Food color", font=('andy', 16))
    food_color_label.grid(row = 1, column = 0)
    food_color_button = Button(sets_window, command=on_food_color_changed, bg = settings["food_color"], padx=10)
    food_color_button.grid(row = 1, column = 1)
    bg_color_label = Label(sets_window, text = f"Background color", font=('andy', 16))
    bg_color_label.grid(row = 2, column = 0)
    bg_color_button = Button(sets_window, command=on_bg_color_changed, bg = settings["background_color"], padx=10)
    bg_color_button.grid(row = 2, column = 1)
    use_window_border = Label(sets_window, text = f"Use window border", font=('andy', 16))
    use_window_border.grid(row = 3, column = 0)
    use_window_border_check = Checkbutton(sets_window, variable=settings["is_window_border"], command=on_window_border_changed)
    use_window_border_check.grid(row = 3, column = 1)
    if(settings["is_window_border"].get() == 1):
        use_window_border_check.select()
    game_speed_label = Label(sets_window, text = f"Game speed", pady=10, font=('andy', 16))
    game_speed_label.grid(row = 4, column = 0, columnspan=2)
    speed_scale = Scale(sets_window, from_ = 1, to = 10, tickinterval=1, orient=HORIZONTAL, length=215, font=('andy', 12), command=on_game_speed_changed)
    speed_scale.grid(row = 5, column = 0, columnspan=2)
    speed_scale.set(settings["game_speed"])

    change_pause_state()


def on_snake_color_changed():
    global snake_color_button
    global canvas
    global snake
    global settings
    color = colorchooser.askcolor()
    if settings["snake_color"] != color[1]:
        settings["snake_color"] = color[1]
        snake_color_button.configure(background = color[1])
        for body_part in snake.body_parts:
            canvas.itemconfig(body_part, fill=color[1])
        settings["settings_changed"] = True


def on_food_color_changed():
    global food_color_button
    global settings
    global canvas
    color = colorchooser.askcolor()
    if settings["food_color"] != color[1]:
        settings["food_color"] = color[1]
        food_color_button.configure(background = color[1])
        canvas.itemconfig("food", fill=color[1])
        settings["settings_changed"] = True


def on_bg_color_changed():
    global bg_color_button
    global settings
    global canvas
    color = colorchooser.askcolor()
    if settings["background_color"] != color[1]:
        settings["background_color"] = color[1]
        bg_color_button.configure(background = color[1])
        canvas.configure(background = color[1])
        settings["settings_changed"] = True


def on_window_border_changed():
    global settings
    settings["settings_changed"] = True


def on_game_speed_changed(value):
    global settings
    settings["settings_changed"] = True
    settings["game_speed"] = int(value)
    window.after(int(settings["GAME_SPEED_VALUES"][settings["game_speed"]]), next_move)


def change_pause_state():
    global window
    global settings
    settings["pause_pressed"] = not settings["pause_pressed"]
    if not settings["pause_pressed"]:
        window.after(int(settings["GAME_SPEED_VALUES"][settings["game_speed"]]), next_move)


def next_move():
    global canvas
    global window
    global snake
    global food
    global settings

    if settings["pause_pressed"]:
        return
    # calculate snake head new coordinates depend on the direction and window boarder
    x_head, y_head = snake.coordinates[0]
    element_size = settings["ELEMENT_SIZE"]
    x_head, y_head = get_new_head_coordinates(x_head, y_head, settings["direction"], settings["GAME_HEIGHT"],
                                              settings["GAME_WIDTH"], settings["is_window_border"].get() == 1,
                                              element_size)
    # add snake head new position
    snake.coordinates.insert(0, (x_head, y_head))
    body_part = canvas.create_rectangle(x_head, y_head, x_head + element_size, y_head + element_size, fill=settings["snake_color"])
    snake.body_parts.insert(0, body_part)

    if x_head == food.coordinates[0] and y_head == food.coordinates[1]:
        # add new snake body part while food is catched
        global score
        global score_label
        score += 1
        score_label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food(snake.coordinates)
    else:
        # remove last snake body part
        del snake.coordinates[-1]
        canvas.delete(snake.body_parts[-1])
        del snake.body_parts[-1]
    
    if check_collisions(snake):
        game_over()
    else:
        window.after(int(settings["GAME_SPEED_VALUES"][settings["game_speed"]]), next_move)
    

def get_new_head_coordinates(x_head, y_head, direction, game_height, game_width, check_window_border, element_size):
    match direction:
        case "down":
            y_head = 0 if not check_window_border and y_head == game_height - element_size else y_head + element_size
        case "up":
            y_head = game_height - element_size if not check_window_border and y_head == 0 else y_head - element_size
        case "right":
            x_head = 0 if not check_window_border and x_head == game_width - element_size else x_head + element_size
        case "left":
            x_head = game_width - element_size if not check_window_border and x_head == 0 else x_head - element_size
    return x_head, y_head
    

def change_direction(new_direction):
    global settings
    direction = settings["direction"]
    if is_new_direction_allowed(direction, new_direction):
        settings["direction"] = new_direction


def is_new_direction_allowed(old_direction, new_direction):
    return (new_direction == "up" and old_direction != "down") \
            or (new_direction == "down" and old_direction != "up") \
            or (new_direction == "left" and old_direction != "right") \
            or (new_direction == "right" and old_direction != "left")


def check_collisions(snake):
    global settings
    x_head, y_head = snake.coordinates[0]
    if settings["is_window_border"].get() == 1:
        if x_head < 0 or x_head >= settings["GAME_WIDTH"]:
            return True
        elif y_head < 0 or y_head >= settings["GAME_HEIGHT"]:
            return True

    for body_part in snake.coordinates[1:]:
        if x_head == body_part[0] and y_head == body_part[1]:
            return True
    
    return False


def game_over():
    global canvas
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=("andy", 68), text = "Game over!", fill="red")


def new_game():
    main()


if __name__ == "__main__":
    new_game()