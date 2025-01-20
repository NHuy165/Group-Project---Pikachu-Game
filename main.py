import random, collections, time, sys, copy, json
import pygame as pg
from BFS import bfs

pg.init()
pg.font.init()
pg.mixer.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
Time = pg.time.Clock()

# Creates game window with the specified sizes:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background images loading:
LIST_BACKGROUND = [pg.transform.scale(pg.image.load("assets/images/background/" + str(i) + ".jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)) for i in range(10)]

# Board variables:
board_row = None
board_column = None
num_tile_on_board = None
num_same_tile = None
margin_x = None
margin_y = None

TILE_WIDTH = 50
TILE_HEIGHT = 55                                                                                           

NUM_TILE = 33
LIST_TILE = [0] * (NUM_TILE + 1)
for i in range(1, NUM_TILE + 1): 
    LIST_TILE[i] = pg.transform.scale(pg.image.load("assets/images/tiles/section" + str(i) + ".png"), (TILE_WIDTH, TILE_HEIGHT))

# Time bar:
TIME_BAR_WIDTH = 500
TIME_BAR_HEIGHT = 30
TIME_BAR_POS = ((SCREEN_WIDTH - TIME_BAR_WIDTH) // 2, 35)
TIME_ICON = pg.transform.scale(pg.image.load("assets/images/tiles/section1.png"), (TILE_WIDTH, TILE_HEIGHT))

# Game level and time:
MAX_LEVEL = 5
GAME_TIME = 120
TIME_END = 6 # Game over screen time

# Font loading:
FONT_COMICSANSMS = pg.font.SysFont('dejavusans', 40)
FONT_TUROK = pg.font.SysFont('timesnewroman', 60)
FONT_PIKACHU = pg.font.Font("assets/font/pikachu.otf", 50)
FONT_ARIAL = pg.font.Font('assets/font/Folty-Bold.ttf', 25)

# Backgrounds:
START_SCREEN_BACKGOUND = pg.transform.scale(pg.image.load("assets/images/background/b1g.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
GAMEOVER_BACKGROUND = pg.transform.scale(pg.image.load("assets/images/button/gameover.png").convert_alpha(), (1000, 600))
WIN_BACKGROUND = pg.transform.scale(pg.image.load("assets/images/button/win1.png").convert_alpha(), (1000, 562))
PAUSE_PANEL_IMAGE = pg.transform.scale(pg.image.load("assets/images/button/panel_pause.png"), (800, 600))

# Menu UI:
LOGO_IMAGE = pg.transform.scale(pg.image.load("assets/images/logo/logo_home.png"), (600, 200))
NEW_GAME_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/new_game.png"), (180, 72)).convert_alpha()
CONTINUE_BUTTON_START = pg.transform.scale(pg.image.load("assets/images/button/continue_start.png"), (180, 72)).convert_alpha()
SIGN_IN_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/sign_in.png"), (180, 72)).convert_alpha()
REGISTER_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/register.png"), (180, 72)).convert_alpha()
PROCEED_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/proceed.png").convert_alpha(), (180, 72))
WARNING_GUEST_PANEL = pg.transform.scale(pg.image.load("assets/images/button/warning_guest_panel.png"), (700, 469)).convert_alpha()
WARNING_SAVELESS_PANEL = pg.transform.scale(pg.image.load("assets/images/button/warning_saveless_panel.png"), (700, 469)).convert_alpha()
SIGN_IN_PANEL = pg.transform.scale(pg.image.load("assets/images/button/sign_in_panel.png"), (700, 469)).convert_alpha()
SIGN_IN_PANEL = pg.transform.scale(pg.image.load("assets/images/button/sign_in_panel.png"), (956, 500)).convert_alpha()
REGISTER_PANEL = pg.transform.scale(pg.image.load("assets/images/button/register_panel.png"), (956, 500)).convert_alpha()
SIZE_SMALL_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/size_small.png"), (373, 72)).convert_alpha()
SIZE_MEDIUM_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/size_medium.png"), (373, 72)).convert_alpha()
SIZE_LARGE_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/size_large.png"), (373, 72)).convert_alpha()
SELECT_SIZE_PANEL = pg.transform.scale(pg.image.load("assets/images/button/select_size_panel.png"), (700, 469)).convert_alpha()
INSTRUCTION_PANEL = pg.transform.scale(pg.image.load("assets/images/button/instruction.png"), (760, 469)).convert_alpha()
SOUND_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/sound.png"), (50, 50))
MUSIC_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/music.png"), (50, 50))
INFO_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/info.png"), (50, 50))

# Game UI:
EXIT_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/close.png"), (60, 60))
REPLAY_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/replay.png"), (50, 50))
HOME_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/exit.png").convert_alpha(), (50, 50))
PAUSE_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/pause.png").convert_alpha(), (50, 50))
HINT_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/hint.png").convert_alpha(), (50, 50))
CONTINUE_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/continue.png").convert_alpha(), (50, 50))
RESET_BUTTON = pg.transform.scale(pg.image.load("assets/images/button/replay.png"), (50, 50))
LIST_LEVEL = [pg.transform.scale(pg.image.load("assets/images/level/" + str(i) + ".png"), (50, 50)) for i in range(1, 10)]
LIVES_IMAGE = pg.transform.scale(pg.image.load("assets/images/heart.png"), (50, 50))

# Background music:
pg.mixer.music.load("assets/music/background1.mp3")
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1, 0.0, 5000)
music_on = True


# Sounds:
click_sound = pg.mixer.Sound("assets/sound/click_sound.mp3")
click_sound.set_volume(0.2)
success_sound = pg.mixer.Sound("assets/sound/success.mp3")
success_sound.set_volume(0.2)
fail_sound = pg.mixer.Sound("assets/sound/fail.mp3")
fail_sound.set_volume(0.2)
win_sound = pg.mixer.Sound("assets/sound/win.mp3")
win_sound.set_volume(0.2)
game_over_sound = pg.mixer.Sound("assets/sound/gameover.wav")
game_over_sound.set_volume(0.2)
sound_on = True

# Working with sign-in and register systems:
current_player = "[Guest]"
user_background = pg.image.load("assets/images/button/user_background.png")
NAME_LIMIT = 20
PASSWORD_LIMIT = 20
NAME_HITBOX_SIGN_IN = pg.Rect(570, 286, 345, 41)
PASSWORD_HITBOX_SIGN_IN = pg.Rect(570, 383, 345, 41)
NAME_HITBOX_REGISTER = pg.Rect(570, 295, 345, 42)
PASSWORD_HITBOX_REGISTER = pg.Rect(570, 395, 345, 42)


# Working with hints:
current_hint = None  # Will store the current hint tiles
show_hint = False   # Flag to control hint visibility

# Initialize game info:
board = None
lives = 3
level = 1
remaining_time = GAME_TIME
curr_remaining_time = GAME_TIME

# Resets game info:
def reset_game_info():
	global board, lives, level, remaining_time, curr_remaining_time, bonus_time, show_hint
	board = None
	lives = 3
	level = 1
	remaining_time = GAME_TIME
	curr_remaining_time = GAME_TIME
	bonus_time = 0
	show_hint = False

# Gets top-left corner coordinates of a tile based on its row (i) and column (j):
def get_left_top_coords(i, j): 
	x = j * TILE_WIDTH + margin_x
	y = i * TILE_HEIGHT + margin_y
	return x, y

# Gets center coordinates of a tile based on its row (i) and column (j):
def get_center_coords(i, j): 
	x, y = get_left_top_coords(i, j)
	return x + TILE_WIDTH // 2, y + TILE_HEIGHT // 2

# Calculates row and column of tile clicked based on position of mouse click:
def get_index_at_mouse(x, y): 
	if x < margin_x or y < margin_y: return None, None
	return (y - margin_y) // TILE_HEIGHT, (x - margin_x) // TILE_WIDTH

# Generates a random shuffled game board:
def get_random_board():
	list_index_tiles = list(range(1, NUM_TILE + 1)) 
	random.shuffle(list_index_tiles)
	list_index_tiles = list_index_tiles[:num_tile_on_board] * num_same_tile 
	random.shuffle(list_index_tiles)
	board = [[0 for _ in range(board_column)] for _ in range(board_row)]
	k = 0
	for i in range(1, board_row - 1):
		for j in range(1, board_column - 1):
			board[i][j] = list_index_tiles[k]
			k += 1
	return board

# Draws game board:
def draw_board(board):
	for i in range(1, board_row - 1):
		for j in range(1, board_column - 1):
			if board[i][j] != 0:
				screen.blit(LIST_TILE[board[i][j]], get_left_top_coords(i, j))

# Draws a darkened version of an image:
def draw_dark_image(image, image_rect, color):
	dark_image = image.copy()
	dark_image.fill(color, special_flags = pg.BLEND_RGB_SUB)
	screen.blit(dark_image, image_rect)

# Darkens and draws tiles that have been clicked:
def draw_clicked_tiles(board, clicked_tiles):
	for i, j in clicked_tiles:
		x, y = get_left_top_coords(i, j)
		try:
			darkImage = LIST_TILE[board[i][j]].copy()
			darkImage.fill((60, 60, 60), special_flags = pg.BLEND_RGB_SUB)
			screen.blit(darkImage, (x, y))
		except: pass

# Draws blue border around a specified tile:
def draw_border_tile(board, i, j):
	x, y = get_left_top_coords(i, j)
	pg.draw.rect(screen, (0, 0, 255),(x - 1, y - 3, TILE_WIDTH + 4, TILE_HEIGHT + 4), 2)

# Draws a red line connecting tiles:
def draw_path(path):
	for i in range(len(path) - 1):
		start_pos = (get_center_coords(path[i][0], path[i][1]))
		end_pos = (get_center_coords(path[i + 1][0], path[i + 1][1]))
		pg.draw.line(screen, 'red', start_pos, end_pos, 4)
		pg.display.update()
	pg.time.wait(400)

# Draws a green border around specific tiles as hints:
def draw_hint(hint):
	for i, j in hint:
		x, y = get_left_top_coords(i, j)
		pg.draw.rect(screen, (0, 255, 0),(x - +1, y - 2, TILE_WIDTH + 4, TILE_HEIGHT + 4), 2)
 
# Draws current number of lives and level:
def draw_lives(lives, level):
	screen.blit(LIVES_IMAGE, (10, 12))
	lives_count = FONT_PIKACHU.render(str(lives), True, 'white')
	screen.blit(lives_count, (60, 13))

	screen.blit(LIST_LEVEL[level - 1], (SCREEN_WIDTH - 70, 12))
 
 # Draws a time bar:
def draw_time_bar(start_time):
	global time_start_paused, time_paused, curr_remaining_time, bonus_time
	pg.draw.rect(screen, (255,255,255,5), (TIME_BAR_POS[0], TIME_BAR_POS[1], TIME_BAR_WIDTH, TIME_BAR_HEIGHT), 2, border_radius = 20)
	current_time = time.time()
	 # ratio between remaining time and total time
	if show_paused:
		if not time_start_paused: 
			time_start_paused = time.time()

	else:
		if time_start_paused:
			time_paused += current_time - time_start_paused
		time_start_paused = 0

		curr_remaining_time = GAME_TIME - (current_time - start_time - time_paused) + bonus_time
		if curr_remaining_time > GAME_TIME:
			bonus_time -= curr_remaining_time - GAME_TIME
			curr_remaining_time = GAME_TIME
      
  
	real_remaining_time = curr_remaining_time - (GAME_TIME - remaining_time)
	timeOut = real_remaining_time / GAME_TIME
	time_text = FONT_ARIAL.render(f"{str(int(real_remaining_time // 60)).zfill(2)}:{str(int(real_remaining_time % 60)).zfill(2)}", True, (255, 255, 255))
	time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 18))
	screen.blit(time_text, time_rect)

	# Calculate inner bar width
	inner_width = max(3, TIME_BAR_WIDTH * timeOut - 4)  # Minimum width of 40 pixels
    
    # If time is actually up, set width to 0
	if timeOut <= 0:
		inner_width = 0
    
	innerPos = (TIME_BAR_POS[0] + 2, TIME_BAR_POS[1] + 2)
	innerSize = (inner_width, TIME_BAR_HEIGHT - 4)
    
    # Only draw with border radius if bar is wide enough
	if inner_width >= 3:
		pg.draw.rect(screen, 'green', (innerPos, innerSize), border_radius=20)
	elif inner_width > 0:  # For very small widths, draw without border radius
		pg.draw.rect(screen, 'green', (innerPos, innerSize))

# Draws pause button:
def draw_pause_button(mouse_x, mouse_y, mouse_clicked):
	global show_paused
	pause_rect = pg.Rect(0, 0, *PAUSE_BUTTON.get_size())
	pause_rect.center = (SCREEN_WIDTH - 220, 35)
	screen.blit(PAUSE_BUTTON, pause_rect)
	if pause_rect.collidepoint(mouse_x, mouse_y):
		if not show_paused: 
			draw_dark_image(PAUSE_BUTTON, pause_rect, (60, 60, 60))
			if mouse_clicked:
				mouse_clicked = False
				show_paused = True
				click_sound.play()
	return mouse_clicked

# Draws hint button: 
def draw_hint_button(mouse_x, mouse_y, mouse_clicked, board):
    global current_hint, show_hint
    hint_rect = pg.Rect(0, 0, *HINT_BUTTON.get_size())
    hint_rect.center = (35, SCREEN_HEIGHT - 400)
    screen.blit(HINT_BUTTON, hint_rect)
    if hint_rect.collidepoint(mouse_x, mouse_y):
        draw_dark_image(HINT_BUTTON, hint_rect, (60, 60, 60))
        if mouse_clicked:
            mouse_clicked = False
            current_hint = get_hint(board)
            if not current_hint:
                reset_board(board)
				# Add reshuffle message
                reshuffle_text = FONT_ARIAL.render("No valid moves found. Reshuffling board...", True, (255, 255, 255))
                text_rect = reshuffle_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
                screen.blit(reshuffle_text, text_rect)
                pg.display.flip()
                pg.time.wait(3000)  # Show message for 1 second

            show_hint = True
            click_sound.play()
    return mouse_clicked

# Draws New Game button:
def draw_new_game_button(mouse_x, mouse_y, mouse_clicked):
	global show_select_size, show_warning_guest

	new_game_rect = NEW_GAME_BUTTON.get_rect(center=(SCREEN_WIDTH // 2, 410))
	screen.blit(NEW_GAME_BUTTON, new_game_rect)
	if new_game_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(NEW_GAME_BUTTON, new_game_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			if current_player == "[Guest]":
				show_warning_guest = True
			else:
				show_select_size = True
			click_sound.play()
	return mouse_clicked

# Draws Continue button:
def draw_continue_button(mouse_x, mouse_y, mouse_clicked, players):
	global show_warning_saveless
	global board, level, lives, remaining_time
	global board_row, board_column, num_tile_on_board, num_same_tile
	global margin_x, margin_y

	continue_rect = CONTINUE_BUTTON_START.get_rect(center=(SCREEN_WIDTH // 2, 485))
	if current_player == "[Guest]":
		draw_dark_image(CONTINUE_BUTTON_START, continue_rect, (120, 120, 120))
	else:
		screen.blit(CONTINUE_BUTTON_START, continue_rect)

	if continue_rect.collidepoint(mouse_x, mouse_y) and current_player != "[Guest]": 
		draw_dark_image(CONTINUE_BUTTON_START, continue_rect, (60, 60, 60))
		if mouse_clicked:
			click_sound.play()
			mouse_clicked = False
			if players[current_player]["save"][0] is None: # If no board saved
				show_warning_saveless = True
				
			else:
				board = players[current_player]["save"][0]
				level = players[current_player]["save"][1]
				lives = players[current_player]["save"][2]
				remaining_time = players[current_player]["save"][3]

				board_row = len(board)
				board_column = len(board[0])
				num_tile_on_board = 21 if board_row != 7 else 25
				num_same_tile = ((board_row - 2) * (board_column - 2)) // num_tile_on_board

				margin_x = (SCREEN_WIDTH - TILE_WIDTH * board_column) // 2
				margin_y = (SCREEN_HEIGHT - TILE_HEIGHT * board_row) // 2 + 15
				return mouse_clicked, True
	return mouse_clicked, False

# Draws Sign in button:
def draw_sign_in_button(mouse_x, mouse_y, mouse_clicked):
	global show_sign_in

	sign_in_rect = SIGN_IN_BUTTON.get_rect(center=(SCREEN_WIDTH // 2,  560))
	screen.blit(SIGN_IN_BUTTON, sign_in_rect)
	if sign_in_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(SIGN_IN_BUTTON, sign_in_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_sign_in = True
			click_sound.play()
	return mouse_clicked

# Draws Register button:
def draw_register_button(mouse_x, mouse_y, mouse_clicked):
	global show_register

	register_rect = REGISTER_BUTTON.get_rect(center=(SCREEN_WIDTH // 2,  635))
	screen.blit(REGISTER_BUTTON, register_rect)
	if register_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(REGISTER_BUTTON, register_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_register = True
			click_sound.play()
	return mouse_clicked

# Draws sound button:
def draw_sound_button(mouse_x, mouse_y, mouse_clicked):
	global sound_on

	sound_rect = SOUND_BUTTON.get_rect(center=(65, SCREEN_HEIGHT - 65))
	if sound_on:
		screen.blit(SOUND_BUTTON, sound_rect)
	else: 
		draw_dark_image(SOUND_BUTTON, sound_rect, (120, 120, 120))
	
	if sound_rect.collidepoint(mouse_x, mouse_y):
		if sound_on:
			draw_dark_image(SOUND_BUTTON, sound_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			if sound_on:
				sound_on = False
				success_sound.set_volume(0)
				fail_sound.set_volume(0)
				click_sound.set_volume(0)

			else:
				sound_on = True
				success_sound.set_volume(0.2)
				fail_sound.set_volume(0.2)
				click_sound.set_volume(0.2)
			click_sound.play()
	return mouse_clicked

# Draws sound button:
def draw_music_button(mouse_x, mouse_y, mouse_clicked):
	global music_on

	music_rect = MUSIC_BUTTON.get_rect(center=(130, SCREEN_HEIGHT - 65))
	if music_on:
		screen.blit(MUSIC_BUTTON, music_rect)
	else: 
		draw_dark_image(MUSIC_BUTTON, music_rect, (120, 120, 120))
	
	if music_rect.collidepoint(mouse_x, mouse_y):
		if music_on:
			draw_dark_image(MUSIC_BUTTON, music_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			if music_on:
				music_on = False
				pg.mixer.music.set_volume(0)

			else:
				music_on = True
				pg.mixer.music.set_volume(0.1)
	
			click_sound.play()
	return mouse_clicked

# Draws info button:
def draw_info_button(mouse_x, mouse_y, mouse_clicked):
	global show_instruction

	info_rect = INFO_BUTTON.get_rect(center=(SCREEN_WIDTH - 65, SCREEN_HEIGHT - 65))
	screen.blit(INFO_BUTTON, info_rect)
	if info_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(INFO_BUTTON, info_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_instruction = True
			click_sound.play()
	return mouse_clicked

# Provides a hint by finding two matching tiles that can be connected:
def get_hint(board):
	hint = [] # stores two tuple
	tiles_location = collections.defaultdict(list)
	for i in range(board_row):
		for j in range(board_column):
			if board[i][j]:
				tiles_location[board[i][j]].append((i, j))
	for value, positions in tiles_location.items():	
		n = len(positions)
		for idx1 in range(n):
			for idx2 in range(idx1 + 1, n):
				pos1, pos2 = positions[idx1], positions[idx2]
				
				# Check connectivity using BFS
				if bfs(board, pos1[0], pos1[1], pos2[0], pos2[1]):
					hint.append(pos1)
					hint.append(pos2)
					return hint
	return []

# Checks if current level is complete:
def is_level_complete(board):
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] != 0: return False
	return True

# Modifies the board based on difficulty level:
def update_difficulty(board, level, tile1_i, tile1_j, tile2_i, tile2_j):
	if level == 2: #all card move up
		for j in (tile1_j, tile2_j):
			new_column = [0]
			for i in range(board_row):
				if board[i][j] != 0:
					new_column.append(board[i][j])
			while(len(new_column) < board_row): new_column.append(0)
			for k in range(board_row):
				board[k][j] = new_column[k]
	if level == 3: #all card move down
		for j in (tile1_j, tile2_j):
			new_column = []
			for i in range(board_row):
				if board[i][j] != 0:
					new_column.append(board[i][j])
			while(len(new_column) < board_row - 1): new_column = [0] + new_column
			new_column.append(0)
			for k in range(board_row):
				board[k][j] = new_column[k]
	if level == 4: #all card move left
		for i in (tile1_i, tile2_i):
			new_row = [0]
			for j in range(board_column):
				if board[i][j] != 0:
					new_row.append(board[i][j])
			while(len(new_row) < board_column): new_row.append(0)
			for k in range(board_column):
				board[i][k] = new_row[k]
	if level == 5: #all card move right
		for i in (tile1_i, tile2_i):
			new_row = []
			for j in range(board_column):
				if board[i][j] != 0:
					new_row.append(board[i][j])
			while len(new_row) < board_column - 1: new_row = [0] + new_row
			new_row.append(0)
			for k in range(board_column):
				board[i][k] = new_row[k]

# Randomly shuffles the board while keeping the same tiles:
def reset_board(board):
	current_tiles = []
	for i in range(board_row):
		for j in range(board_column):
			if board[i][j]: current_tiles.append(board[i][j])
	tmp = current_tiles[:]
	while tmp == current_tiles:
		random.shuffle(current_tiles)
	k = 0
	for i in range(board_row):
		for j in range(board_column):
			if board[i][j]:
				board[i][j] = current_tiles[k]
				k += 1
	return board

# Checks if the player has run out of time:
def check_time():
	global lives, remaining_time, curr_remaining_time
	if show_paused: 
		return 2	
	# check game lost
	if curr_remaining_time - (GAME_TIME - remaining_time) < 0: # time up
		curr_remaining_time = remaining_time = GAME_TIME
		if lives <= 0: 
			return 0
		return 1
	return 2

# Creates a dimmed overlay effect on the screen:
def show_dim_screen():
	dim_screen = pg.Surface(screen.get_size(), pg.SRCALPHA)
	pg.draw.rect(dim_screen, (0, 0, 0, 220), dim_screen.get_rect())
	screen.blit(dim_screen, (0, 0))

# Displays the instruction panel:
def draw_panel_instruction(mouse_x, mouse_y, mouse_clicked):
	show_dim_screen()
	instruct_rect = INSTRUCTION_PANEL.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
	screen.blit(INSTRUCTION_PANEL, instruct_rect)

	exit_rect = EXIT_BUTTON.get_rect(topright=(instruct_rect.right - 10, instruct_rect.top + 30))
	screen.blit(EXIT_BUTTON, exit_rect)

	show_instruction = True

	if exit_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(EXIT_BUTTON, exit_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_instruction = False
			click_sound.play()
	return mouse_clicked, show_instruction

# Displays the saveless warning panel:
def draw_panel_warning_saveless(mouse_x, mouse_y, mouse_clicked):
	show_dim_screen()
	warning_saveless_rect = WARNING_SAVELESS_PANEL.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
	screen.blit(WARNING_SAVELESS_PANEL, warning_saveless_rect)
	proceed_rect = PROCEED_BUTTON.get_rect(center=(warning_saveless_rect.centerx, warning_saveless_rect.bottom - 50))
	screen.blit(PROCEED_BUTTON, proceed_rect)

	exit_rect = EXIT_BUTTON.get_rect(topright=(warning_saveless_rect.right - 10, warning_saveless_rect.top + 30))
	screen.blit(EXIT_BUTTON, exit_rect)

	show_warning_saveless = True
	show_select_size = False
	
	if proceed_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(PROCEED_BUTTON, proceed_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_select_size = True
			show_warning_saveless = False
			click_sound.play()
	elif exit_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(EXIT_BUTTON, exit_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_warning_saveless = False
			click_sound.play()

	return mouse_clicked, show_warning_saveless, show_select_size

def draw_panel_warning_guest(mouse_x, mouse_y, mouse_clicked): 
	show_dim_screen()
	warning_guest_rect = WARNING_GUEST_PANEL.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
	screen.blit(WARNING_GUEST_PANEL, warning_guest_rect)
	proceed_rect = PROCEED_BUTTON.get_rect(center=(warning_guest_rect.centerx, warning_guest_rect.bottom - 50))
	screen.blit(PROCEED_BUTTON, proceed_rect)

	exit_rect = EXIT_BUTTON.get_rect(topright=(warning_guest_rect.right - 10, warning_guest_rect.top + 30))
	screen.blit(EXIT_BUTTON, exit_rect)

	show_warning_guest = True
	show_select_size = False
	
	if proceed_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(PROCEED_BUTTON, proceed_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_select_size = True
			show_warning_guest = False
			click_sound.play()
	elif exit_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(EXIT_BUTTON, exit_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_warning_guest = False
			click_sound.play()

	return mouse_clicked, show_warning_guest, show_select_size

def draw_panel_sign_in(mouse_x, mouse_y, mouse_clicked, input_active, name_input, password_input, error):
	show_dim_screen()
	panel_rect = SIGN_IN_PANEL.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
	screen.blit(SIGN_IN_PANEL, panel_rect)

	exit_rect = EXIT_BUTTON.get_rect(topright=(panel_rect.right - 10, panel_rect.top + 30))
	screen.blit(EXIT_BUTTON, exit_rect)

	show_sign_in = True

	if exit_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(EXIT_BUTTON, exit_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_sign_in = False
			error = ""  
			name_input = ""  
			password_input = ""
			click_sound.play()

	elif NAME_HITBOX_SIGN_IN.collidepoint(mouse_x, mouse_y) and mouse_clicked:
		mouse_clicked = False
		input_active = "name"

	elif PASSWORD_HITBOX_SIGN_IN.collidepoint(mouse_x, mouse_y) and mouse_clicked:
		mouse_clicked = False
		input_active = "password"
		

	# Draw input fields and text
	name_text = FONT_ARIAL.render(name_input, True, (0, 0, 0))  # Changed to black
	password_text = FONT_ARIAL.render("*" * len(password_input), True, (0, 0, 0))  # Changed to black

	name_rect = name_text.get_rect(center=(panel_rect.centerx + 102, panel_rect.centery - 54))
	# pg.draw.rect(screen, (0, 0, 0), NAME_HITBOX_SIGN_IN, 1)
	password_rect = password_text.get_rect(center=(panel_rect.centerx + 102, panel_rect.centery + 43))
	# pg.draw.rect(screen, (0, 0, 0), PASSWORD_HITBOX_SIGN_IN, 1)
	
	screen.blit(name_text, name_rect)
	screen.blit(password_text, password_rect)

	# Draw active input indicator
	if input_active == "name":
		pg.draw.line(screen, (0, 0, 0),  
					(name_rect.right + 5, name_rect.top + 1), 
					(name_rect.right + 5, name_rect.bottom - 2), 2)
	else:
		pg.draw.line(screen, (0, 0, 0), 
					(password_rect.right + 5, password_rect.top + 1), 
					(password_rect.right + 5, password_rect.bottom - 2), 2)

	# Draw error message if any
	if error:
		error_text = FONT_ARIAL.render(error, True, (255, 0, 0)) 
		error_rect = error_text.get_rect(center=(panel_rect.centerx, panel_rect.centery + 150))
		screen.blit(error_text, error_rect)

	return mouse_clicked, input_active, name_input, password_input, show_sign_in

def draw_panel_register(mouse_x, mouse_y, mouse_clicked, input_active, name_input, password_input, error):
	show_dim_screen()
	panel_rect = REGISTER_PANEL.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
	screen.blit(REGISTER_PANEL, panel_rect)

	exit_rect = EXIT_BUTTON.get_rect(topright=(panel_rect.right - 10, panel_rect.top + 30))
	screen.blit(EXIT_BUTTON, exit_rect)

	show_register = True

	if exit_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(EXIT_BUTTON, exit_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_register = False
			error = "" 
			name_input = ""  
			password_input = ""
			click_sound.play()

	if NAME_HITBOX_REGISTER.collidepoint(mouse_x, mouse_y) and mouse_clicked:
		mouse_clicked = False
		input_active = "name"

	if PASSWORD_HITBOX_REGISTER.collidepoint(mouse_x, mouse_y) and mouse_clicked:
		mouse_clicked = False
		input_active = "password"

	# Draw input fields and text
	name_text = FONT_ARIAL.render(name_input, True, (0, 0, 0))  # Changed to black
	password_text = FONT_ARIAL.render("*" * len(password_input), True, (0, 0, 0))  # Changed to black

	name_rect = name_text.get_rect(center=(panel_rect.centerx + 102, panel_rect.centery - 64))
	# pg.draw.rect(screen, (0, 0, 0), NAME_HITBOX_REGISTER, 1)
	password_rect = password_text.get_rect(center=(panel_rect.centerx + 102, panel_rect.centery + 36))
	# pg.draw.rect(screen, (0, 0, 0), PASSWORD_HITBOX_REGISTER, 1)

	screen.blit(name_text, name_rect)
	screen.blit(password_text, password_rect)

	# Draw active input indicator
	if input_active == "name":
		pg.draw.line(screen, (0, 0, 0),  
					(name_rect.right + 5, name_rect.top + 0), 
					(name_rect.right + 5, name_rect.bottom - 2), 2)
	else:
		pg.draw.line(screen, (0, 0, 0), 
					(password_rect.right + 5, password_rect.top + 1), 
					(password_rect.right + 5, password_rect.bottom - 2), 2)

	# Draw error message if any
	if error:
		error_text = FONT_ARIAL.render(error, True, (255, 0, 0)) 
		error_rect = error_text.get_rect(center=(panel_rect.centerx, panel_rect.centery + 105))
		screen.blit(error_text, error_rect)

	return mouse_clicked, input_active, name_input, password_input, show_register

def draw_panel_select_size(mouse_x, mouse_y, mouse_clicked):
	global board_row, board_column, num_tile_on_board, num_same_tile, margin_x, margin_y, board, GAME_TIME, remaining_time, curr_remaining_time

	# Board configuration:
	# Small: 5 x 10
	# Medium: 7 x 12
	# Large: 9 x 14
	# True row and column are board_row - 2 and board_column - 2

	show_dim_screen()
	select_size_rect = SELECT_SIZE_PANEL.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
	screen.blit(SELECT_SIZE_PANEL, select_size_rect)

	small_rect = SIZE_SMALL_BUTTON.get_rect(center=(select_size_rect.centerx, select_size_rect.top + 150))
	screen.blit(SIZE_SMALL_BUTTON, small_rect)
	medium_rect = SIZE_MEDIUM_BUTTON.get_rect(center=(select_size_rect.centerx, select_size_rect.centery))
	screen.blit(SIZE_MEDIUM_BUTTON, medium_rect)
	large_rect = SIZE_LARGE_BUTTON.get_rect(center=(select_size_rect.centerx, select_size_rect.bottom - 150))
	screen.blit(SIZE_LARGE_BUTTON, large_rect)

	exit_rect = EXIT_BUTTON.get_rect(topright=(select_size_rect.right - 10, select_size_rect.top + 30))
	screen.blit(EXIT_BUTTON, exit_rect)

	show_select_size = True

	start_game = False

	if small_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(SIZE_SMALL_BUTTON, small_rect, (60, 60, 60))
		if mouse_clicked:
			board_row = 7
			board_column = 12
			num_tile_on_board = 25
			num_same_tile = 2
			start_game = True
			GAME_TIME = 60
			click_sound.play()

	elif medium_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(SIZE_MEDIUM_BUTTON, medium_rect, (60, 60, 60))
		if mouse_clicked:
			board_row = 9
			board_column = 14
			num_tile_on_board = 21
			num_same_tile = 4
			start_game = True
			GAME_TIME = 120
			click_sound.play()

	elif large_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(SIZE_LARGE_BUTTON, large_rect, (60, 60, 60))
		if mouse_clicked:
			board_row = 11
			board_column = 16
			num_tile_on_board = 21
			num_same_tile = 6
			start_game = True
			GAME_TIME = 180
			click_sound.play()

	elif exit_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(EXIT_BUTTON, exit_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			show_select_size = False
			click_sound.play()

	if start_game:
		margin_x = (SCREEN_WIDTH - TILE_WIDTH * board_column) // 2
		margin_y = (SCREEN_HEIGHT - TILE_HEIGHT * board_row) // 2 + 15
		remaining_time = GAME_TIME
		curr_remaining_time = GAME_TIME
		board = get_random_board()
		return "start_game"
	
	return mouse_clicked, show_select_size

# Displays the pause panel:
def draw_panel_paused(mouse_x, mouse_y, mouse_clicked):
	global lives
 
	show_dim_screen()
	panel_rect = pg.Rect(0, 0, *PAUSE_PANEL_IMAGE.get_size())
	panel_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	screen.blit(PAUSE_PANEL_IMAGE, panel_rect)

	# Continue
	continue_rect = pg.Rect(0, 0, *CONTINUE_BUTTON.get_size())
	continue_rect.center = (panel_rect.centerx, panel_rect.centery)
	screen.blit(CONTINUE_BUTTON, continue_rect)
 
	# Replay
	replay_rect = pg.Rect(0, 0, *REPLAY_BUTTON.get_size())
	replay_rect.center = (panel_rect.centerx - 80, panel_rect.centery)
	screen.blit(REPLAY_BUTTON, replay_rect)
 
	# Home
	home_rect = pg.Rect(0, 0, *HOME_BUTTON.get_size())
	home_rect.center = (panel_rect.centerx + 80, panel_rect.centery)
	screen.blit(HOME_BUTTON, home_rect)
 
	show_paused = True

	if continue_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(CONTINUE_BUTTON, continue_rect, (60, 60, 60))
		if mouse_clicked:
			mouse_clicked = False
			draw_dark_image(CONTINUE_BUTTON, continue_rect, (120, 120, 120))
			show_paused = False
			click_sound.play()

	if replay_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(REPLAY_BUTTON, replay_rect, (60, 60, 60))
		if mouse_clicked:
			draw_dark_image(REPLAY_BUTTON, replay_rect, (120, 120, 120))
			click_sound.play()
			return "time_up"

	if home_rect.collidepoint(mouse_x, mouse_y):
		draw_dark_image(HOME_BUTTON, home_rect, (60, 60, 60))
		if mouse_clicked:
			draw_dark_image(HOME_BUTTON, home_rect, (120, 120, 120))
			click_sound.play()
			return "start_screen"

	return mouse_clicked, show_paused

# Sign-in system functions:
def load_players():
    try:
        with open('players.json', 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If file is empty or corrupted, return empty dict
                return {}
    except FileNotFoundError:
        # If file doesn't exist, create it with empty dict
        with open('players.json', 'w') as f:
            json.dump({}, f)
        return {}

def save_players(players):
    with open('players.json', 'w') as f:
        json.dump(players, f, indent = 2)

def update_players(board, level, lives, curr_remaining_time, remaining_time):
	global current_player
	if current_player != "[Guest]":
		players = load_players()
		players[current_player]["save"][0] = board
		players[current_player]["save"][1] = level
		players[current_player]["save"][2] = lives
		players[current_player]["save"][3] = curr_remaining_time - (GAME_TIME - remaining_time)
		save_players(players)

def verify_player(name, password):
    players = load_players()
    if name in players:
        return players[name]["password"] == password
    return False

def add_player(name, password):
    players = load_players()
    players[name] = {"password": password, "save": [None, 1, 3, GAME_TIME]}
    save_players(players)


# Displays the starting screen:
def start_screen():
	global sound_on, music_on, current_player, user_background, board_row, board_column, num_same_tile, num_tile_on_board, margin_x, margin_y, board, lives, level, remaining_time, curr_remaining_time
	global show_warning_guest, show_warning_saveless, show_instruction, show_sign_in, show_select_size, show_register

	# Currently open panels:
	show_warning_guest = False
	show_warning_saveless = False
	show_instruction = False
	show_sign_in = False
	show_register = False
	show_select_size = False

	# Signals:
	mouse_clicked = False

	mouse_x, mouse_y = 0, 0

	# Sign-in variables:
	error = ""
	name_input = ""
	password_input = ""
	input_active = "name"  # or "password"
 
	players = load_players()

	while True:
		
		Time.tick(FPS)
		screen.blit(START_SCREEN_BACKGOUND, (0, 0))

		# Logo
		image_width, image_height = LOGO_IMAGE.get_size()
		screen.blit(LOGO_IMAGE, ((SCREEN_WIDTH - image_width) // 2 - 20, (SCREEN_HEIGHT - image_height) // 2 - 175))

		# Player status text
		display_name = current_player
		user_background = pg.transform.scale(user_background, (len(display_name)*20 + 180, 72))
		user_background_rect = user_background.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT - image_height) // 2 + 60))
		screen.blit(user_background, user_background_rect)
		player_text = FONT_ARIAL.render(f"Playing as {display_name}", True, (0, 0, 0))
		text_rect = player_text.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT - image_height) // 2 + 60))
		screen.blit(player_text, text_rect)

		mouse_clicked = False
		panel_open = (show_instruction, show_warning_guest, show_warning_saveless, show_select_size, show_sign_in, show_register) # Checks if any panel is currently open

		# Event handling:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()

			if event.type == pg.MOUSEMOTION:
				mouse_x, mouse_y = event.pos   

			if event.type == pg.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = event.pos
				mouse_clicked = True

			# Taking input from user if signing in:     
			if event.type == pg.KEYDOWN and show_sign_in:
				if event.key == pg.K_TAB:
					input_active = "password" if input_active == "name" else "name"
				elif event.key == pg.K_RETURN:
					if (name_input == "[Guest]" and password_input == "") or verify_player(name_input, password_input):
						current_player = name_input
						show_sign_in = False
						name_input = ""
						password_input = ""
						error = ""
					else:
						if name_input == "[Guest]":
							error = "Leave password blank to play as [Guest]"
						elif name_input not in players:
							error = "Username not found"
						else:
							error = "Incorrect password"
						fail_sound.play()
				elif event.key == pg.K_BACKSPACE:
					if input_active == "name":
						name_input = name_input[:-1]
					else:
						password_input = password_input[:-1]
				else:
					if input_active == "name" and len(name_input) < NAME_LIMIT:
						name_input += event.unicode
					elif input_active == "password" and len(password_input) < PASSWORD_LIMIT:
						password_input += event.unicode
      
			# Taking input from user if registering:     
			if event.type == pg.KEYDOWN and show_register:
				if event.key == pg.K_TAB:
					input_active = "password" if input_active == "name" else "name"
				elif event.key == pg.K_RETURN:
					if name_input in players:
						error = "Username already exists"
						fail_sound.play()
					else:	
						if name_input == "[Guest]":
							error = "Cannot register as [Guest]"
							fail_sound.play()
						else:
							add_player(name_input, password_input)
							show_register = False
							name_input = ""
							password_input = ""
							error = ""
							players = load_players()
				elif event.key == pg.K_BACKSPACE:
					if input_active == "name":
						name_input = name_input[:-1]
					else:
						password_input = password_input[:-1]
				else:
					if input_active == "name" and len(name_input) < NAME_LIMIT:
						name_input += event.unicode
					elif input_active == "password" and len(password_input) < PASSWORD_LIMIT:
						password_input += event.unicode



		# Draws and checks if the relevant buttons are hovered over or clicked:
		if not any(panel_open):
			mouse_clicked = draw_new_game_button(mouse_x, mouse_y, mouse_clicked)

			mouse_clicked, continue_signal = draw_continue_button(mouse_x, mouse_y, mouse_clicked, players)
			if continue_signal:
				return

			mouse_clicked = draw_sign_in_button(mouse_x, mouse_y, mouse_clicked)
			mouse_clicked = draw_register_button(mouse_x, mouse_y, mouse_clicked)
			mouse_clicked = draw_sound_button(mouse_x, mouse_y, mouse_clicked)
			mouse_clicked = draw_music_button(mouse_x, mouse_y, mouse_clicked)
			mouse_clicked = draw_info_button(mouse_x, mouse_y, mouse_clicked)
   
		# Handles currently open panel: 
		# Instruction panel:
		if show_instruction:
			mouse_clicked, show_instruction = draw_panel_instruction(mouse_x, mouse_y, mouse_clicked)

		# Saveless warning panel (continuing without saved game):
		if show_warning_saveless:
			mouse_clicked, show_warning_saveless, show_select_size = draw_panel_warning_saveless(mouse_x, mouse_y, mouse_clicked)

		# Warning guest panel:
		if show_warning_guest:
			mouse_clicked, show_warning_guest, show_select_size = draw_panel_warning_guest(mouse_x, mouse_y, mouse_clicked)
		
		# Sign in panel:
		if show_sign_in:
			mouse_clicked, input_active, name_input, password_input, show_sign_in = draw_panel_sign_in(mouse_x, mouse_y, mouse_clicked, input_active, name_input, password_input, error)

		# Register panel:
		if show_register:
			mouse_clicked, input_active, name_input, password_input, show_register = draw_panel_register(mouse_x, mouse_y, mouse_clicked, input_active, name_input, password_input, error)

		# Select board size panel, this leads to the start of the game:
		if show_select_size:
			select = draw_panel_select_size(mouse_x, mouse_y, mouse_clicked)
			if select == "start_game":
				return 
			else:
				mouse_clicked, show_select_size = select

		pg.display.flip()



# Handles the main game loop where gameplay occurs:
def playing():
	global level, lives, show_paused, time_start_paused, time_paused, bonus_time, show_hint, current_hint, board, lives, level, remaining_time

	# Time variables:
	show_paused = False
	curr_remaining_time = GAME_TIME - (GAME_TIME - remaining_time)
	time_start_paused = 0
	time_paused = 0
	bonus_time = 0
	start_time = time.time()

	background = LIST_BACKGROUND[0] # get random background

	mouse_x, mouse_y = 0, 0
	clicked_tiles = [] # store index cards clicked
	hint = get_hint(board)
	mouse_clicked = False
	

	while True:
		Time.tick(FPS)

		screen.blit(background, (0, 0)) # set background
		dim_screen = pg.Surface(screen.get_size(), pg.SRCALPHA)
		pg.draw.rect(dim_screen, (0, 0, 0, 150), dim_screen.get_rect())
		screen.blit(dim_screen, (0, 0))
		draw_board(board)
		draw_lives(lives, level)
		draw_time_bar(start_time)
		draw_clicked_tiles(board, clicked_tiles)

		mouse_clicked = False

		if show_hint and current_hint:
			draw_hint(current_hint)

		if lives < 0:		
			return "game_over"

		# check event
		for event in pg.event.get():
			if event.type == pg.QUIT: 
				current_time = time.time()
				if time_start_paused:
					time_paused += current_time - time_start_paused
				elapsed_time = current_time - start_time - time_paused
				curr_remaining_time = GAME_TIME - elapsed_time + bonus_time
				
				update_players(board, level, lives, curr_remaining_time, remaining_time)
 
				pg.quit()
				sys.exit()

			if event.type == pg.MOUSEMOTION:
				mouse_x, mouse_y = event.pos

			if event.type == pg.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = event.pos
				mouse_clicked = True

			if event.type == pg.KEYUP:
				if event.key == pg.K_k: # use key k to hack game
					show_hint = False
					tile1_i, tile1_j = hint[0][0], hint[0][1]
					tile2_i, tile2_j = hint[1][0], hint[1][1]
					board[tile1_i][tile1_j] = 0
					board[tile2_i][tile2_j] = 0
					bonus_time += 1
					update_difficulty(board, level, tile1_i, tile1_j, tile2_i, tile2_j)

					if is_level_complete(board): 
						return "next"

					if not(board[tile1_i][tile1_j] != 0 and bfs(board, tile1_i, tile1_j, tile2_i, tile2_j)):
						hint = get_hint(board)
						while not hint:
							pg.time.wait(100)
							reset_board(board)
							hint = get_hint(board)



		# Draws and checks if the relevant buttons are hovered over or clicked:
		if not show_paused:
			# Draws pause button and checks if it's clicked:
			mouse_clicked = draw_pause_button(mouse_x, mouse_y, mouse_clicked)

			# Draw hint button and checks if it's clicked:
			mouse_clicked = draw_hint_button(mouse_x, mouse_y, mouse_clicked, board)

		is_time_up = check_time() # 0 if game over, 1 if lives -= 1, 2 if nothing
		if is_time_up == 0: #game over
			return "game_over"
		elif is_time_up == 1:
			return "time_up"
  
		if show_paused:
			select = draw_panel_paused(mouse_x, mouse_y, mouse_clicked)
			if select == "time_up":
				return "time_up"
			elif select == "start_screen":	
				return "start_screen"
			else:
				mouse_clicked, show_paused = select


		
		# update
		try:
			tile_i, tile_j = get_index_at_mouse(mouse_x, mouse_y)
			if board[tile_i][tile_j] != 0 and not show_paused:
				draw_border_tile(board, tile_i, tile_j)
				if mouse_clicked:
					mouse_clicked = False
					clicked_tiles.append((tile_i, tile_j))
					draw_clicked_tiles(board, clicked_tiles)
					if len(clicked_tiles) > 1: # 2 cards was clicked 
						path = bfs(board, clicked_tiles[0][0], clicked_tiles[0][1], tile_i, tile_j)
						if path:
							# delete the same card
							board[clicked_tiles[0][0]][clicked_tiles[0][1]] = 0
							board[tile_i][tile_j] = 0
							success_sound.play(maxtime = 1500)
							draw_path(path)

							bonus_time += 1

					
							show_hint = False  # Reset hint when tiles are matched
							current_hint = None

							# if level > 1, upgrade difficulty by moving cards 
							update_difficulty(board, level, clicked_tiles[0][0], clicked_tiles[0][1], tile_i, tile_j)

							if is_level_complete(board):
								if level == 5:
									pg.mixer.music.pause()
									fade_speed = 2
									alpha = 0
									time_win = 10
									tmp = time.time()
									
									win_sound.play(maxtime = 10000)
									show_dim_screen()
									while time.time() - tmp < 10:
										alpha += fade_speed
										if alpha > 255: alpha = 255
										tmp_image = WIN_BACKGROUND.copy()
										tmp_image.set_alpha(alpha)
										screen.blit(tmp_image, (180, 70))
										pg.display.flip()
									pg.mixer.music.unpause()
									return "victory"

								return "next"
						
						else:
							if not (clicked_tiles[0][0] == clicked_tiles[1][0] and clicked_tiles[0][1] == clicked_tiles[1][1]):
								fail_sound.play(maxtime = 500)

						#reset
						clicked_tiles = []
		except: pass
		pg.display.flip()

# Incorporates all the above functions to run the game: 
def main():
	#init pygame and module
	global level, lives, board, curr_remaining_time, remaining_time, show_hint
	
	while True:
		start_screen()

		while level <= MAX_LEVEL:
			random.shuffle(LIST_BACKGROUND)
			signal = playing()
			if signal == "start_screen":
				update_players(board, level, lives, curr_remaining_time, remaining_time)
				reset_game_info()
				break
			elif signal == "next":
				board = get_random_board()
				remaining_time = GAME_TIME
				level += 1
				pg.time.wait(300)
				pg.mixer.music.play()
			elif signal == "time_up":
				lives -= 1
				show_hint = False
				board = get_random_board()
				remaining_time = GAME_TIME
			elif signal == "game_over":
				update_players(None, 1, 3, GAME_TIME, GAME_TIME)
				show_dim_screen()
				game_over_sound.play()
				pg.mixer.music.pause()
				start_end = time.time()
				while time.time() - start_end <= TIME_END:
					gameover_width, gameover_height = GAMEOVER_BACKGROUND.get_size()
					screen.blit(GAMEOVER_BACKGROUND, (SCREEN_WIDTH // 2 - gameover_width // 2, SCREEN_HEIGHT // 2 - gameover_height // 2))
					pg.display.flip()
				reset_game_info()
				pg.mixer.music.unpause()
				break
			elif signal == "victory":
				update_players(None, 1, 3, GAME_TIME, GAME_TIME)
				reset_game_info()
				break


if __name__ == '__main__':
	main()
