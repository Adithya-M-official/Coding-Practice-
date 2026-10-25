import numpy as np
import os 
import time

class Board:
	def __init__(self):
		self.board = board = [""] * 9
		
	def slot_repr(self, slot):
		return f"{slot}" if self.board[slot-1] == "" else f"{self.board[slot-1]}" 
	
	def __str__(self):
		board_repr = f"""
		| {self.slot_repr(1)} | {self.slot_repr(2)} | {self.slot_repr(3)} |
		-------------
		| {self.slot_repr(4)} | {self.slot_repr(5)} | {self.slot_repr(6)} |
		-------------
		| {self.slot_repr(7)} | {self.slot_repr(8)} | {self.slot_repr(9)} |
		"""
		return board_repr
	

class Engine:
	def __init__(self, user_char, comp_char, difficulty = "Easy", max_depth=1):
		self.board = Board()
		self.user_char = user_char
		self.comp_char = comp_char
		self.max_depth = max_depth
		self.difficulty = difficulty
		self.winning_bits = [0b111000000, 0b000111000, 0b000000111,0b100010001, 0b001010100, 0b100100100,0b010010010,0b001001001]
		
	def render(self):
		print(self.board)
		
	def get_bit_ints(self):
		user_bit, comp_bit = 0,0
		for index, char in enumerate(self.board.board):
			if char == self.user_char:
				user_bit |= (1<<index)
			elif char == self.comp_char:
				comp_bit |= (1<<index)
		board_bit = user_bit | comp_bit
		
		return user_bit, comp_bit, board_bit
	
	def input_choices(self):
		user_bit, comp_bit, board_bit = self.get_bit_ints()
			
		for slot in range(9):
			mask = (1<<slot)
			if (user_bit & mask) != 0:
				self.board.board[slot] = self.user_char
			if (comp_bit & mask) != 0:
				self.board.board[slot] = self.comp_char
				
	def check_wins(self):
		user_bit, comp_bit, _ = self.get_bit_ints()
		user_won = any((user_bit & bit_int) == bit_int for bit_int in self.winning_bits)
		comp_won = any((comp_bit & bit_int) == bit_int for bit_int in self.winning_bits)
		
		return user_won, comp_won
		
	def get_state_index(self):
		user_bit, comp_bit, _ = self.get_bit_ints()
		state_idx = 0
		
		powerof_3 = np.power(3, np.arange(9))
		
		for i in range(9):
			mask = (1<<i)
			if (user_bit & mask) != 0:
				state_idx += 1*powerof_3[i]
			elif (comp_bit & mask) != 0:
				state_idx += 2*powerof_3[i]
		return state_idx
	
	def step(self, action, comp_char):
		self.board.board[action] = comp_char
		user_bit, comp_bit, board_bit = self.get_bit_ints()
		next_state = (user_bit, comp_bit)
		user_won, comp_won = self.check_wins()
		
		if user_won:
			reward = -1.0
			done = True
		elif comp_won:
			reward = 1.0
			done = True
		elif board_bit == 0b111111111:
			reward = 0.05
			done = True
		else:
			reward = 0.0
			done = False
			
		return next_state, done, reward
		
	def minimax(self, user_bit, comp_bit, depth, max_depth, is_maximising):
		board_bit = user_bit|comp_bit
		empty_slots = ~board_bit & 0b111111111
		user_won, comp_won = self.check_wins()
		
		if user_won:
			return -1 + (0.05*depth)
		elif comp_won:
			return 1 - (0.05*depth)
		elif board_bit == 0b111111111:
			return 0.05
		
		if depth >= max_depth:
			return 0
			
		if is_maximising:
			best_score = float("-inf")
			for slot in range(9):
				is_empty = (empty_slots & (1<<slot)) != 0
				if is_empty:
					new_comp_bit = (comp_bit | (1<<slot))
					new_score = self.minimax(user_bit, new_comp_bit, depth+1, max_depth, is_maximising=False)
					best_score = max(best_score, new_score)
			return best_score
		else:
			best_score = float("inf")
			for slot in range(9):
				is_empty = (empty_slot & (1<<slot)) != 0
				if is_empty:
					new_user_bit = (user_bit | (1<<slot)) 
					new_score = self.minimax(new_user_bit, comp_bit, depth+1, max_depth, is_maximising=True)
					best_score = min(new_score, best_score)
			return best_score
				
				
	def get_best_move(self, max_depth):
		depth = 1
		is_maximising = True
		user_bit, comp_bit, board_bit = self.get_bit_ints()
		empty_slots = ~board_bit & 0b111111111
		
		best_score = float("-inf")
		best_slot = None
		for slot in range(9):
			is_empty = (empty_slots & (1<<slot)) != 0
			if is_empty:
				new_comp_bit = (comp_bit | (1<<slot))
				new_score = self.minimax(user_bit, new_comp_bit, depth, max_depth, is_maximising = False)
				
				if new_score > best_score:
					best_score = new_score
					best_slot = slot
		return best_slot
		
		
class Bot:
	def __init__(self,qtable_file, render_mode=None):
		self.qtable_file = qtable_file
		self.render_mode = render_mode
		
		if os.path.exists(self.qtable_file):
			self.q_table = np.load(self.qtable_file)
			print("Trained Qtable Loaded!")
		else:
			self.q_table = np.zeros((3**9, 9))
			print("Qtable file not found. Initializing empty Qtable.")
			
	def train(self, episodes):
		if self.render_mode != None:
			print("Render Mode has been set to 'human'. Change to None to train the model!")
			return
			
		alpha = 0.2
		gamma = 0.90
		epsilon = 1.0
		decay = 0.997
		min_epsilon = 0.01
		
		user_epsilon = 1.
		user_epsilon_decay = 0.997
		user_min_epsilon = 0.15
			
		for episode in range(episodes):
			engine = Engine(user_char = "X", comp_char = "O")
			done = False
			prev_state, prev_action = None, None
			
			while not done:
				
				user_bit, comp_bit, board_bit = engine.get_bit_ints()
				#allowed_hmoves = [s for s in range(9) if (board_bit & (1<<s)) == 0]
#				h_move = np.random.choice(allowed_hmoves)
#				
				if np.random.rand() < user_epsilon:
					allowed_hmoves = [s for s in range(9) if (board_bit & (1<<s)) == 0]
					h_move = np.random.choice(allowed_hmoves)
				else:
					h_move = engine.get_best_move(max_depth = 9)
					
				_, done, reward = engine.step(h_move, engine.user_char)
				state_index = engine.get_state_index()
		
				
				
				if done:
					if reward == -1.0:
						best_future_q = 0.0
						td_error = reward - self.q_table[prev_state, prev_action]
						self.q_table[prev_state, prev_action] += alpha*td_error
					elif reward == 0.05:
						best_future = 0.0
						td_error = reward - self.q_table[prev_state, prev_action]
						self.q_table[prev_state, prev_action] += alpha*td_error
					break
					
				_,_, board_bit = engine.get_bit_ints()
				q_values = np.copy(self.q_table[state_index])
				for slot in range(9):
					if (board_bit & (1<<slot)) != 0:
						q_values[slot] = -np.inf
				
				if np.random.rand() < epsilon:
					allowed_cmoves = [s for s in range(9) if (board_bit & (1<<s)) == 0]
					action = np.random.choice(allowed_cmoves)
				else:
					action = np.argmax(q_values)
				
				next_state, done, reward = engine.step(action, engine.comp_char)
				if done:
					if reward == 1.0:
						best_future_q = 0.0
						td_error = reward - self.q_table[state_index, action]
						self.q_table[state_index, action] += alpha*td_error
					elif reward == 0.05:
						best_future_q = 0.0
						td_error = reward - self.q_table[state_index, action]
						self.q_table[state_index, action] += alpha*td_error
					break
					
				next_state_idx = engine.get_state_index()
				best_future_q = np.max(self.q_table[next_state_idx])
				td_target = reward + (gamma*best_future_q)
				td_error = td_target - self.q_table[state_index, action]
				
				self.q_table[state_index, action] += alpha*td_error
				
				prev_state, prev_action = state_index, action
				
				state_index = next_state_idx
			epsilon = max(min_epsilon, epsilon*decay)
				
			
		print("Non-zero Q values:", np.count_nonzero(self.q_table))
		print("Max Q:", np.max(self.q_table))
		print("Min Q:", np.min(self.q_table))
	
		np.save(self.qtable_file, self.q_table)
		print("Updated Qtable Saved!")
		
	
	def play_match(self):
		if self.render_mode != 'human':
			print("Render Mode has been set to None. Change to 'human' to play against the bot!")
			return
			
		while True:
			print(" TIC TAC TOE (VS BOT) ")
	
			print("Welcome! what would you like to do? (1/2)")
	
			choice = input(f"""

2) Play a game!
>>""")
            # difficulty choice (1) in progress.

			#if choice.strip() == "1":
#				print("What would you like to change the difficulty to? (1/2/3/4)")
#				print(f"1) Easy{is_current('Easy')}")
#				print(f"2) Medium{is_current('Medium')}")
#				print(f"3) Hard{is_current('Hard')}")
#				print(f"4) Expert{is_current('Expert')}")
#		
#				difficulty_input = input(">>")
#			
#				match difficulty_input.strip():
#					case "1":
#						difficulty = "Easy"
#						max_depth = 1
#					case "2":
#						difficulty = "Medium"
#						max_depth = 3
#					case "3":
#						difficulty = "Hard"
#						max_depth = 6
#					case "4":
#						difficulty = "Expert"
#						max_depth = 9

			if choice == '2':
				print("What character would you like to play as? (X or O)")
				user_char = input(">> ").upper()
				comp_char = "O" if user_char == "X" else "X"
				engine = Engine(user_char, comp_char)
				
				print("Okay, lets play! You get first move.")
			
				engine.render()
		
				while True:
					
					print("What slot would you like to put your character in? (enter any of the number you see on board) ")
					user_slot = int(input(">> ")) -1 
					
					
					next_state, reward, done = engine.step(user_slot, engine.user_char)
					_, _, board_bit = engine.get_bit_ints()
					
					if done:
						engine.render()
						user_won, comp_won = engine.check_wins()
						if user_won:
							print('Yay you won!')
							print("==================================")
							break
						if comp_won:
							print('No you lost!')
							print("==================================")
							break
						if board_bit == 0b111111111:
							print("Draw!")
							print("==================================")
							break
			
					state_idx = engine.get_state_index()
					q_values = np.copy(self.q_table[state_idx])
					_, _, board_bit = engine.get_bit_ints()
					
					for slot in range(9):
						if (board_bit & (1<<slot)) != 0:
							q_values[slot] = -np.inf
							
					best_slot = np.argmax(q_values)
		
					_, reward, done = engine.step(best_slot, engine.comp_char)
					_, _, board_bit = engine.get_bit_ints()
					engine.render()
					
					if done:
						engine.render()
						user_won, comp_won = engine.check_wins()
						if user_won:
							print('Yay you won!')
							print("==================================")
							break
						if comp_won:
							print('No you lost!')
							print("==================================")
							break
						if board_bit == 0b111111111:
							print("Draw!")
							print("==================================")
							break
			
			
#set to train.
mode = None
		
tictactoe_agent = Bot(qtable_file = "Trained weights/tictactoeqtable.npy", render_mode = mode)
		
tictactoe_agent.train(15000) if tictactoe_agent.render_mode == None else tictactoe_agent.play_match()
