# Python snake game
#### Video Demo:  <https://www.youtube.com/watch?v=9slyV9zLMmg>
#### Description:
**Python snake game** - is a classic snake game written in Python using **Tkinter** module. It is a fun game to play while waiting for things. Player can change snake, food or background color as well as can change game speed. Besides, there is an option to use window as game border or not.
**Game folder contains next files**:
- **snake_game.py** - the main file with the game itself.
- **test_snake_game.py** - a file with unit tests.
- **settings.json** - a file to save user settings: snake, food or background color, game speed, use window as game border or not.
##### Game window description:
In the top left side of window there are two buttons:
- **New game** - to run a new game
- **Settings** - to open additional window with user settings.

In the top right side of window there is an information about game score.
Game area is **650x650 px** square where player can move the snake around with the arrow keys, eat the food to grow bigger, and avoid hitting own tail (or window border).
When player hits own tail (or window border) the game is over and a big red "Game over" hint appears.
##### Settings window description:
Settings window is opened when Settings button is pressed. It contains next elements:
- **Snake color** - to choose snake color with the help of color chooser.
- **Food color** - to choose food color with the help of color chooser.
- **Background color** - to choose background color with the help of color chooser.
- **Use window border** - to use window as game border or not with the help of check button.
- **Game speed** - to set game speed (from 1 to 10) with the help of scale.

##### Key assignment:
- **→** - move right
- **←** - move left
- **↑** - move up
- **↓** - move down
- **space** - game pause

##### snake_game.py file description:
This file contains two classes:
- **Snake** - the class that inits the snake. It is a list of rectangles on the canvas.
- **Food** - the class that inits food. While food initings it checks snake location to prevent food appears at snake location. It is a circle on the canvas.

**Functions**:
- **main()** - inits game settings, main window and its elements, snake and food. Runs game key button binding. Starts the game.
- **init_user_settings()** - inits score and default direction (right). Inits user settings (snake, food or background color, game speed, use window as game border or not) from **settings.json** file.
- **save_settings()** - saves user settings.
- **bind_button_pressed()** - binds pressing →, ←, ↑, ↓ and space buttons to  handlers
- **on_sets_window_close()** - handles actions after settings window closed. Run user settings saving and resume game.
- **get_centered_window_params(window)** - calculates and returns parameters for window to be placed in the center of the screen.
- **format_window_geometry(screen_width, window_width, screen_height, window_height)** - returns formatted window parameters for geometry method.
- **open_settings_window()** - opens Settings window after "Setting" button was pressed. The game is paused while Settings window is opened.
- **on_snake_color_changed()** - handles snake color changed event
- **on_food_color_changed()** - handles food color changed event
- **on_bg_color_changed()** - handles background color changed event
- **on_window_border_changed()** - handles using window as game border
- **on_game_speed_changed()** - handles game speed changed event
- **change_pause_state()** - handles game pause
- **next_move()** - calculates the event that will occure after snake next move (checks if direction was changed and calculates new snake head position. If snake catches the food - it groves, if snake collides with own tail (or window border) - game over, otherwise - makes one step ahead).
- **get_new_head_coordinates()** - calculates and returns new snake head coordinates depends on its current position and direction
- **change_direction(new_direction)** - sets new snake direction
- **is_new_direction_allowed(old_direction, new_direction)** - checks if the snake move direction can be changed
- **check_collisions(snake)** - check snake collision with own tail (or window border)
- **game_over()** - ends the game and shows "Game over" hint
- **new_game()** - starts new game