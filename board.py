import os
from piece import Piece

class Board:
    """
    Class that represents the BoxShogi board
    """

    # The BoxShogi board is 5x5
    BOARD_SIZE = 5
    let_num = {"a":0, "b":1, "c":2, "d":3, "e":4}
    UPPER_captures = []
    UPPER_pieces = []
    lower_captures = []
    lower_pieces = []
    ILLEGAL_FLAG = 0

    def __init__(self):
        self._board = self._initEmptyBoard()

    def _initDefaultBoard(self):
        # Initialize starting board
        upper = ["N", "G", "R", "S", "D"]
        lower = ["d", "s", "r", "g", "n"]
        arr = [None] * self.BOARD_SIZE
        for i in range(self.BOARD_SIZE):
            arr[i] = [""] * self.BOARD_SIZE
            arr[i][0] = lower[i]
            arr[i][self.BOARD_SIZE - 1] = upper[i]
            if i == 0:
                arr[i][1] = "p"
            if i == self.BOARD_SIZE - 1:
                arr[i][self.BOARD_SIZE - 2] = "P"
        return arr
        
    def _initEmptyBoard(self):
        # Initialize empty board
        arr = [[""] * self.BOARD_SIZE for i in range(self.BOARD_SIZE)]
        return arr
            
    def __repr__(self):
        return self._stringifyBoard()

    def _stringifyBoard(self):
        """
        Utility function for printing the board
        """
        s = ''
        for row in range(len(self._board) - 1, -1, -1):

            s += '' + str(row + 1) + ' |'
            for col in range(0, len(self._board[row])):
                s += self._stringifySquare(self._board[col][row])

            s += os.linesep

        s += '    a  b  c  d  e' + os.linesep
        return s

    def _stringifySquare(self, sq):
        """
       	Utility function for stringifying an individual square on the board

        :param sq: Array of strings.
        """
        if type(sq) is not str or len(sq) > 2:
            raise ValueError('Board must be an array of strings like "", "P", or "+P"')
        if len(sq) == 0:
            return '__|'
        if len(sq) == 1:
            return ' ' + sq + '|'
        if len(sq) == 2:
            return sq + '|'
    
    #perform a move
    def _move(self, start, end, player, promote):
        if not self._validMove(start, end, player):
            self._reportIllegalMove()
        else:
            if self._getPiece(end) != "":
                self._capture(end)
            temp = self._getPiece(start)
            self._replacePiece(start, "")
            self._replacePiece(end, temp)
            if promote == 1:
                if not self._validPromotion(self._getPiece(end), end):
                    self._reportIllegalMove()
                else:
                    self._promotePiece(end)
    
    #drop a piece
    def _drop(self, piece, position, player):
        if self._getPiece(position) == "":
            #check if the given piece has been captured
            if player == "UPPER" and piece in self.lower_captures:
                self._replacePiece(position, piece)
            elif player == "lower" and piece in self.UPPER_captures:
                self._replacePiece(position, piece)
        else:
            self._reportIllegalMove()
    
    #check if the given move is legal
    def _validMove(self, start, end, player):
        if self._getPiece(start) == "":
            return False
        elif self._getPiece(end) != "":
            #check that the player is moving their own piece
            print(self._getPiece(start))
            if self._getPiece(start).isupper() and player == "lower":
                print("x")
                return False
            if self._getPiece(start).islower() and player == "UPPER":
                print("y")
                return False
            #check that the player isn't capturing their own piece
            if self._getPiece(start).isupper() == self._getPiece(end).isupper():
                print("z")
                return False
        moves = self._getAvailableMoves(self._getPiece(start), start)
        if end not in moves:
            print("a")
            return False
        return True
    
    # return the piece or empty space found at a given position
    def _getPiece(self, pos):
        return self._board[self.let_num[pos[0]]][int(pos[1]) - 1]
    
    #replace the current empty space or piece with a new one
    def _replacePiece(self, pos, new_piece):
        self._board[self.let_num[pos[0]]][int(pos[1]) - 1] = new_piece
    
    # for file mode; place all provided pieces onto board
    def _placePieces(self, piece_arr):
        for piece_dict in piece_arr:
            self._replacePiece(piece_dict['position'], piece_dict['piece'])
    
    # return the position of a given piece
    def _getPosition(self, piece):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self._board[i][j] == piece:
                    return str(Piece.num_let[i]) + str(j + 1)
        return
        
    #finds all possible spaces on the board that the given piece can move to
    def _getAvailableMoves(self, piece_type, pos):
        piece = Piece(piece_type)
        moves = piece._availableMoves(pos)
        #check if any spaces are occupied by the player's own pieces
        for move in moves:
            if self._getPiece(move) != "":
                piece2 = Piece(self._getPiece(move))
                if piece._player == piece2._player:
                    moves.remove(move)
        return moves
    
    #add captured pieces to relevant capture array
    def _capture(self, pos):
        piece = Piece(self._getPiece(pos))
        #check for promoted pieces
        if "+" in piece._type:
            piece._type = piece[1]
        if piece._player == 1:
            self.lower_captures.append(self._getPiece(pos).lower())
        else:
            self.UPPER_captures.append(self._getPiece(pos).upper())
    
    def _getCapturedPieces(self):
        return ' '.join(self.UPPER_captures), ' '.join(self.lower_captures)
    
    #change illegal move flag to indicate that illegal move was made
    def _reportIllegalMove(self):
        self.ILLEGAL_FLAG = 1
    
    #determine if an illegal move was made
    def _checkLegality(self):
        if self.ILLEGAL_FLAG == 1:
            return False
        return True
    
    #check if we can promote the given piece
    def _validPromotion(self, piece, pos):
        curr = Piece(piece)
        if curr._promotionZone != int(pos[1]):
            return False
        if "+" in curr._type:
            return False
        return True
    
    #promote a given piece
    def _promotePiece(self, pos):
        piece = self._getPiece(pos)
        piece = "+" + piece
        self.replacePiece(pos, piece)
        
    #determine if the current player is in check
    def _checkDetection(self, player):
        king_position = self._getPosition("D")
        opponent_pieces = self.lower_pieces
        if player == "lower":
            king_position = self._getPosition("d")
            opponent_pieces = self.UPPER_pieces
        opponent_moves = self._getPlayerMoves(opponent_pieces)
        if king_position in opponent_moves:
            return True
        return False
    
    #return all possible moves to escape check
    def _possibleCheckMoves(self, player):
        check_moves = []
        #assume that player is UPPER; if not, change variables
        king_type = "D"
        player_pieces = self.UPPER_pieces
        opponent_pieces = self.lower_pieces
        player_captures = self.UPPER_captures
        if player == "lower":
            king_type = "d"
            opponent_pieces = self.UPPER_pieces
            player_pieces = self.lower_pieces
            player_captures = self.lower_captures
        #1. move the king/drive
        king_position = self._getPosition(king_type)
        king_moves = self._getAvailableMoves(king_type, king_position)
        opponent_moves, checking = self._getPlayerMovesAndPos(opponent_pieces, [king_position])       
        for move in king_moves:
            if move not in opponent_moves:
                check_moves.append("move %s %s" % king_position, move)
        
        #2. capture the checking piece
        capturers = self._getPlayerMovesToPos(player_pieces, checking.keys())
        for capturer in capturers.keys():
            for move in capturers[capturer]:
                check_moves.append("move %s %s" %  capturer, move)
        #3. block the checkmate
        between = []
        for pos in checking.keys():
            between.append(self._findSpacesBetween(king_position, pos))
        blockers = self._getPlayerMovesToPos(player_pieces, between)
        for blocker in blockers.keys():
            for move in blockers[blocker]:
                check_moves.append("move %s %s" % blocker, move)
        for piece in player_captures:
            for space in between:
                check_moves.append("drop %s %s" % piece, space)
                
        return check_moves
                
    #get all possible moves for a player
    def _getPlayerMoves(self, player_pieces):
        player_moves = []
        for piece in player_pieces:
            player_moves.add(self._getAvailableMoves(piece, self._getPosition(piece)))
        return player_moves
    
    #get all possible moves for a player, and moves to a given position
    def _getPlayerMovesAndPos(self, player_pieces, positions):
        move_dict = {}
        all_moves = []
        for piece in player_pieces:
            moves = self._getAvailableMoves(piece, self._getPosition(piece))
            for pos in positions:
                if pos in moves:
                    if piece not in move_dict.keys():
                        move_dict[self._getPosition(piece)] = []
                    move_dict[self._getPosition(piece)].append(pos)
            all_moves.append(moves)
        return all_moves, move_dict
    
    #get all possible moves to a given position
    def _getPlayerMovesToPos(self, player_pieces, positions):
        move_dict = {}
        for piece in player_pieces:
            moves = self._getAvailableMoves(piece, self._getPosition(piece))
            for pos in positions:
                if pos in moves:
                    if piece not in move_dict.keys():
                        move_dict[self._getPosition(piece)] = []
                    move_dict[self._getPosition(piece)].append(pos)
        return move_dict
    
    #find all spaces on the grid directly between two positions
    def _findSpacesBetween(self, pos1, pos2):
        spaces = []
        
        #horizontal
        if pos1[0] == pos2[0]:
            dif = max(int(pos1[1]), int(pos2[1])) - min(int(pos1[1]), int(pos2[1]))
            if dif >= 2:
                for i in range(1, dif):
                    spaces.append(str(pos1[0]) + str(min(int(pos1[1]), int(pos2[1]) + i)))
            return spaces
        
        #vertical
        if pos1[1] == pos2[1]:
            a = self.let_num[pos1[1]]
            b = self.let_num[pos2[1]]
            dif = max(a, b) - min(a, b)
            if dif >= 2:
                for i in range(1, dif):
                    spaces.append(str(min(Piece.num_let[a+i], Piece.num_let[b+i])) + str(pos1[1]))
            return spaces
        
        #diagonal
        for i in range(2, self.BOARD_SIZE):
            a = self.let_num[pos1[1]]
            b = self.let_num[pos2[1]]
            if int(pos1[1]) + i <= 5:
                if a + i <= 4:
                    pos = str(Piece.num_let[a+i]) + str(int(pos1[1]) + i)
                    if pos == pos2:
                        for j in range(2, i+i):
                            spaces.append(str(Piece.num_let[a+j]) + str(int(pos1[1]) + j))
                        return spaces
                if a - i >= 0:
                    pos = str(Piece.num_let[a-i]) + str(int(pos1[1]) + i)
                    if pos == pos2:
                        for j in range(2, i+i):
                            spaces.append(str(Piece.num_let[a-j]) + str(int(pos1[1]) + j))
                        return spaces
            if int(pos1[1]) - i >= 1:
                if a + i <= 4:
                    pos = str(Piece.num_let[a+i]) + str(int(pos1[1]) - i)
                    if pos == pos2:
                        for j in range(2, i+i):
                            spaces.append(str(Piece.num_let[a+j]) + str(int(pos1[1]) - j))
                        return spaces
                if a - i >= 0:
                    pos = str(Piece.num_let[a-i]) + str(int(pos1[1]) - i)
                    if pos == pos2:
                        for j in range(2, i+i):
                            spaces.append(str(Piece.num_let[a-j]) + str(int(pos1[1]) - j))
                        return spaces
        
        return spaces
