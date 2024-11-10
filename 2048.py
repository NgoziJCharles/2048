import random


def print_board(game_board: [[int, ], ]) -> None:
    """
    Print a formatted version of the game board.
    :param game_board: a 4x4 2D list of integers representing a game of 2048
    """
    for row in game_board:
        print("+----+" * 4)
        print(''.join(f"|{cell if cell else '':^4}|" for cell in row))
        print("+----+" * 4)


def generate_piece(game_board: [[int, ], ], user_input=False) -> {str: int, }:
    """
    Generates a value and coordinates for the next number to be placed on the board.
    Will raise error if the provided board is full.
    :param game_board: a 4x4 2D list of integers representing a game of 2048
    :param user_input: specifies type of piece generation: random or user-specified
    :return: dictionary with the following keys: {'row': int, 'column': int, 'value': int}
    """
    empty_cells = [(y, x) for y, row in enumerate(game_board) for x, cell in enumerate(row) if not cell]
    if not empty_cells:
        raise Exception("Board Full")
    if user_input:
        return dict(zip(('column', 'row',  'value'), (int(i) for i in input("column,row,value:").split(','))))
    return dict(
        zip(('row', 'column', 'value'), (*random.choice(empty_cells), (2 if random.random() * 100 < 90 else 4))))





# from utilities import generate_piece, print_board

DEV_MODE = False

def checking_for_win(game_board):
    target_count = 0
    for row in range(0, len(game_board)):
        for i in range(0, len(game_board[row])):
            if game_board[row][i] == 2048:
                target_count += 1
    if target_count != 0:
        print("You Win!")
        return True
    return False
    
def main(game_board: [[int, ], ]) -> [[int, ], ]:
    """
    2048 main function, runs a game of 2048 in the console.

    Uses the following keys:
    w - shift up
    a - shift left
    s - shift down
    d - shift right
    q - ends the game and returns control of the console
    :param game_board: a 4x4 2D list of integers representing a game of 2048
    :return: returns the ending game board
    """
    # Initialize board's first cell
    dict = generate_piece(game_board) #assigns a row, column, value specifically
    
    # TODO: generate a random piece and location using the generate_piece function    
    # TODO: place the piece at the specified location
    game_board[dict['row']][dict['column']] = dict['value']
    
    is_game_going = True
    while(is_game_going):
        new_piece = generate_piece(game_board)
        game_board[new_piece['row']][new_piece['column']] = new_piece['value']

        print_board(game_board)
        
        if checking_for_win(game_board) == True:
            print("You Win!")
            break
        
        if game_over(game_board) == True:
            print("You Lost.")
            break
        
        user_input = input("Enter a key: ")
        movement(game_board, user_input)
        
        if user_input == 'q':
            print('Goodbye')
            break
        
        
        # elif user_input != 'w' or user_input != 'a' or user_input != 's' or user_input != 'd':
        #     print('enter a vlid move:')
        #     continue #stop the board from producing 
        # is_game_going = game_over(game_board)
    return game_board
    
def changing_row_w_a(array): #left and up
    mini_array = []
    for index,value in enumerate(array):
        if value != 0:
            mini_array.append(value)
    another_array = []
    if len(mini_array) % 2 == 0:
        for i in range(0,(len(mini_array) - 1),2):
            if mini_array[i] == mini_array[i + 1]:
                another_array.append(mini_array[i] + mini_array[i + 1])
            else:
                another_array.append(mini_array[i])
                another_array.append(mini_array[i + 1])
    elif len(mini_array) == 1:
        another_array = mini_array
    elif len(mini_array) == 3:
        if mini_array[0] == mini_array[1]:
            another_array.append(mini_array[0]+mini_array[1])
            another_array.append(mini_array[2])
        elif mini_array[1] == mini_array[2] and mini_array[0] != mini_array[1]:
            another_array.append(mini_array[0])
            another_array.append(mini_array[1]+mini_array[2])
        else:
            another_array = mini_array
            
    while len(another_array) < 4:
        another_array.append(0)
    return another_array
    
def changing_row_s_d(array): #right and down
    mini_array = []
    for index,value in enumerate(array):
        if value != 0:
            mini_array.append(value)
    another_array = []
    if len(mini_array) % 2 == 0:
        for i in range(0,(len(mini_array) - 1),2):
            if mini_array[i] == mini_array[i + 1]:
                another_array.append(mini_array[i] + mini_array[i + 1])
            else:
                another_array.append(mini_array[i])
                another_array.append(mini_array[i + 1])
    elif len(mini_array) == 1:
        another_array = mini_array
    elif len(mini_array) == 3:
        if mini_array[2] == mini_array[1]:
            another_array.append(mini_array[0])
            another_array.append(mini_array[2]+mini_array[1])
        elif mini_array[1] == mini_array[0] and mini_array[2] != mini_array[1]:
            another_array.append(mini_array[1]+mini_array[0])
            another_array.append(mini_array[2])
        else:
            another_array = mini_array
            
    while len(another_array) < 4:
        another_array = [0] + another_array 
    return another_array
  
def movement(game_board, user_input): #generates multiple pieces instead of just one piece?
    if user_input.lower() == 'w':
        for index in range(len(game_board)):
            values = [row[index] for row in game_board]
            new_col = changing_row_w_a(values)
            for i, row in enumerate(game_board):
                row[index] = new_col[i]
        # print(changing_row_w_a([8, 2, 4, 4]))
       
    if user_input.lower() == 'a':
        for index, row in enumerate(game_board):
            new_row = changing_row_w_a(row)
            game_board[index] = new_row
        # print(changing_row_w_a([8, 2, 4, 4])) # --- [8, 8, 4, 0]
    
    if user_input.lower() == 's':
        for index in range(len(game_board)):
            values = [row[index] for row in game_board]
            new_col = changing_row_s_d(values)
            for i, row in enumerate(game_board):
                row[index] = new_col[i]
        # print(changing_row_w_a([8, 2, 4, 4]))
            
    if user_input.lower() == 'd':
        for index, row in enumerate(game_board):
            new_row = changing_row_s_d(row)
            game_board[index] = new_row
        # print(changing_row_w_a([8, 2, 4, 4]))
     


    # Game Loop

        # TODO: UPDATE/ADD PIECE TO BOARD
        # place a random piece on the board
        # check to see if the game is over using the game_over function

        # TODO: Show updated board using the print_board function

        # TODO: GET AND EXECUTE USER MOVE
        # Take input until the user's move is a valid key
        # if the user quits the game, print Goodbye and stop the Game Loop
        # User's Move Loop:
            # Execute the user's move
            # Compare board before user's move & after user's move
                # get and execute another move if board has not changed

        # Check if the user wins
    return game_board
    


def game_over(game_board: [[int, ], ]) -> bool:
    """
    Query the provided board's game state.

    :param game_board: a 4x4 2D list of integers representing a game of 2048
    :return: Boolean indicating if the game is over (True) or not (False)
    """
    is_full = True

    for row in range(0, len(game_board)):
        for i in range(0, len(game_board[row])):
            if game_board[row][i] == 0:
                is_full = False
                break
    is_over = True
    if is_full:
        for index, row in enumerate(game_board):
            if 0 in changing_row_s_d(row) or 0 in changing_row_w_a(row):
                print(row)
                is_over = False
                break
            values = [row[index] for row in game_board]
            if 0 in changing_row_s_d(row) or 0 in changing_row_w_a(row):
                print("Column:", values)
                print("New Column:", changing_row_s_d(values), changing_row_w_a(values))                
                is_over = False
                break
    else:
        is_over = False

    return is_over
                    
                    
                    #continue with the game but do not generate a random piece
                    #check column
    # for index in range(len(game_board)):
    #     for i, row in enumerate(game_board):

    # TODO: Loop over the board and determine if the game is over



if __name__ == "__main__":
    main([[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]])

