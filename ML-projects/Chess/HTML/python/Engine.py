
EMPTY = 0
WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING = 1,2,3,4,5,6
BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING = -1,-2,-3,-4,-5,-6

FileA = 0x8080808080808080
FileB = 0x4040404040404040
FileC = 0x2020202020202020
FileD = 0x1010101010101010
FileE = 0x0808080808080808
FileF = 0x0404040404040404
FileG = 0x0202020202020202
FileH = 0x0101010101010101

notFileA = ~FileA & 0xFFFFFFFFFFFFFFFF
notFileAB = ~(FileA|FileB) & 0xFFFFFFFFFFFFFFFF
notFileH = ~FileH & 0xFFFFFFFFFFFFFFFF
notFileGH = ~(FileH|FileG) & 0xFFFFFFFFFFFFFFFF

class Board:
    def __init__(self):
        self.wpawn_bit = 0x000000000000FF00
        self.wknight_bit = 0x0000000000000042
        self.wbishop_bit = 0x0000000000000024
        self.wrook_bit = 0x0000000000000081
        self.wqueen_bit = 0x0000000000000010
        self.wking_bit = 0x0000000000000008

        self.bpawn_bit = 0x00FF000000000000
        self.bknight_bit = 0x4200000000000000
        self.bbishop_bit = 0x2400000000000000
        self.brook_bit = 0x8100000000000000
        self.bqueen_bit = 0x1000000000000000
        self.bking_bit = 0x0800000000000000

        self.update_squares()

        

    def update_squares(self):
        self.white_occupied = (self.wpawn_bit|self.wknight_bit|self.wbishop_bit|self.wrook_bit|self.wqueen_bit|self.wking_bit)
        self.black_occupied = (self.bpawn_bit|self.bknight_bit|self.bbishop_bit|self.brook_bit|self.bqueen_bit|self.bking_bit)
        self.board_bit = (self.black_occupied|self.white_occupied)
        
    def bitboard_to_array(self):
        board_array = [EMPTY]*64
        for square in range(63, 0, -1):
            mask = (1<<square)
            if (self.board_bit & mask) != 0:
                if (mask & self.brook_bit) != 0:
                    board_array[63-square] = BROOK
                elif (mask & self.bbishop_bit) != 0:
                    board_array[63-square] = BBISHOP
                elif (mask & self.bknight_bit) != 0:
                    board_array[63-square] = BKNIGHT
                elif (mask & self.bqueen_bit) != 0:
                    board_array[63-square] = BQUEEN
                elif (mask & self.bking_bit) != 0:
                    board_array[63-square] = BKING
                elif (mask & self.bpawn_bit) != 0:
                    board_array[63-square] = BPAWN

                elif (mask & self.wrook_bit) != 0:
                    board_array[63-square] = WROOK
                elif (mask & self.wbishop_bit) != 0:
                    board_array[63-square] = WBISHOP
                elif (mask & self.wknight_bit) != 0:
                    board_array[63-square] = WKNIGHT
                elif (mask & self.wqueen_bit) != 0:
                    board_array[63-square] = WQUEEN
                elif (mask & self.wking_bit) != 0:
                    board_array[63-square] = WKING
                elif (mask & self.wpawn_bit) != 0:
                    board_array[63-square] = WPAWN
        return board_array

    def get_pawn_moves(self, pawn_bb, is_white=True):
        moves = 0

        init_position = 0x000000000000FF00 if is_white else 0x00FF000000000000

        moves |= 

    def get_knight_moves(self, knight_bb):
        moves = 0
        
        moves |= (knight_bb & notFileH) << 15
        moves |= (knight_bb & notFileH) >> 17
        moves |= (knight_bb & notFileGH) << 6
        moves |= (knight_bb & notFileGH) >> 10
        
        moves |= (knight_bb & notFileA) << 17
        moves |= (knight_bb & notFileA) >> 15
        moves |= (knight_bb & notFileAB) << 10
        moves |= (knight_bb & notFileAB) >> 6

        return moves

    def get_king_moves(self, king_bb):
        moves = 0
        moves |= (king_bb << 8)
        moves |= (king_bb >> 8)
        moves |= (king_bb & notFileA) << 1
        moves |= (king_bb & notFileA) << 9
        moves |= (king_bb & notFileA) >> 7
        
        moves |= (king_bb & notFileH) >> 1
        moves |= (king_bb & notFileH) >> 9
        moves |= (king_bb & notFileH) << 7
        return moves
#class GameState:
 #   self.board = Board()
  #  self.board_arr = self.board.bitboard_to_array()
   # self.white_to_move = True

    
            
if __name__ == '__main__':
    
    board = Board()

    board_arr = board.bitboard_to_array()
    test_nbb = 0x0000000008000000
    test_kbb = 0x0000000000000100
    print(board_arr)
    print(board.board_bit)
    print("------------------------------")
    print(board.get_knight_moves(test_nbb))
    print(bin(board.get_knight_moves(test_nbb)))
    print("---------------------------------")
    print(board.get_king_moves(test_kbb))
    print(bin(board.get_king_moves(test_kbb)))
    #self.move_log = []
    
    
    
    
    
    
    