import numpy as np
PRINT_DEBUG = False
class Board:
    def __init__(self, fen):
        self.move_stack = []
        self.board = list(
                        "            "
                        "            "
                        "  rnbqkbnr  "
                        "  pppppppp  "
                        "  ........  "
                        "  ........  "
                        "  ........  "
                        "  ........  "
                        "  PPPPPPPP  "
                        "  RNBQKBNR  "
                        "            "
                        "            "
                    )
        '''self.board = list(
                        "            "
                        "            "
                        "  R......R  "
                        "  ...Q....  "
                        "  .Q....Q.  "# these are just some test positions
                        "  ....Q...  "# this one has 218 legal mvoes for white
                        "  ..Q....Q  "
                        "  Q....Q..  "
                        "  pp.Q....  "
                        "  kBNN.KB.  "
                        "            "
                        "            "
                    )
        
        self.board = list(
                        "            "
                        "            "
                        "  r...k..r  "
                        "  p.ppqpb.  "
                        "  bn..pnp.  "
                        "  ...PN...  "# this position at perft 5 should give a result
                        "  .p..P...  "# of exactly 193690690
                        "  ..N..Q.p  "# positions
                        "  PPPBBPPP  "
                        "  R...K..R  "
                        "            "
                        "            "
                    )
        self.board = list(
                        "            "
                        "            "
                        "  K.k.....  "#
                        "  ........  "#
                        "  P.......  "# perft 6 - 2217
                        "  ........  "#
                        "  ........  "#
                        "  ........  "#
                        "  ........  "#
                        "  ........  "#
                        "            "
                        "            "
                    )
        self.board = list(
                        "            "
                        "            "
                        "  ........  "#
                        "  ..K.....  "#
                        "  ........  "# perft 4 - 23527
                        "  ..n.....  "#
                        "  ..q.....  "#
                        "  .....k..  "#
                        "  ........  "#
                        "  ........  "#
                        "            "
                        "            "
                    )
        self.board = list(
                        "            "
                        "            "
                        "  rnbq.k.r  "#
                        "  pp.Pbppp  "# perft test results
                        "  ..p.....  "# rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8  
                        "  ........  "# depth 1 = 44
                        "  ..B.....  "# depth 2 = 1486
                        "  ........  "# depth 3 = 62379
                        "  PPP.NnPP  "# depth 4 = 2103487
                        "  RNBQK..R  "#
                        "            "
                        "            "
                    )'''
        self.white, self.black = [True, True], [True, True]
        self.gst_white, self.gst_black = [], []
        self.notation = dict(zip([i + 1 for i in range(9)], [chr(i + 65) for i in range(8)]))
        U, D, L, R = int(-(np.sqrt(len(self.board)))), int(np.sqrt(len(self.board))), -1, 1
        self.dirs = {
            "N": ((U + U + L, U + U + R, L + L + U, L + L + D, R + R + U, R + R + D, D + D + L, D + D + R), False),
            "B": ((U + L, U + R, D + L, D + R), True),
            "R": ((U, D, L, R), True),
            "Q": ((U + L, U + R, D + L, D + R, U, D, L, R), True),
            "K": ((U + L, U + R, D + L, D + R, U, D, L, R), False),
            "P": ((U, U + R, U + L), False)
            }
        self.history = []
        self.player = True
        if not fen == "None":
            self.set_fen(fen)

    def play_move(self, inputX: str):
        self.makeMove(inputX.split(), list(self.legal_moves(self.player, self.board, True, False)), False, self.player)
        self.player = not self.player

    def fen_to_mailbox(self, fen_str:str) -> list:
        fen_str = fen_str.split()[0]
        board = []
        for i in fen_str:
            if str(i).isdigit():
                for i in range(int(i)):
                    board.append(".")
            if str(i) in "rnbkqpRNBKQP":
                board.append(i)

        padded_board = [" " for i in range(144)]
        for index, item in enumerate(board):
            padded_board(self.twelve_ify)
        return board


    def is_mate(self):
        leg_OM = (list(zip(*(list(self.legal_moves(not self.player, self.board, False, True)))))[1])
        if self.player:
            ki = self.board.index("K")
        else:
            ki = self.board.index("k")
        if len(self.legal_moves(self.player, self.board, True, False)) == 0:
            for i in leg_OM:
                if i == ki:
                    return 1
            return 2
        return 0
    
    def set_fen(self, fen: str):
        self.board = list()
        pos = fen.split()[0]
        player = fen.split()[1]
        if player == "w":
            self.player = True
        else:
            self.player = False
        
        for _ in range(26):
            self.board.append(" ")
        for character in pos:
            if character == "/":
                for _ in range(4):
                    self.board.append(" ")

            elif character.isdigit():
                for _ in range(int(character)):
                    self.board.append(".")
            
            else:
                self.board.append(character)
        for _ in range(26):
            self.board.append(" ")

    def is_check(self):
        leg_OM = (list(zip(*(list(self.legal_moves(not self.player, self.board, False, True)))))[1])
        if self.player:
            ki = self.board.index("K")
        else:
            ki = self.board.index("k")
        for i in leg_OM:
            if i == ki:
                return True
        return False
    
    def is_light_square(self, index: int):
        if index % 2 == 0: return True
        else: return False
        
    def legal_moves(self, player: bool, br: str, is_checking: bool, icc: bool):
        if br.count("K") + br.count("k") != 2:
            return []
        legal_moves = []
        if player:
            for index, item in enumerate(br):
                try:
                    for dir in self.dirs[item][0]:
                        if not self.dirs[item][1]: ray_dist = 1
                        else: ray_dist = 8
                        for rays in range(ray_dist):
                            if item == "P":
                                ind = index + (dir * (rays + 1))
                                if index % 12 == (index + dir) % 12:
                                    if br[index + dir] == ".":
                                        legal_moves.append((index, ind))
                                        if index > 97 and index < 106:
                                            if br[index + (dir * 2)] == ".":
                                                legal_moves.append((index, index + (dir * 2)))
                                        if ind > 25 and ind < 34: 
                                            for promotion in "NQRB":
                                                legal_moves.append((index, ind, promotion))
                                                try:
                                                    legal_moves.remove((index, ind))
                                                except: pass
                                else:
                                    if PRINT_DEBUG:
                                        print(ind, self.gst_black)
                                    if br[ind] != " " and br[ind] != "." and br[ind].islower() == player or [ind] in self.gst_black:
                                        legal_moves.append((index, ind))
                                        if ind > 25 and ind < 34: 
                                                for promotion in "NQRB":
                                                    legal_moves.append((index, ind, promotion))
                                                    try:
                                                        legal_moves.remove((index, ind))
                                                    except: pass
                            else:
                                ind = index + (dir * (rays + 1))
                                checkspot = br[ind]
                                if item == "K" and index == 114 and not icc:
                                    leg_OM = (list(zip(*(list(self.legal_moves(False, br, False, True)))))[1])
                                    if not 114 in leg_OM:
                                        if self.white[1] and 116 not in leg_OM and 115 not in leg_OM and br[116] == "." and br[115] == "." and br[117] == "R":
                                            try: legal_moves.index((114, 116, 117, 115))
                                            except: legal_moves.append((114, 116, 117, 115))
                                        if self.white[0] and 113 not in leg_OM and 112 not in leg_OM and br[112] == "." and br[113] == "." and br[110] == "R":
                                            try: legal_moves.index((114, 112, 110, 113))
                                            except: legal_moves.append((114, 112, 110, 113))
                                if checkspot == " ": break
                                elif checkspot == ".": legal_moves.append((index, ind))
                                elif checkspot.islower():
                                    legal_moves.append((index, ind))
                                    break
                                elif checkspot.isupper(): break
                except (KeyError, IndexError): pass
            if is_checking: 
                return sorted(self.check_lg(legal_moves, player))
            else:
                return legal_moves
        else: ###################### EVERYtHING BELOW THIS LINE IN THE FUNCTION IS JUST A COPY BUT ALTERED FOR BLACK'S PIECES
            for index, item in enumerate(br):
                try:
                    if item.islower():
                        for dir in (self.dirs[item.upper()][0]): 
                            if not self.dirs[item.upper()][1]: ray_dist = 1
                            else: ray_dist = 8
                            for rays in range(ray_dist):
                                if item == "p":
                                    ind = index - (dir * (rays + 1))
                                    if index % 12 == (ind) % 12:
                                        if br[ind] == ".":
                                            legal_moves.append((index, ind))
                                            if index > 37 and index < 46:
                                                if br[index + (-dir * 2)] == ".":
                                                    legal_moves.append((index, index + (-dir * 2)))
                                            if ind > 109 and ind < 118:
                                                for promotion in "nqrb":
                                                    legal_moves.append((index, ind, promotion))
                                                    try: legal_moves.remove((index, ind))
                                                    except: pass
                                    else:
                                        if self.board[ind] != " " and br[ind] != "." and br[ind].isupper() == bool(not player) or [ind] in self.gst_white:
                                            legal_moves.append((index, ind))
                                            if ind > 109 and ind < 118: 
                                                for promotion in "nqrb":
                                                    legal_moves.append((index, ind, promotion))
                                                    try:
                                                        legal_moves.remove((index, ind))
                                                    except: pass
                                        pass
                                else:
                                    ind = index + (dir * (rays + 1))
                                    checkspot = br[ind]
                                    if item == "k" and index == 30 and not icc:
                                        leg_OM = (list(zip(*(list(self.legal_moves(True, br, False, True)))))[1])
                                        if not 30 in leg_OM:
                                            if self.black[1] and 32 not in leg_OM and 31 not in leg_OM and br[32] == "." and br[31] == "." and br[33] == "r":
                                                try: legal_moves.index((30, 32, 33, 31))
                                                except: legal_moves.append((30, 32, 33, 31))
                                            if self.black[0] and 29 not in leg_OM and 28 not in leg_OM and br[28] == "." and br[29] == "." and br[26] == "r":
                                                try: legal_moves.index((30, 28, 26, 29))
                                                except: legal_moves.append((30, 28, 26, 29))
                                    if checkspot == " ": break
                                    elif checkspot == ".": legal_moves.append((index, ind))
                                    elif checkspot.isupper():
                                        legal_moves.append((index, ind))
                                        break
                                    elif checkspot.islower(): break
                                    if PRINT_DEBUG:
                                        print(index, ind)
                except KeyError:
                    pass       
            if is_checking:
                return sorted(self.check_lg(legal_moves, player))
            else:
                return legal_moves

    def check_lg(self, leg_moves: list, player: bool):
        nlm = leg_moves[:]
        for moves in leg_moves:
            temp_board = list(self.board[:])
            if player:
                king_spot = self.index(temp_board, "K")
            else:
                king_spot = self.index(temp_board, "k")

            if king_spot == moves[0]:
                king_spot = moves[1]
            temp_board[moves[1]] = temp_board[moves[0]]
            temp_board[moves[0]] = "."
            leg_opp_moves = self.legal_moves(not player, temp_board, False, False)
            for i in range(len(leg_opp_moves)):
                if king_spot == leg_opp_moves[i][1]:
                    nlm.remove(moves)
                    break
        return nlm

    def index(self, iterable, indexing):
        for i in range(len(iterable)):
            if iterable[i] == indexing:
                return i
    
    
    def cleaned_moves(self):
        nlm = []
        for i in self.legal_moves(self.player, self.board, True, False):
            from_sq, to_sq = i[0], i[1]
            frow, fcol, trow, tcol = from_sq//12, from_sq%12, to_sq//12, to_sq%12
            nlm.append(((frow - 2) * 8 + (fcol - 2), (trow - 2) * 8 + (tcol - 2)))
        return nlm
    
    def clean_moves(self, move):
        alphabet = {
            0:"A",
            1:"B",
            2:"C",
            3:"D",
            4:"E",
            5:"F",
            6:"G",
            7:"H"
        }
        from_sq, to_sq = move[0], move[1]
        frow, fcol, trow, tcol = from_sq//12, from_sq%12, to_sq//12, to_sq%12
        return ((alphabet[fcol - 2], abs((frow- 2) - 8), alphabet[tcol - 2], abs((trow - 2 - 8))))
    def print_board(self, position:str):
        counter = 0
        for w in range(12):
            print("| ", end = "")
            for l in range(12):
                if position[counter] == " ":
                    if len(str(counter)) == 1:
                        print(f"{counter}  |  ", end = "")
                    elif len(str(counter)) == 2:
                        print(f"{counter} |  ", end = "")
                    elif len(str(counter)) == 3:
                        print(f"{counter} | ", end = "")
                else:
                    print(f"{position[counter]}  |  ", end = "")
                counter += 1
            print("\n", "-" * (int(np.sqrt(len(position))*4) + 1), sep = "")
        
    def makeMove(self, player_inp, lm, is_castle: bool, player: bool):
        #print(player_inp)
        try:
            player_inp = self.ltt(player_inp)
        except:
            if len(player_inp) == 3:
                if (int(player_inp[0]), int(player_inp[1]), str(player_inp[2])) in lm:
                    if player:
                        if len(player_inp) == 3 and player and player_inp[2] in "RBQN":
                            self.board[int(player_inp[1])] = player_inp[2]
                            self.board[int(player_inp[0])] = "."
                            self.gst_white = []; self.gst_black = []
                            self.move_stack.append((player_inp, self.white, self.black, self.gst_white, self.gst_black))
                        else: raise ValueError("Error Invalid Move")
                    else:
                        if len(player_inp) == 3 and not player and player_inp[2] in "rbqn":
                            self.board[int(player_inp[1])] = player_inp[2]
                            self.board[int(player_inp[0])] = "."
                            self.gst_white = []; self.gst_black = []
                            self.move_stack.append((player_inp, self.white, self.black, self.gst_white, self.gst_black))
                        else: raise ValueError(f"Error Invalid Move: move-{player_inp}, player-{player}")
                else: raise ValueError(f"Error Invalid Move: move-{player_inp}, player-{player}")
            else: raise ValueError(f"Error Invalid Move: move-{player_inp}, player-{player}")
                
        else:
            #print(player_inp)
            if is_castle:
                self.board[int(player_inp[1])] = str(self.board[int(player_inp[0])])
                self.board[int(player_inp[0])] = "."
                self.gst_white = []; self.gst_black = []
                self.move_stack.append((player_inp, self.white, self.black, self.gst_white, self.gst_black))
            elif not player_inp in lm: raise ValueError("Invalid Move")
            elif player_inp in lm and not is_castle:
                # White side check rook/king #############################
                if int(player_inp[0]) == 110 or int(player_inp[1]) == 110:
                    self.white[0] = False
                if int(player_inp[0]) == 117 or int(player_inp[1]) == 117:
                    self.white[1] = False
                if int(player_inp[0]) == 114 or int(player_inp[1]) == 114:
                    self.white = [False, False]
                # Black side check rook/king #############################
                if int(player_inp[0]) == 26 or int(player_inp[1]) == 26:
                    self.black[0] = False
                if int(player_inp[0]) == 33 or int(player_inp[1]) == 33:
                    self.black[1] = False
                if int(player_inp[0]) == 30 or int(player_inp[1]) == 30:
                    self.black = [False, False]
                if len(player_inp) == 2:
                    promo = False
                    # if it is en passant 
                    # ((self.board[int(player_inp[0])] == "P" and player) or (self.board[int(player_inp[0])] == "p" and not player))
                    if player:
                        if ([player_inp[1]] in self.gst_black) and self.board[player_inp[0]] == "P":
                            self.board[int(player_inp[1])] = str(self.board[int(player_inp[0])])
                            self.board[int(player_inp[0])] = "."
                            self.move_stack.append((player_inp, self.white, self.black, self.gst_white, self.gst_black))
                            self.board[int(player_inp[1]) + 12] = "."
                            promo = True
                    else:
                        if ([player_inp[1]] in self.gst_white) and self.board[player_inp[0]] == "p":
                            self.board[int(player_inp[1])] = str(self.board[int(player_inp[0])])
                            self.board[int(player_inp[0])] = "."
                            self.move_stack.append((player_inp, self.white, self.black, self.gst_white, self.gst_black))
                            self.board[int(player_inp[1]) - 12] = "."
                            promo = True
                    #self.print_board(self.board)
                    self.gst_white = []; self.gst_black = []
                    
                    # if it is a double move
                    if self.board[int(player_inp[0])].upper() == "P" and abs(int(player_inp[0]) - int(player_inp[1])) == 24:
                        if player:
                            self.gst_white.append([player_inp[0] - 12])
                        else:
                            self.gst_black.append([player_inp[0] + 12])
                    
                    if not promo:
                        self.board[int(player_inp[1])] = str(self.board[int(player_inp[0])])
                        self.board[int(player_inp[0])] = "."
                        self.move_stack.append((player_inp, self.white, self.black, self.gst_white, self.gst_black))
                else:
                    if player_inp[0] == 114:
                        self.white = [False, False]
                    if player_inp[0] == 30:
                        self.black = [False, False]
                    self.gst_white = []; self.gst_black = []
                    self.board[int(player_inp[1])] = str(self.board[int(player_inp[0])])
                    self.board[int(player_inp[0])] = "."
                    self.makeMove(player_inp[2:], [], True, self.player)
                    self.move_stack.append((player_inp, self.white, self.black, self.gst_white, self.gst_black))

    def undo(self):
        self.board = list(
                        "            "
                        "            "
                        "  rnbqkbnr  "
                        "  pppppppp  "
                        "  ........  "
                        "  ........  "
                        "  ........  "
                        "  ........  "
                        "  PPPPPPPP  "
                        "  RNBQKBNR  "
                        "            "
                        "            "
        )
        for i in self.move_stack:
            self.makeMove(i, [i], False, self.player)
        self.move_stack = []

    def twelve_ify(self, move_from, move_to):
        f_col, f_row = move_from % 8, move_from // 8
        t_col, t_row = move_to % 8, move_to // 8
        f_col, t_col, f_row, t_row = f_col + 2, t_col + 2, f_row + 2, t_row + 2
        move_from, move_to = (f_row * 12) + f_col, (t_row * 12) + t_col
        return (move_from, move_to)

    def make_temp_Move(self, player_inp: list, board):
        br = list(board)[:]
        br[int(player_inp[1])] = str(self.board[int(player_inp[0])])
        br[int(player_inp[0])] = "."
        return self.lts(board)

    def lts(self, l: list):
        return "".join(map(str, l))

    def ltt(self, list: list):
        new_tup = tuple()
        for i in list:
            new_tup += (int(i),)
        return new_tup

    def clean(self, board_w_padding: str):
        new_board = ""
        for inx, itm in enumerate(board_w_padding):
            if not inx < 25 or inx > 118 and inx % 12 not in [0, 1, 10, 11]:
                new_board += itm
        return new_board.replace(" ", "")
    