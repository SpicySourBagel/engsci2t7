def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)

def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    y_start = y_end - d_y * (length - 1)
    x_start = x_end - d_x * (length - 1)
    col = board[y_end][x_end]
    start_type = ""
    end_type = ""

    # test the value after the end square
    if y_end + d_y < 0 or y_end + d_y >= len(board) or x_end + d_x < 0 or x_end + d_x >= len(board[0]):  # first tests if it is in the board
        end_type = "edge"
    else:  # means in board, need this otherwise might be an index error
        end_type = board[y_end + d_y][x_end + d_x]

    # test the value before the start square
    if y_start - d_y < 0 or y_start - d_y >= len(board) or x_start - d_x < 0 or x_start - d_x >= len(board[0]):
        start_type = "edge"
    else:
        start_type = board[y_start - d_y][x_start - d_x]

    if start_type == col or end_type == col:  # test if sequence is complete or not
        return None
    
    if start_type == " " and end_type == " ":
        return "OPEN"
    elif start_type == " " or end_type == " ":  # can do this cause scenario with both is tested before this
        return "SEMIOPEN"
    else:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    y = y_start
    x = x_start
    seq_len = 0
    
    while 0 <= y < len(board) and 0 <= x < len(board[0]):
        if board[y][x] == col:
            seq_len += 1
            if seq_len == length:
                    if is_bounded(board, y, x, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y, x, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
        else:
            seq_len = 0  # means that it is not connected
        y += d_y
        x += d_x  # next element in row R

    return (open_seq_count, semi_open_seq_count)

def detect_rows(board, col, length):
    '''since there are only 4 possible directions on the board, they are set as the cases and then tested'''
    open_seq_count, semi_open_seq_count = 0, 0

    # up/down
    for i in range(len(board)):
        res_1 = detect_row(board, col, 0 , i, length, 1, 0)
        open_seq_count += res_1[0]
        semi_open_seq_count += res_1[1]
    
    # side/side
    for i in range(len(board)):
        res_2 = detect_row(board, col, i , 0, length, 0, 1)
        open_seq_count += res_2[0]
        semi_open_seq_count += res_2[1]

    # top left to bottom right
    for i in range(len(board[0])):
        res_3 = detect_row(board, col, 0 , i, length, 1, 1)
        open_seq_count += res_3[0]
        semi_open_seq_count += res_3[1]
    for k in range(1, len(board)):
        res_4 = detect_row(board, col, k, 0, length, 1, 1)
        open_seq_count += res_4[0]
        semi_open_seq_count += res_4[1]

    # bottom left to top right
    for i in range(len(board[0])):
        res_5 = detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += res_5[0]
        semi_open_seq_count += res_5[1]
    for k in range(1, len(board)):
        res_6 = detect_row(board, col, k, len(board[0]) - 1, length, 1, -1)
        open_seq_count += res_6[0]
        semi_open_seq_count += res_6[1]

    return (open_seq_count, semi_open_seq_count)

def search_max(board):
    max_score = score(board)
    move_y = 0
    move_x = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                board[y][x] = "b"
                if score(board) > max_score:
                    max_score = score(board)
                    move_y = y
                    move_x = x
                board[y][x] = " "
            else:
                continue
                
    return (move_y, move_x)

def is_win(board):
    if better_detect_rows(board, "w", 5)[0] > 0 or better_detect_rows(board, "w", 5)[1] > 0 or better_detect_rows(board, "w", 5)[2] > 0:
        return "White won"
    elif better_detect_rows(board, "b", 5)[0] > 0 or better_detect_rows(board, "b", 5)[1] > 0 or better_detect_rows(board, "b", 5)[2] > 0:
        return "Black won"
    elif better_detect_rows(board, "w", 5)[0] == 0 and better_detect_rows(board, "w", 5)[1] == 0 and better_detect_rows(board, "w", 5)[2] == 0\
    and better_detect_rows(board, "b", 5)[0] == 0 and better_detect_rows(board, "b", 5)[1] == 0 and better_detect_rows(board, "b", 5)[2] == 0 and is_full(board) == True:
        return "Draw"
    else:
        return "Continue playing"

# helper functions:

def better_detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    y = y_start
    x = x_start
    seq_len = 0
    
    while 0 <= y < len(board) and 0 <= x < len(board[0]):
        if board[y][x] == col:
            seq_len += 1
            if seq_len == length:
                    if is_bounded(board, y, x, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y, x, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                    else:  
                        closed_seq_count += 1  # has to be closed
        else:
            seq_len = 0  # means that it is not connected
        y += d_y
        x += d_x  # next element in row R

    return (open_seq_count, semi_open_seq_count, closed_seq_count)

def better_detect_rows(board, col, length):
    '''also returns the closed ones, and returns everything in a list'''
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0

    # up/down
    for i in range(len(board)):
        res_1 = better_detect_row(board, col, 0 , i, length, 1, 0)
        open_seq_count += res_1[0]
        semi_open_seq_count += res_1[1]
        closed_seq_count += res_1[2]
    
    # side/side
    for i in range(len(board)):
        res_2 = better_detect_row(board, col, i , 0, length, 0, 1)
        open_seq_count += res_2[0]
        semi_open_seq_count += res_2[1]
        closed_seq_count += res_2[2]

    # top left to bottom right
    for i in range(len(board[0])):
        res_3 = better_detect_row(board, col, 0 , i, length, 1, 1)
        open_seq_count += res_3[0]
        semi_open_seq_count += res_3[1]
        closed_seq_count += res_3[2]
    for k in range(1, len(board)):
        res_4 = better_detect_row(board, col, k, 0, length, 1, 1)
        open_seq_count += res_4[0]
        semi_open_seq_count += res_4[1]
        closed_seq_count += res_4[2]

    # bottom left to top right
    for i in range(len(board[0])):
        res_5 = better_detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += res_5[0]
        semi_open_seq_count += res_5[1]
        closed_seq_count += res_5[2]
    for k in range(1, len(board)):
        res_6 = better_detect_row(board, col, k, len(board[0]) - 1, length, 1, -1)
        open_seq_count += res_6[0]
        semi_open_seq_count += res_6[1]
        closed_seq_count += res_6[2]

    return [open_seq_count, semi_open_seq_count, closed_seq_count]

def is_full(board):
    '''returns True/False for if the board has any empty squares in it'''
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                return False
    return True

if __name__ == '__main__':
    play_gomoku(8)