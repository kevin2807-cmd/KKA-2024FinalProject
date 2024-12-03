import pygame
from ChessPiece import *
from Computer import get_random_move, get_ai_move

dark_block = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/square brown dark_png_shadow_128px.png')
light_block = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/square brown light_png_shadow_128px.png')
dark_block = pygame.transform.scale(dark_block, (75, 75))
light_block = pygame.transform.scale(light_block, (75, 75))

whitePawn = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/w_pawn_png_shadow_128px.png')
whitePawn = pygame.transform.scale(whitePawn, (75, 75))
whiteRook = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/w_rook_png_shadow_128px.png')
whiteRook = pygame.transform.scale(whiteRook, (75, 75))
whiteBishop = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/w_bishop_png_shadow_128px.png')
whiteBishop = pygame.transform.scale(whiteBishop, (75, 75))
whiteKnight = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/w_knight_png_shadow_128px.png')
whiteKnight = pygame.transform.scale(whiteKnight, (75, 75))
whiteKing = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/w_king_png_shadow_128px.png')
whiteKing = pygame.transform.scale(whiteKing, (75, 75))
whiteQueen = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/w_queen_png_shadow_128px.png')
whiteQueen = pygame.transform.scale(whiteQueen, (75, 75))

blackPawn = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/b_pawn_png_shadow_128px.png')
blackPawn = pygame.transform.scale(blackPawn, (75, 75))
blackRook = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/b_rook_png_shadow_128px.png')
blackRook = pygame.transform.scale(blackRook, (75, 75))
blackBishop = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/b_bishop_png_shadow_128px.png')
blackBishop = pygame.transform.scale(blackBishop, (75, 75))
blackKnight = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/b_knight_png_shadow_128px.png')
blackKnight = pygame.transform.scale(blackKnight, (75, 75))
blackKing = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/b_king_png_shadow_128px.png')
blackKing = pygame.transform.scale(blackKing, (75, 75))
blackQueen = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/b_queen_png_shadow_128px.png')
blackQueen = pygame.transform.scale(blackQueen, (75, 75))

highlight_block = pygame.image.load('../assets/JohnPablok Cburnett Chess set/128px/highlight_128px.png')
highlight_block = pygame.transform.scale(highlight_block, (75, 75))

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 650
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (150, 250, 150)
TEXT_COLOR = (0, 0, 0)
BUTTON_TEXT = "Q to Morph!"

screen = None
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

def initialize():
    global screen
    pygame.init()
    pygame.display.set_caption('Chess!')
    icon = pygame.image.load('../assets/icon.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))

def draw_button():
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(SCREEN_WIDTH - BUTTON_WIDTH - 20, SCREEN_HEIGHT - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT)
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)

    font_button = pygame.font.SysFont('Arial', 20)
    text = font_button.render(BUTTON_TEXT, True, TEXT_COLOR)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    return button_rect

def draw_background(board):
    
    block_x = 0
    for i in range(4):
        block_y = 0
        for j in range(4):
            screen.blit(light_block, (block_x, block_y))
            screen.blit(dark_block, (block_x + 75, block_y))
            screen.blit(light_block, (block_x + 75, block_y + 75))
            screen.blit(dark_block, (block_x, block_y + 75))
            block_y += 150
        block_x += 150
    step_x = 0
    step_y = pygame.display.get_surface().get_size()[0] - 75
    for i in range(8):
        for j in range(8):
            if isinstance(board[i][j], ChessPiece):
                obj = globals()[f'{board[i][j].color}{board[i][j].type}']
                screen.blit(obj, (step_x, step_y))
            step_x += 75
        step_x = 0
        step_y -= 75
    pygame.display.update()

def draw_text(text):
    s = pygame.Surface((400, 50))
    s.fill((0, 0, 0))
    screen.blit(s, (100, 600))
    text_surface = font.render(text, False, (237, 237, 237))
    if 'DRAW' in text:
        x = 260
    else:
        x = 230
    text_surface_restart = font.render('PRESS "SPACE" TO RESTART', False, (237, 237, 237))
    screen.blit(text_surface, (x, 600))
    screen.blit(text_surface_restart, (150, 620))
    pygame.display.update()

def start(board):
    global screen
    possible_piece_moves = []
    running = True
    visible_moves = False
    dimensions = pygame.display.get_surface().get_size()
    game_over = False
    piece = None
    button_message = ""
    game_over_txt = ""
    transform_pawn = False 

    while running:
        screen.fill((0, 0, 0))
        draw_background(board)

        button_rect = draw_button()

        if button_message:
            message_surface = font.render(button_message, True, (255, 255, 255))
            screen.blit(message_surface, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    transform_pawn = True
                    button_message = ""
                    print(button_message)
                    pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = 7 - event.pos[1] // 75
                y = event.pos[0] // 75

                if not game_over and 0 <= x < 8 and 0 <= y < 8:
                    if transform_pawn:
                        if isinstance(board[x][y], Pawn) and board.get_player_color() == board[x][y].color:
                            pawn = board[x][y]
                            new_rook = Rook(pawn.color, x, y, '\u265C')  
                            board[x][y] = new_rook 
                            board.save_pieces()
                            print(f"Pawn at ({x}, {y}) transformed into a rook.")

                            transform_pawn = False
                            visible_moves = False  
                            possible_piece_moves.clear() 
                            draw_background(board) 

                            if board.ai:
                                get_ai_move(board) 
                                draw_background(board) 

                            if board.white_won():
                                game_over = True
                                game_over_txt = "WHITE WINS!"
                            elif board.black_won():
                                game_over = True
                                game_over_txt = "BLACK WINS!"
                            elif board.draw():
                                game_over = True
                                game_over_txt = "DRAW!"
                        else:
                            button_message = ""
                            print(button_message)

                    else:
                        if isinstance(board[x][y], ChessPiece) and (
                            board.get_player_color() == board[x][y].color or not board.ai
                        ) and (x, y) not in possible_piece_moves:
                            piece = board[x][y]
                            moves = piece.filter_moves(piece.get_moves(board), board)
                            move_positions = []
                            possible_piece_moves = []
                            for move in moves:
                                move_positions.append(
                                    (dimensions[0] - (8 - move[1]) * 75, dimensions[1] - move[0] * 75 - 125)
                                )
                                move_x = 7 - move_positions[-1][1] // 75
                                move_y = move_positions[-1][0] // 75
                                possible_piece_moves.append((move_x, move_y))
                            if visible_moves:
                                draw_background(board)
                                visible_moves = False
                            for move in move_positions:
                                visible_moves = True
                                screen.blit(highlight_block, (move[0], move[1]))
                                pygame.display.update()
                        else:
                            clicked_move = (x, y)
                            try:
                                if clicked_move in possible_piece_moves:
                                    board.make_move(piece, x, y)
                                    possible_piece_moves.clear()
                                    draw_background(board)
                                    if board.ai:
                                        get_ai_move(board)
                                        draw_background(board)

                                    if board.white_won():
                                        game_over = True
                                        game_over_txt = "WHITE WINS!"
                                    elif board.black_won():
                                        game_over = True
                                        game_over_txt = "BLACK WINS!"
                                    elif board.draw():
                                        game_over = True
                                        game_over_txt = "DRAW!"
                            except UnboundLocalError:
                                pass

        if game_over:
            draw_text(game_over_txt)
