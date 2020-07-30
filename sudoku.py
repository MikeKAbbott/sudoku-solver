import csv
import itertools

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        #initialize all of the variables
        self.n2 = 0
        self.n = 0
        self.spaces = 0
        self.board = None
        self.valuesInRows = None
        self.valuesInCols = None
        self.valuesInBoxes = None
        self.unsolved = None
        self.constraints = None

        #load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    #loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                #Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valuesInRows = [set() for _ in range(self.n2)]
                        self.valuesInCols = [set() for _ in range(self.n2)]
                        self.valuesInBoxes = [set() for _ in range(self.n2)]
                        self.unsolved = set(itertools.product(range(self.n2), range(self.n2)))

                #check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row must have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                #add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valuesInRows[reader.line_num-1].add(int(item))
                        self.valuesInCols[index].add(int(item))
                        self.valuesInBoxes[self.spaceToBox(reader.line_num-1, index)].add(int(item))
                        self.unsolved.remove((reader.line_num-1, index))
  

    #converts a given row and column to its inner box number
    def spaceToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n

    #prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            #add row divider
            if r % self.n == 0 and not r == 0:
                if self.n2 > 9:
                    print("  " + "----" * self.n2)
                else:
                    print("  " + "---" * self.n2)
            self.row=""
        
            for c in range(self.n2):
                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                #add column divider
                if c % self.n == 0 and not c == 0:
                    self.row += " | "
                else:
                    self.row += "  "

                #add value placeholder
                if self.n2 > 9:
                    if val is None: self.row += "__"
                    else: self.row += "%2i" % val
                else:
                    if val is None: self.row += "_"
                    else: self.row += str(val)
            print(self.row)
            
       

    # returns True if the space is empty and on the board,
    # and assigning val to it is not blocked by any constraints
   
    def isValidMove(self,space,val):
        """
        2 of the same cannot be in the same row
        2 of the same cannot be in the same column
        2 of the same cannot be in the same box
        """


        #checks if the give value is a valid move by checked if it is in any of the arrays
        if not (space[0] < 0 or space[1] < 0 or space[0] >= self.n2 or space[1] >= self.n2):
            if space in self.unsolved:
                self.board[(space)] = val
                num = self.board[(space)] 
                if num in self.valuesInBoxes[self.spaceToBox(space[0],space[1])]:
                    del self.board[(space)]
                    return False
                elif num in self.valuesInCols[space[1]]:
                    del self.board[(space)]
                    return False
                        
                elif num in self.valuesInRows[space[0]]:
                    del self.board[(space)]
                    return False
                else:
                    del self.board[(space)]
                    return True
            else:
                return False
        else:
            return False
            
            

            


    ## makes a move, records it in its row, col, and box, and removes the space from unsolved
    def placeValue(self,space,val):
            emptySpace = self.isValidMove(space,val)
            if emptySpace == True:
                self.board[(space)] = val
                self.unsolved.remove(space)
                self.valuesInRows[space[0]].add(val)
                self.valuesInCols[space[1]].add(val)
                self.valuesInBoxes[self.spaceToBox(space[0],space[1])].add(val)
                return True
            else:
                return False
            

    # removes the move, its record in its row, col, and box, and adds the space back to unsolved
    def removeValue(self, space, val):
        self.unsolved.add(space);
        num = self.board[(space)] 
        self.valuesInRows[space[0]].remove(val)
        self.valuesInCols[space[1]].remove(val)
        self.valuesInBoxes[self.spaceToBox(space[0],space[1])].remove(val)
        del self.board[(space)]
        return True


    ## gets the unsolved space with the most current constraints
    ## returns None if unsolved is empty

    #returns a list with the location and the numbers that will not fit 
    def getMostConstrainedUnsolvedSpace(self):
        if len(self.unsolved) > 0:
            space = []
            maxConstraints = 0
            for i in self.unsolved:
                count = 0
                constraints = []
                for item in self.valuesInBoxes[self.spaceToBox(i[0],i[1])]:
                    constraints = constraints + [item] 
                    count +=1
                for item in self.valuesInRows[i[0]]:
                    if item not in constraints:
                        constraints = constraints + [item]
                        count +=1
                for item in self.valuesInCols[i[1]]:
                    if item not in constraints:
                        constraints = constraints + [item]
                        count +=1
                if count == maxConstraints:
                    space.append(i) 
                elif count > maxConstraints:
                    maxConstraints = count 
                    space = []
                    space.append(i)
            return space[0]
        else:
            return None 
                
        

            



        
                
                

class Solver:
    def __init__(self):
        pass

    def solve(self, board):
        size = board.n2 ** 2
        original = board
        
        if not board.unsolved:
            board.print()
            return True
        else:
            board.print()
            constraint = board.getMostConstrainedUnsolvedSpace();
            space = constraint
            for val in range(1, board.n2 + 1):
                if board.isValidMove((space), val):
                    board.placeValue(space,val)
                    if self.solve(board):
                        return True  
                    
                    board.removeValue(space,val)

                    
        return False

if __name__ == "__main__":
    #change this to the input file that you'd like to test
    board = Board('tests/bowser.csv');
    s = Solver()
    s.solve(board)

