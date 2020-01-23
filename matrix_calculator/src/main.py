from .parser import parseMatrix, parseOperator, parseScalar, askToContinue
from .calculator import *
import sys

# Դարձնել այս մոդուլը Pyrhon 2 համատեղելի.
if sys.version_info[0] == 2:
    input = raw_input


def __handle_operator(operator, matrix):
    """Կատարել օգտվողի կողմից տրված գործողությունը մատրիցի հետ"""

    # Օգտվողը ուզում է հաշվել դետերմինանտը
    if operator == "det":
        ans = matrixDeterminant(matrix)
        if ans != 0 and not ans:
            print("Դետերմինանտը անորոշ է կամ գոյություն չունի տրված մատրիցի համար")
        else:
            print("Դետերմինանտն է՝: " + str(ans))

    # Օգտվողը ուզում է հաշվել հակադարձը.
    if operator == "inverse" or operator == "-1":
        matrix2 = matrixInverse(matrix)
        if not matrix2:
            print("Մատրիցը հակադարձելի չէ")
        else:
            matrix = matrix2
            print("Մատրիցի հակադարձումը հաջողված է")

    # Օգտվողը ուզում է հաշվել բազմապատկել մատրիցը սկալյարով.
    if operator == "scalar":
        n = parseScalar()
        matrix.multiplyScalar(n)
        print("Մատրիցի բազմապատկումը սկալյարով հաջողված է")

    # Օգտվողը ուզում է հաշվել տրանսպոզը
    if operator == "transpose":
        matrix = matrixTranspose(matrix)
        print("Մատրիցի տրանսպոզիցիան գտնելը հաջողված է")

    # Օգտվողը ուզում է հաշվել մատրիցների գումարը
    if operator == "+":
        matrix2 = parseMatrix()

        # Կվերադարձնի None եթե մատրիցների գումարումն անհնար է
        resultMatrix = matrixAddition(matrix, matrix2)

        if not resultMatrix:
            print("Մատրիցի գումարումը ձախողված է")
        else:
            matrix = resultMatrix
            print("Մատրիցի գումարումը հաջողված է")

    # Օգտվողը ուզում է հաշվել մատրիցների տարբերությունը
    if operator == "-":
        matrix2 = parseMatrix()
        resultMatrix = matrixSubstraction(matrix, matrix2)
        if not resultMatrix:
            print("Մատրիցի բազմապատկումը ձախողված է")
        else:
            matrix = resultMatrix
            print("Մատրիցի բազմապատկումը հաջողված է")

    # Օգտվողը ուզում է հաշվել մատրիցների արտադրյալը
    if operator == "*":
        matrix2 = parseMatrix()
        resultMatrix = matrixMultiplication(matrix, matrix2)
        if not resultMatrix:
            print("Մատրիցի բազմապատկումը տապալված է")
        else:
            matrix = resultMatrix
            print("Մատրիցի բազմապատկումը հաջողված է")

    # Տպել արդյունքում ստացված մատրիցը օգտվողին
    print(matrix)
    return matrix


def main():
    """Կապել հայտարարված ֆունկցիաները միմյանց"""

    # Հարցնել առաջին մատրիցը
    matrix = parseMatrix()

    # Կատարել օպերացիան կամ կանգնել երբ այն None է
    while matrix:
        # Հարցնել ինչ օպերացիա է օգտվողն ուզում կիրառել
        operator = parseOperator()

        # Կատարել գործողությունը մատրիցի(ների) վրա
        matrix = __handle_operator(operator, matrix)

        userWantsToContinueWithCurrentMatrix = askToContinue()
        if not userWantsToContinueWithCurrentMatrix:
            # Հարցնել նոր մատրից եթե Օգտագործողը ոչ մի տարր չի հայտարարել
            # կամ եթե մատրիցը None արժեք ունի
            # ծրագիրը կկանգնի
            matrix = parseMatrix()

    print("")
    print("Ցտեսություն!")
