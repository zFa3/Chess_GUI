#!/usr/bin/env python

# zFa3 - ChessGUI in Python(Tkinter)
import tkinter as tk
from Chess_Framework import *
import random


FEN = ("None")
SIDE_LEN = 600
COVER = 235
END_TIME = 100 # in ms but tkinter is slow so its sometimes longer
LINE_WID = 1
PERFT = False
DEPTH = 3
Counter = 0
# [highlight color] [select color] [legal moves] [check color] [Dark sq color] [Light sq Color]
ALL_THEMES = [
            ["blue", "green", "orange", "red", "gray", "white"], # DEFAULT
            ["black", "brown", "grey", "gold", "gray", "white"], # GREY RED
            ["#59E03D", "#3DE0CD", "#3DE15E", "#9DE03D", "gray", "white"], # LIGHT BLUE GREEN
            ["#B89AE3", "#E39ADB", "#E39AAF", "#A09AE3", "gray", "white"], # PURPLE TINT
            ["#E68373", "#E6AB73", "#E69772", "#E67380", "gray", "white"], # PEACH FRUIT
            ["#47E6DD", "#4789E6", "#48BBE6", "#47E6A7", "gray", "white"], # OCEAN WATER
            ["#E67F30", "#E6B330", "#E59D31", "#E65F30", "gray", "white"], # AUTUMN COLORS
            ["#85B2E6", "#85D0E6", "#84E5DC", "#85E69A", "gray", "white"] # AQUARIUM BLUE
]
COLORS = ALL_THEMES[0]

UNICODE_PIECES = {
    "K":"♔",
    "Q":"♕",
    "R":"♖",
    "B":"♗",
    "N":"♘",
    "P":"♙",
    "k":"♚",
    "q":"♛",
    "r":"♜",
    "b":"♝",
    "n":"♞",
    "p":"♟",
    ".":" "
}

GRID = 8

def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)

def main():
    root = tk.Tk()
    #Pawn = tk.PhotoImage(file="Pawn.PNG")
    height, width = root.winfo_screenheight(), root.winfo_screenwidth()
    root.title("Main Menu")
    root.geometry(f"{SIDE_LEN}x{SIDE_LEN}+{(width - SIDE_LEN)//2}+{(height - SIDE_LEN)//2}")
    root.resizable(False, False)
    R1 = tk.IntVar(root)
    G1 = tk.IntVar(root)
    B1 = tk.IntVar(root)

    R2 = tk.IntVar(root)
    G2 = tk.IntVar(root)
    B2 = tk.IntVar(root)

    R3 = tk.IntVar(root)
    G3 = tk.IntVar(root)
    B3 = tk.IntVar(root)

    def custom_theme():

        def a(_):
            global COLORS
            tk.Label(theme_cutomizer, width=25, height=7, background = rgb_to_hex(int(R1.get() * 2.55), int(G1.get() * 2.55), int(B1.get() * 2.55))).place(x = 400, y = 25)
            tk.Label(theme_cutomizer, width=25, height=7, background = rgb_to_hex(int(R2.get() * 2.55), int(G2.get() * 2.55), int(B2.get() * 2.55))).place(x = 400, y = 160)
            tk.Label(theme_cutomizer, width=25, height=7, background = rgb_to_hex(int(R3.get() * 2.55), int(G3.get() * 2.55), int(B3.get() * 2.55))).place(x = 400, y = 300)
            
            tk.Label(theme_cutomizer, width=25, height=3, background = rgb_to_hex(abs(int(R1.get() * 2.55) - 255), abs(int(G1.get() * 2.55) - 255), abs(int(B1.get() * 2.55) - 255))).place(x = 400, y = 105)
            tk.Label(theme_cutomizer, width=25, height=3, background = rgb_to_hex(abs(int(R2.get() * 2.55) - 255), abs(int(G2.get() * 2.55) - 255), abs(int(B2.get() * 2.55) - 255))).place(x = 400, y = 245)
            tk.Label(theme_cutomizer, width=25, height=3, background = rgb_to_hex(abs(int(R3.get() * 2.55) - 255), abs(int(G3.get() * 2.55) - 255), abs(int(B3.get() * 2.55) - 255))).place(x = 400, y = 385)
            
            COLORS = []
            COLORS.append(rgb_to_hex(int(R1.get() * 2.55), int(G1.get() * 2.55), int(B1.get() * 2.55)))
            COLORS.append(rgb_to_hex(int(R2.get() * 2.55), int(G2.get() * 2.55), int(B2.get() * 2.55)))
            COLORS.append(rgb_to_hex(int(R3.get() * 2.55), int(G3.get() * 2.55), int(B3.get() * 2.55)))

            COLORS.append(rgb_to_hex(abs(int(R1.get() * 2.55) - 255), abs(int(G1.get() * 2.55) - 255), abs(int(B1.get() * 2.55) - 255)))
            COLORS.append(rgb_to_hex(abs(int(R2.get() * 2.55) - 255), abs(int(G2.get() * 2.55) - 255), abs(int(B2.get() * 2.55) - 255)))
            COLORS.append(rgb_to_hex(abs(int(R3.get() * 2.55) - 255), abs(int(G3.get() * 2.55) - 255), abs(int(B3.get() * 2.55) - 255)))

        theme_cutomizer = tk.Toplevel(root, bg = "black")
        theme_cutomizer.title("Theme Customizer")
        theme_cutomizer.geometry(f"{SIDE_LEN}x{SIDE_LEN}+{(width - SIDE_LEN)//2}+{(height - SIDE_LEN)//2}")
        theme_cutomizer.resizable(False, False)

        a(0)

        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=R1).place(x = 151, y = 25)
        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=G1).place(x = 201, y = 25)
        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=B1).place(x = 251, y = 25)

        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=R2).place(x = 151, y = 175)
        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=G2).place(x = 201, y = 175)
        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=B2).place(x = 251, y = 175)
        
        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=R3).place(x = 151, y = 335)
        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=G3).place(x = 201, y = 335)
        tk.Scale(theme_cutomizer, bigincrement=0.2, width=15, length=100, variable=B3).place(x = 251, y = 335)        

        tk.Button(theme_cutomizer, text="DONE", width=35, height=3, bg="white", relief="solid", command=theme_cutomizer.destroy).place(x = 150, y = 485)
        theme_cutomizer.bind("<ButtonRelease-1>", a)

    def Game():
        global click_indexes
        board = Board(FEN)
        Game_Window = tk.Toplevel(root)
        Game_Window.geometry(f"{SIDE_LEN}x{SIDE_LEN}+{(width - SIDE_LEN)//2}+{(height - SIDE_LEN)//2}")
        Game_Window.title("Chess")
        game_canvas = tk.Canvas(Game_Window, width=SIDE_LEN, height=SIDE_LEN)
        game_canvas.pack()
        def tts(tup: tuple):
            return " ".join(tuple(map(str, tup)))
        click_indexes = []

        def resize(_):
            global SIDE_LEN
            SIDE_LEN = min(Game_Window.winfo_width(), Game_Window.winfo_height())
            draw()

        def click(event):
            global click_indexes, COVER, Counter
            Counter += 1
            col = event.x//(SIDE_LEN//GRID)
            row = event.y//(SIDE_LEN//GRID)
            index = (col + row * GRID)
            click_indexes.append(index)
            try:
                if len(click_indexes) > 1:
                    f_ind, t_ind = click_indexes[-2], click_indexes[-1]
                    f, t = board.twelve_ify(f_ind, t_ind)
                    for i in (board.legal_moves(board.player, board.board, True, False)):
                        if i[:2] == (f, t):
                            if len(i) == 3:
                                move = tts(i[:2])
                            else:
                                move = tts(i)
                    promotion = ""
                    if str(board.board[f]).upper() == "P":
                        if board.player and t_ind < 8:
                            promotion += input()
                            if not promotion in "RBNQ":
                                raise ValueError
                        elif not board.player and t_ind > 55:
                            promotion += input()
                            if not promotion in "rnbq":
                                raise ValueError
                        else:
                            pass
                    
                    if (f_ind, t_ind) in board.cleaned_moves():
                        game_canvas.delete("all")
                        board.play_move(f"{move} {promotion}")
                        if board.is_mate() == 1 or board.is_mate() == 2:
                            try:
                                COVER = 235
                                for i in range(COVER):
                                    Game_Window.after(END_TIME//COVER)
                                    highlight_spot(random.randint(0, 64), False, ("#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
                                    game_canvas.update()
                            finally:
                                Game_Window.destroy()
                        click_indexes = []
                        try:
                            draw()
                        finally:
                            return
                draw()
                if not board.is_check():
                    highlight_spot(index, True, COLORS[1])
                for i in board.cleaned_moves():
                    if i[0] == index:
                        highlight_spot(i[1], True, COLORS[2])
            except ValueError: draw()
            if board.is_mate() == 1 or board.is_mate() == 2:
                COVER = 235
                try:
                    for i in range(COVER):
                        Game_Window.after(END_TIME//COVER)
                        highlight_spot(random.randint(0, 64), False, ("#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
                        game_canvas.update()
                except: pass
                Game_Window.destroy()
        
        def highlight_spot(index: int, light: bool, color):
            try:
                row, col = index % 8, index // 8
                x, y = row * (SIDE_LEN//GRID), col * (SIDE_LEN//GRID)
                if not light:
                    game_canvas.create_rectangle(x, y, x + (SIDE_LEN//GRID), y + (SIDE_LEN//GRID), fill = color)
                else:
                    game_canvas.create_rectangle(x, y, x + (SIDE_LEN//GRID), y + (SIDE_LEN//GRID), fill = color, stipple='gray75')
            except Exception as Error: pass

        def change_theme(event):
            global COLORS
            COLORS = ALL_THEMES[random.randint(0, len(ALL_THEMES) - 1)]
            draw()
            for ind, itm in enumerate(COLORS):
                highlight_spot(ind, True, itm)
        
        def show_theme(event):
            draw()
            for ind, itm in enumerate(COLORS):
                highlight_spot(ind, False, itm)
        
        def rand_theme(event):
            global COLORS
            COLORS = [("#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) for i in range(6)]
            draw()
            for ind, itm in enumerate(COLORS):
                highlight_spot(ind, True, itm)

        def draw():
            global Counter
            #game_canvas.config(width=SIDE_LEN, height=SIDE_LEN)
            # clear the board every 50 clicks, to prevent strobing
            # as well as lag due to layers
            if Counter == 50:
                Counter = 0
                game_canvas.delete("all")
            try:
                # make the pattern first (so its in the back)
                for index, item in enumerate(board.clean(board.board)):
                    if ((index % 8) + (index // 8)) % 2 == 1:
                        highlight_spot(index, False, COLORS[4])
                    else:
                        highlight_spot(index, False, COLORS[5])
                # creates the vertical lines
                for line in range(GRID - 1):
                    # iterates creating the vertical lines
                    game_canvas.create_line((SIDE_LEN//GRID) * (line + 1), 0, (SIDE_LEN//GRID) * (line + 1), SIDE_LEN, width = LINE_WID)
                # create the horizontal lines
                for line in range(GRID - 1):
                    game_canvas.create_line(0, (SIDE_LEN//GRID) * (line + 1), SIDE_LEN, (SIDE_LEN//GRID) * (line + 1), width = LINE_WID)
                if board.is_check():
                    if board.player:
                        highlight_spot((board.clean(board.board)).index("K"), False, "red")
                    else:
                        highlight_spot((board.clean(board.board)).index("k"), False, "red")
                # create the pieces last
                for index, item in enumerate(board.clean(board.board)):
                    ind_row, ind_col = index // 8, index % 8
                    game_canvas.create_text(ind_col * (SIDE_LEN//GRID) + (SIDE_LEN//GRID)//2, ind_row * (SIDE_LEN//GRID) + (SIDE_LEN//GRID)//2, text = UNICODE_PIECES[item], font = ("FreeSerif", SIDE_LEN//12))
            except: pass
            game_canvas.update()

        def right_click(event):
            col = event.x//(SIDE_LEN//GRID)
            row = event.y//(SIDE_LEN//GRID)
            index = (col + row * GRID)
            highlight_spot(index, True, COLORS[0])

        def undo(event):
            if len(board.move_stack) > 1:
                board.board = list(
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
                a = board.move_stack[:-2]
                board.move_stack = []
                for i in a:
                    board.makeMove(i[0], [i[0]], False, board.player)
                    board.white = i[1]
                    board.black = i[2]
                    board.gst_white = i[3]
                    board.gst_black = i[4]
            draw()

        Game_Window.bind("u", undo)
        Game_Window.bind("s", show_theme)
        Game_Window.bind("r", rand_theme)
        Game_Window.bind("t", change_theme)
        Game_Window.bind("<Button-1>", click)
        Game_Window.bind("<Button-2>", right_click)
        Game_Window.bind("<Button-3>", right_click)
        Game_Window.bind("<Configure>", resize)
        draw()
        Game_Window.mainloop()
        #Game()
    
    bg_image = tk.PhotoImage(file = "Pawn.PNG")
    tk.Label(master = root, image = bg_image, width=SIDE_LEN, height=SIDE_LEN).place(x = 0, y = 0)
    Play_Button = tk.Button(root, width=20, height=2, text = "PLAY", background="black", foreground="white", command=Game)
    Play_Button.place(x = 225, y = 275)
    Theme_Button = tk.Button(root, width=20, height=2, text = "THEME", background="black", foreground="white", command=custom_theme)
    Theme_Button.place(x = 225, y = 325)
    root.mainloop()

def perft(depth: int, position: Board, player: bool, a: bool):
    # this is the perft test which stands for PERF ormance T est
    # and it does two things
    # it is commonly used to determine twhether move generation is fast
    # and its also used to make sure all the legal moves of chess have 
    # been accounted for. As an example, the positions that have been 
    # commented out near the top of the program may have perft results
    # next to them, indicating the number of positions searched 
    global nodes, move_nodes
    # You could also add a time.perf_counter() into this code and measure
    # how long perft takes at each depth, but Im not measuring the speed, 
    # just the accuracy
    if depth == 0:
        nodes += 1
        move_nodes += 1
        return
    br = position.board[:]
    moves = position.legal_moves(player, position.board, True, False)
    for i in moves:
        position.makeMove(i, [i], False, player)
        perft(depth - 1, position, bool(not player), False)
        position.board = br[:]
        if a:
            #print(x.clean_moves(i), nodes, move_nodes)
            move_nodes = 0
        else:
            #print("\t", x.clean_moves(i), nodes, move_nodes)
            pass

if __name__ == "__main__":
    if PERFT:
        nodes = 0
        move_nodes = 0
        x = Board(FEN)
        x.print_board(x.board)
        #print(x.player)
        # --> perft (Depth, Position, Empty List, Player)
        perft(DEPTH, x, x.player, True)
        print("total nodes", nodes)
    main()
