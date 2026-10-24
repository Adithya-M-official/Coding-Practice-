
board = ["", "", "","", "", "","", "", ""]
		 
user_char = "X"
computer_char = "O"
max_depth = 1
difficulty = "Easy"
winning_bit_int = [0b111000000, 0b000111000, 0b000000111,0b100010001, 0b001010100, 0b100100100,0b010010010,0b001001001]
				   
def is_current(level):
	return " (current)" if difficulty == level else ""
				
def slot_repr(slot):
	return f"{slot}" if board[slot-1] == "" else f"{board[slot-1]}" 
	
def show_board():
	board_repr = f"""
		| {slot_repr(1)} | {slot_repr(2)} | {slot_repr(3)} |
		-------------
		| {slot_repr(4)} | {slot_repr(5)} | {slot_repr(6)} |
		-------------
		| {slot_repr(7)} | {slot_repr(8)} | {slot_repr(9)} |
		"""
	if "" in board:
		print(board_repr)
		
	
def input_user_choice(char, slot):
	global user_char, computer_char
	if char == "X":
		user_char, computer_char = char, "O"
	elif char == "O":
		user_char, computer_char = char, "X"
		
	board[slot-1] = char
	
def bit_int_to_board(computer_bit_int, board):
	for slot in range(9):
		mask = (1<<slot)
		if (computer_bit_int & mask) != 0:
			board[slot] = computer_char
	
def evaluate_board(board):
	user_bit_int = 0
	computer_bit_int = 0
	
	for index, char in enumerate(board):
		if char == user_char:
			user_bit_int |= (1 << index)
		if char == computer_char:
			computer_bit_int |= (1<<index)
	return user_bit_int, computer_bit_int
	
def evaluate_position(user_bit_int, computer_bit_int):
	user_won = any((user_bit_int & bit_int) == bit_int for bit_int in winning_bit_int)
	computer_won = any((computer_bit_int & bit_int) == bit_int for bit_int in winning_bit_int)
	
	return user_won, computer_won


def minimax(user_bit_int, computer_bit_int, depth, max_depth, is_maximising):
	position_bit_int = user_bit_int | computer_bit_int
	empty_slots = ~position_bit_int & 0b111111111
	
	user_won, computer_won = evaluate_position(user_bit_int, computer_bit_int)
	
	if user_won:
		return -10 + depth
	if computer_won:
		return 10 - depth
	if position_bit_int == 0b111111111:
		return 0
		
	if depth >= max_depth:
		return 0
	
	if is_maximising:
		best_score = float('-inf')
		for slot in range(9):
			is_empty = (empty_slots & (1<<slot)) != 0
			
			if is_empty:
				new_comp_bit_int = computer_bit_int | (1<<slot)
				score = minimax(user_bit_int, new_comp_bit_int, depth+1, max_depth, False)
				best_score = max(best_score, score)
		return best_score
		
	else:
		best_score = float('inf')
		for slot in range(9):
			is_empty = (empty_slots & (1<<slot)) != 0
			if is_empty:
				new_user_bit_int = user_bit_int | (1<<slot)
				score = minimax(new_user_bit_int, computer_bit_int, depth+1, max_depth, True)
				best_score = min(best_score, score)
		return best_score

def get_best_move(board, max_depth):
	depth = 1
	is_maximising = True
	user_bit_int, computer_bit_int = evaluate_board(board)
	position_bit_int = user_bit_int | computer_bit_int
	
	best_score = float("-inf")
	best_slot = None
	
	empty_slots = ~position_bit_int & 0b111111111
	
	for slot in range(9):
		is_empty = (empty_slots & (1<<slot)) != 0
		
		if is_empty:
			new_comp_bit_int = computer_bit_int | (1<<slot)
			score = minimax(user_bit_int, new_comp_bit_int, depth, max_depth = max_depth, is_maximising = False)
			
			if score > best_score:
				best_score = score
				best_slot = slot
	return best_slot



while True:
	board = ["", "", "","", "", "","", "", ""]
	
	print(" TIC TAC TOE (VS BOT) ")
	
	print("Welcome! what would you like to do? (1/2)")
	
	choice = input(f"""
1) Change difficulty (current: {difficulty}; available: Easy, Medium, Hard, Expert)
2) Play a game!
>>""")

	if choice.strip() == "1":
		print("What would you like to change the difficulty to? (1/2/3/4)")
		print(f"1) Easy{is_current('Easy')}")
		print(f"2) Medium{is_current('Medium')}")
		print(f"3) Hard{is_current('Hard')}")
		print(f"4) Expert{is_current('Expert')}")
		
		difficulty_input = input(">>")
		
		match difficulty_input.strip():
			case "1":
				difficulty = "Easy"
				max_depth = 1
			case "2":
				difficulty = "Medium"
				max_depth = 3
			case "3":
				difficulty = "Hard"
				max_depth = 6
			case "4":
				difficulty = "Expert"
				max_depth = 9

	else:
		print("What character would you like to play as? (X or O)")
		user_char = input(">> ").upper()
		
		print("Okay, lets play! You get first move.")
		
		show_board()
		
		while True:
			print("What slot would you like to put your character in? (enter any of the number you see on board) ")
			user_slot_input = int(input(">> "))
			input_user_choice(user_char, user_slot_input)
			
			user_bit_int, computer_bit_int = evaluate_board(board)
			position_bit = computer_bit_int | user_bit_int
			user_won, comp_won = evaluate_position(user_bit_int, computer_bit_int)
			
			
			if user_won:
				print('Yay you won!')
				print("==================================")
				break
			if position_bit == 0b111111111:
				print("Draw!")
				print("==================================")
				break
				
			best_slot = get_best_move(board, max_depth)
			board[best_slot] = computer_char
			
			user_bit_int, computer_bit_int = evaluate_board(board)
			position_bit = computer_bit_int | user_bit_int
			user_won, comp_won = evaluate_position(user_bit_int, computer_bit_int)
			
			if comp_won:
				print('No you lost!')
				print("==================================")
				break
			if position_bit == 0b111111111:
				print("Draw!")
				print("==================================")
				break
			
			show_board()
			
		