import sys
from utils import parseTestCase
from board import Board

def main():
    """
    Main function to read terminal input
    """

    player = ["lower", "UPPER"]
    curr, alt = 0, 1
    moves_made = 0
    end = 0
    end_type = 0
    f_flag = 0
    
    if sys.argv[1] == '-f':
        f_flag = 1
        board = Board()
        test_input = parseTestCase(sys.argv[2])
        board._placePieces(test_input['initialPieces'])
        board.UPPER_captures = test_input['upperCaptures']
        board.lower_captures = test_input['lowerCaptures']
        for move in test_input['moves']:
            print(move)
            print(board)
            check = 0
            check_moves = []
            upper_caps, lower_caps = board._getCapturedPieces()
            test_move = move.strip().split(" ")
            
            #check if maximum number of moves have been made
            if moves_made >= 400:
                end = 1
                end_type = 0               
                break
            
            #see if player is in check
            if board._checkDetection(player[curr]):
                check = 1
                check_moves = board._possibleCheckMoves(player[curr])
                if len(check_moves) > 0:
                    print(str(player[curr]) + " is in check!")
                else:
                    end = 1
                    end_type = 1
                    break
                
            if test_move[0] == "move":
                if len(test_move) == 3:
                    board._move(test_move[1], test_move[2], player[curr], 0)
                elif len(test_move) == 4:
                    board._move(test_move[1], test_move[2], 1)
            elif test_move[0] == "drop":
                board._drop(test_move[1], test_move[2], player[curr])
            
            elif test_move[0] == "drop":
                board._drop(test_move[1], test_move[2], player[curr])
            #check if input does not include "move" or "drop"
            else:
                end = 1
                end_type = 2
                break
            #check if an illegal move was performed or if the player put themselves into check
            if not board._checkLegality() or board._checkDetection(player[curr]):
                end = 1
                end_type = 2
                break            
            #switch current player
            temp = curr
            curr = alt
            alt = temp
            moves_made += 1
            
        print(board)
        print("")
        upper_caps, lower_caps = board._getCapturedPieces()
        print("Captures UPPER: " + str(upper_caps))
        print("Captures lower: " + str(lower_caps))
        print("")
        if end == 1:
            if end_type == 0:
                print("Tie game. Too many moves.")
                return
            elif end_type == 1:
                print("%s wins. Checkmate." % player[alt])
                return
            elif end_type == 2:
                print(str(player[alt]) + " player wins. Illegal move.")
                return

    if sys.argv[1] == '-i':
        board = Board._initDefaultBoard()
        
    while True:
        check = 0
        check_moves = []
        
        if f_flag == 0:
            print(board)
            print("")
            upper_caps, lower_caps = board._getCapturedPieces()
            print("Captures UPPER: " + str(upper_caps))
            print("Captures lower: " + str(lower_caps))
            print("")
        
        #check if maximum number of moves have been made
        if moves_made >= 400:
            print("Tie game. Too many moves.")
            return
        
        #see if player is in check
        if board._checkDetection(player[curr]):
            check = 1
            check_moves = board._possibleCheckMoves(player[curr])
            if len(check_moves) > 0:
                print(str(player[curr]) + " is in check!")
                print("Available moves: ")
                for m in check_moves:
                    print(m)
            else:
                print("%s wins. Checkmate." % player[alt])
                return
        player_str = input(str(player[curr]) + "> ")
        player_move = player_str.strip().split(" ")
        if check == 1 and player_str not in check_moves:
            print(str(player[alt]) + " player wins. Illegal move.")
            return
        if player_move[0] == "move":
            if len(player_move) == 3:
                board._move(player_move[1], player_move[2], player[curr], 0)
            elif len(player_move) == 4:
                board._move(player_move[1], player_move[2], 1)
        elif player_move[0] == "drop":
            board._drop(player_move[1], player_move[2], player[curr])
        #check if input does not include "move" or "drop"
        else:
            print(str(player[alt]) + " player wins. Illegal move.")
            return
        #check if an illegal move was performed or if the player put themselves into check
        if not board._checkLegality() or board._checkDetection(player[curr]):
            print(str(player[alt]) + " player wins. Illegal move.")
            return            
        #switch current player
        temp = curr
        curr = alt
        alt = temp
        moves_made += 1
        f_flag = 0
    
if __name__ == "__main__":
    main()
