init python:

    EMPTY = 0
    P1_RING = 1
    P2_RING = 2
    P1_MARK = 3
    P2_MARK = 4

    BOARD_RADIUS = 4

    def valid_cell(q, r):
        return abs(q) <= BOARD_RADIUS and abs(r) <= BOARD_RADIUS and abs(q + r) <= BOARD_RADIUS

    board = {}
    current_player = P1_RING
    selected_ring = None
    
init python:
    import math

    HEX_SIZE = 60
    CENTER_X = 960
    CENTER_Y = 540

    def hex_to_pixel(q, r):
        x = HEX_SIZE * (3/2 * q)
        y = HEX_SIZE * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
        return int(CENTER_X + x), int(CENTER_Y + y)
#Сброс поля
init python:

    def reset_board():
        global board, current_player, selected_ring

        board = {}
        for q in range(-BOARD_RADIUS, BOARD_RADIUS+1):
            for r in range(-BOARD_RADIUS, BOARD_RADIUS+1):
                if valid_cell(q, r):
                    board[(q, r)] = EMPTY

        current_player = P1_RING
        selected_ring = None

#Движение+Логика
init python:

    DIRECTIONS = [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]

    def get_path(sq, sr, tq, tr):
        dq = tq - sq
        dr = tr - sr

        if dq != 0:
            dq = dq // abs(dq)
        if dr != 0:
            dr = dr // abs(dr)

        path = []
        cq, cr = sq + dq, sr + dr

        while (cq, cr) in board:
            path.append((cq, cr))
            if (cq, cr) == (tq, tr):
                return path
            cq += dq
            cr += dr

        return None


    def flip_markers(path):
        for (q, r) in path:
            if board[(q, r)] == P1_MARK:
                board[(q, r)] = P2_MARK
            elif board[(q, r)] == P2_MARK:
                board[(q, r)] = P1_MARK


    def select_ring(q, r):
        global selected_ring
        if board[(q, r)] == current_player:
            selected_ring = (q, r)


    def move_ring(q, r):
        global selected_ring, current_player

        if not selected_ring:
            return

        sq, sr = selected_ring
        path = get_path(sq, sr, q, r)

        if not path:
            return

        board[(sq, sr)] = P1_MARK if current_player == P1_RING else P2_MARK

        flip_markers(path)

        board[(q, r)] = current_player

        selected_ring = None

        current_player = P2_RING if current_player == P1_RING else P1_RING

#Проверка линий
init python:

    def check_lines(player_mark):
        for (q, r) in board:
            for dq, dr in DIRECTIONS:
                count = 0
                for i in range(5):
                    pos = (q + dq*i, r + dr*i)
                    if pos in board and board[pos] == player_mark:
                        count += 1
                    else:
                        break

                if count == 5:
                    return True

        return False

screen yinsh():

    add "yinsh_board_hex"

    for (q, r) in board:

        $ x, y = hex_to_pixel(q, r)

        if board[(q, r)] == P1_RING:
            add "ring_p1_style" xpos x ypos y anchor (0.5, 0.5)

        elif board[(q, r)] == P2_RING:
            add "ring_p2_style" xpos x ypos y anchor (0.5, 0.5)

        elif board[(q, r)] == P1_MARK:
            add "marker_p1_style" xpos x ypos y anchor (0.5, 0.5)

        elif board[(q, r)] == P2_MARK:
            add "marker_p2_style" xpos x ypos y anchor (0.5, 0.5)

        else:

            imagebutton:
                idle Solid("#00000000")
                hover Solid("#ffffff22")
                action Function(handle_click, q, r)

                xpos x
                ypos y
                anchor (0.5, 0.5)
                xysize (100, 100)
init python:

    def handle_click(q, r):

        if selected_ring:
            move_ring(q, r)

            if check_lines(P1_MARK):
                renpy.say(None, "Игрок 1 собрал линию!")

            elif check_lines(P2_MARK):
                renpy.say(None, "Игрок 2 собрал линию!")

        else:
            select_ring(q, r)

label play_yinsh:

    $ reset_board()

    call screen yinsh

    return