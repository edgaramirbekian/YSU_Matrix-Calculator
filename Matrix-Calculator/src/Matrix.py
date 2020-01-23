from .my_algorithms import my_range

class Matrix:
    """Matrix Կլասս"""

    def __init__(self, rows, n, m):
        """Կառուցել մատրիցի օբյեկտ

        Արգումենտներ:
        rows -- տողերի զանգվածը
        n    -- տողերի թիվը
        m    -- սյունակների թիվը
        """
        self.rowAmount = n
        self.colAmount = m
        self.rowArray = rows
        self.colArray = [[] for i in my_range(n)]
        self.scalar = 1

    def __str__(self):
        """Տպել մատրիցը օգտվողին ընթեռնելի ձևով"""
        output = ""

        for row in self.rowArray:
            output += "["

            for i in my_range(len(row)):
                cell = row[i]
                elem = self.scalar * 1.0 * cell[0] / cell[1]

                if elem % 1 == 0:
                    elem = int(elem)

                if i == len(row) - 1:
                    output += str(elem)
                else:
                    output += str(elem) + " "

            output += "]\n"
        return output[:-1]

    def multiplyScalar(self, n):
        """Բազմապատկել սկալյարով."""
        self.scalar *= n

    def getRowAmount(self):
        """Վերադարձնել տողերի քանակը"""
        return self.rowAmount

    def getRowArray(self):
        """Վերադարձնել տողերի զանգվածը"""
        if self.scalar == 1:
            return self.rowArray
        returnArray = [[self.scalar * elem for elem in row]
                       for row in self.rowArray]
        return returnArray

    def getColAmount(self):
        """Վերադարձնել սյունակների թիվը"""
        return self.colAmount

    def getColArray(self):
        """Վերադարձնել սյունակների զանգվածը"""
        return self.colArray

    def getScalar(self):
        """Վերադարձնել սկալյարը"""
        return self.scalar

    def getCell(self, row, col):
        """Վերադարձնել տարրի արժեքը ըստ նրա դիրքի"""
        return (self.scalar * self.rowArray[row][col][0],
                self.rowArray[row][col][1])

    def getRow(self, row):
        """Վերադարձնել հարցվող տողը"""
        if self.scalar == 1:
            return self.rowArray[row]

        returnRow = [(self.scalar * elem[0], elem[1])
                     for elem in self.rowArray[row]]
        return returnRow

    def genColArray(self, col):
        """Ստեղծել հարցվող սյունակը և այն պահել self.colArray-ում"""
        for i in my_range(self.rowAmount):
            self.colArray[col].append(self.rowArray[i][col])
        return self.colArray[col]

    def getCol(self, col):
        """Վերադարձնել հարցվող սյունակը"""
        if len(self.colArray[col]) == 0:
            self.genColArray(col)

        if self.scalar == 1:
            return self.colArray[col]

        returnCol = [(self.scalar * elem[0], elem[1])
                     for elem in self.colArray[col]]
        return returnCol
