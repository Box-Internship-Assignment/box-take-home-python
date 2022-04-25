class Piece:
    """
    Class that represents a ardxShogi piece
    """
    PIECE_TYPES = ["d", "n", "+n", "g", "+g", "s", "r", "+r", "p", "+p"]
    BOARD_SIZE = 5
    num_let = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e"}
    let_num = {"a":0, "b":1, "c":2, "d":3, "e":4}
    def __init__(self, piece_type):
        self._type = piece_type
        self._player = 0 #lower
        self._promotionZone = 5
        if piece_type.isupper():
            self._player = 1 #upper
            self._promotionZone = 1
        
    def __repr__(self):
        return self._type

    def _availableMoves(self, position):
        moves = []
        #preview/pawn
        t = self._type.lower()
        if t == "p":
            if self._player == 0:
                if 1 + int(position[1]) <= 5:
                    return [str(position[0]) + str(int(position[1]) + 1)]
            else:
                if int(position[1]) - 1 >= 0:
                    return [str(position[0]) + str(int(position[1]) - 1)]
            return []
        #notes/rook
        if t == "n" or t == "+n":
            for i in range(self.BOARD_SIZE):
                moves.append(str(position[0]) + str(i))
                moves.append(str(self.num_let[i]) + str(position[1]))
        #governance/bishop
        if t == "g" or t == "+g":
            for i in range(self.BOARD_SIZE):
                new_let = i + self.let_num[position[0]]
                letter = self.num_let[new_let]
                if new_let <= 4:
                    if int(position[1]) + 1 <= 5:                        
                        moves.append(str(letter) + str(int(position[1]) + i))
                    if int(position[1]) - i >= 1:
                        moves.append(str(letter) + str(int(position[1]) - i))
                new_let -= (2 * i)
                if new_let >= 0:
                    if int(position[1]) + 1 <= 5:                        
                        moves.append(str(letter) + str(int(position[1]) + i))
                    if int(position[1]) - i >= 1:
                        moves.append(str(letter) + str(int(position[1]) - i))                   
        #drive/king, and promoted governance/notes
        if t != "n" and t != "g":
            for i in range(3):
                j = -1 + i
                for k in range(3):
                    l = -1 + k
                    let_val = self.let_num[position[0]] + l
                    if let_val >= 0 and let_val <= 4:
                        if int(position[1]) + j >= 1 and int(position[1]) + j <= 5:
                            moves.append(str(self.num_let[let_val]) + str(int(position[1]) + j))
        #shield/gold general, or promoted preview/relay
        if t == "s" or t == "+r" or t == "+p":
            if self._player == 0:
                if int(position[1]) - 1 >= 1:
                    let_val = self.let_num[position[0]] - 1
                    if let_val >= 0:
                        moves.remove(str(self.num_let[let_val]) + str(int(position[1]) - 1))
                    let_val += 2
                    if let_val <= 4:
                        moves.remove(str(self.num_let[let_val]) + str(int(position[1]) - 1))
                else:
                    if int(position[1]) + 1 <= 5:
                        let_val = self.let_num[position[0]] - 1
                        if let_val >= 0:
                            moves.remove(str(self.num_let[let_val]) + str(int(position[1]) + 1))
                        let_val += 2
                        if let_val <= 4:
                            moves.remove(str(self.num_let[let_val]) + str(int(position[1]) + 1))
        #relay/silver general
        print(moves)
        if t == "r":
            if self._player == 0:
                if int(position[1]) - 1 >= 1:
                    moves.remove(str(position[0]) + str(int(position[1]) - 1))
                let_val = self.let_num[position[0]] - 1
                if let_val >= 0:
                    moves.remove(str(self.num_let[let_val])  + str(position[1]))
                let_val += 2
                if let_val <= 4:
                    moves.remove(str(self.num_let[let_val]) + str(position[1]))
            else:
                if int(position[1]) + 1 <= 5:
                    moves.remove(str(position[0]) + str(int(position[1]) + 1))
                let_val = self.let_num[position[0]] - 1
                if let_val >= 0:
                    moves.remove(str(self.num_let[let_val])  + str(position[1]))
                let_val += 2
                if let_val <= 4:
                    moves.remove(str(self.num_let[let_val]) + str(position[1]))
            print(moves)
        return moves
