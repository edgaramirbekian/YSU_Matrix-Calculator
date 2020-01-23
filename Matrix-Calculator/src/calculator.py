from .Matrix import Matrix
from .my_algorithms import my_gcd, my_abs, my_range, my_reversed


def frac_add(frac_a, frac_b):
    """Վերադարձնել բաղադրիչների գումարը"""
    if frac_a[1] == frac_b[1]:
        return (frac_a[0] + frac_b[0], frac_a[1])

    numerator = frac_a[0] * frac_b[1] + frac_b[0] * frac_a[1]
    denominator = frac_a[1] * frac_b[1]
    return (numerator, denominator)


def frac_sub(frac_a, frac_b):
    """Վերադարձնել բաղադրիչների տարբերությունը"""
    if frac_a[1] == frac_b[1]:
        return (frac_a[0] - frac_b[0], frac_a[1])

    numerator = frac_a[0] * frac_b[1] - frac_b[0] * frac_a[1]
    denominator = frac_a[1] * frac_b[1]
    return (numerator, denominator)


def frac_mult(frac_a, frac_b):
    """Վերադարձնել բաղադրիչների արտադրյալը"""
    numerator = frac_a[0] * frac_b[0]
    denominator = frac_a[1] * frac_b[1]
    return (numerator, denominator)


def frac_div(frac_a, frac_b):
    """Վերադարձնել frac_a բաժանած frac_b-ի"""
    numerator = frac_a[0] * frac_b[1]
    denominator = frac_a[1] * frac_b[0]
    return (numerator, denominator)


def frac_abs(frac):
    """Վերադարձնել բաղադրիչների մոդուլով արժեքը"""
    return (my_abs(frac[0]), my_abs(frac[1]))


def frac_ge(frac_a, frac_b):
    """Համեմատել բաղադրիչները"""
    return frac_a[0] * frac_b[1] > frac_b[0] * frac_a[1]


def frac_reduc(frac):
    """գտնել ամենամեջ ընդհանուր բաժանարարը"""
    syt = my_gcd(frac[0], frac[1])

    # Խուսափում ենք վերջում 0/0-ից
    # gcd(0, 0) == 0.
    if syt == 0:
        syt = 1

    return (int(frac[0] / syt), int(frac[1] // syt))


def matrixAddition(A, B):
    """Գումարել մատրիցները եթե գումարման պայմանը տեղի ունի"""

    if not A or not B:
        return None
    # Գումարումը սահմանված չէ
    if A.getColAmount() != B.getColAmount():
        return None
    if A.getRowAmount() != B.getRowAmount():
        return None

    C = []
    for rowIndex in my_range(A.getRowAmount()):
        resultRow = []
        for colIndex in my_range(A.getColAmount()):
            cellOfA = A.getCell(rowIndex, colIndex)
            cellOfB = B.getCell(rowIndex, colIndex)
            result = frac_add(cellOfA, cellOfB)
            resultRow.append(frac_reduc(result))
        C.append(resultRow)

    return Matrix(C, A.getRowAmount(), A.getColAmount())


def matrixSubstraction(A, B):
    """Հանել մատրիցները եթե պայմանները տեղի ունեն."""

    if not A or not B:
        return None

    if A == B:
        # Վերադարձնել 0-ական մատրից այս դեպքում
        return Matrix(
            [[(0, 1) for i in my_range(A.getColAmount())]
             for j in my_range(A.getRowAmount())],
            A.getRowAmount(),
            A.getColAmount())

    # Բազմապատկել -1 ով քանի որ A-B == A+(-1*B).
    B.multiplyScalar(-1)
    resultMatrix = matrixAddition(A, B)

    # Շտկել B արժեքը
    B.multiplyScalar(-1)

    return resultMatrix


def matrixScalarMultiplication(A, scalar):
    """Բազմապատկել սկալյարով"""
    A.multiplyScalar(scalar)
    return A


def matrixMultiplication(A, B):
    """Բազմապատկել մատրիցները եթե բազմապատկման պայմանը տեղի ունի"""

    if not A or not B:
        return None
    # Բազմապատկում սահմանված չէ
    if A.getColAmount() != B.getRowAmount():
        return None

    n = A.getRowAmount()
    m = A.getColAmount()
    p = B.getColAmount()

    C = [[(0, 1) for i in my_range(p)] for j in my_range(n)]

    for i in my_range(n):
        for j in my_range(p):
            cellValue = (0, 1)

            for k in my_range(m):
                toAdd = frac_mult(A.getCell(i, k), B.getCell(k, j))
                cellValue = frac_add(cellValue, toAdd)

            cellValue = frac_reduc(cellValue)
            C[i][j] = cellValue

    return Matrix(C, n, p)


def matrixTranspose(A):
    """Հաշվել տրանսպոզիցիան"""
    n = A.getRowAmount()
    m = A.getColAmount()
    result = [[A.getCell(j, i) for j in my_range(n)] for i in my_range(m)]
    return Matrix(result, m, n)


def __pivot(A):
    """Պտտել A-ն, որպեսզի յուրաքանչյուր սյունակի ամենամեծ տարրը գտնվի  անկյունագծում:

    Ավելի կոնկրետ ՝ A- ն այն ձևափոխված է,
    որպեսզի յուրաքանչյուր անկյունային տարր ունենա այնպիսի արժեք,
    որն ունի առնվազն նույնքան մեծ բացարձակ արժեք, որքան դրա ներքևի յուրաքանչյուր բջիջ:"""
    n = A.getRowAmount()

    # P-ն նույնականացման մատրից է
    P = [[(int(i == j), 1) for i in my_range(n)] for j in my_range(n)]

    totalPivots = 0

    for j in my_range(n):
        greatest = (0, 1)
        swapWith = j

        for row in my_range(j+1, n):
            if frac_ge(frac_abs(A.getCell(row, j)), greatest):
                greatest = frac_abs(A.getCell(row, j))
                swapWith = row

        if swapWith != j:
            P[j], P[swapWith] = P[swapWith], P[j]
            totalPivots += 1

    return (Matrix(P, n, n), totalPivots)


def __LUP_decomposition(A):
    """Հաշվել LUP դեկոմպոզիցիան"""
    n = A.getRowAmount()

    # Ձևափոխել L և U ինչպես զրոյական մատրից
    L = [[(0, 1) for i in my_range(n)] for j in my_range(n)]
    U = [[(0, 1) for i in my_range(n)] for j in my_range(n)]

    pivot_info = __pivot(A)
    P = pivot_info[0]

    mult = (-1) ** pivot_info[1]

    Prod = matrixMultiplication(P, A)

    # Օգտագործելով հետևյալ ալգորիթմը
    # https://rosettacode.org/wiki/LU_decomposition հաշվել բջիջների արժեքները L-ի և U-ի համար

    for j in my_range(n):
        # Calculate U[i][j].
        for i in my_range(j+1):
            the_sum = (0, 1)

            for k in my_range(i):
                toAdd = frac_mult(U[k][j], L[i][k])
                the_sum = frac_add(the_sum, toAdd)

            the_sum = frac_reduc(the_sum)
            # U_ij == Prod_ij - the_sum
            U[i][j] = frac_sub(Prod.getCell(i, j), the_sum)

        # Calculate L[i][j].
        for i in my_range(j, n):
            the_sum = (0, 1)

            for k in my_range(j):
                toAdd = frac_mult(L[i][k], U[k][j])
                the_sum = frac_add(the_sum, toAdd)

            the_sum = frac_reduc(the_sum)
            L[i][j] = frac_sub(Prod.getCell(i, j), the_sum)
            L[i][j] = frac_div(L[i][j], U[j][j])

    L = Matrix(L, n, n)
    U = Matrix(U, n, n)

    return (L, U, P, mult)


def matrixDeterminant(A):
    """Հաշվել դետերմինանտը"""

    # Դետերմինանտը սահմանված չէ ոչ քառակուսի մատրիցների համար
    if A.getRowAmount() != A.getColAmount():
        return None

    # Կազմալուծել մատրիցը
    decomposition = __LUP_decomposition(A)

    U = decomposition[1]

    # Դետերմինանտը U-ի անկյունագծային արժեքների արտադրյալն է
    ans = (1, 1)
    for i in my_range(U.getRowAmount()):
        ans = frac_mult(ans, U.getCell(i, i))
        ans = frac_reduc(ans)

    if ans[1] == 0:
        return 0

    det_of_P = decomposition[3]
    det = ans[0] * det_of_P * 1.0 / ans[1]
    if det // 1 == det:
        return int(det)
    return det


def __forward_substitution(L):
    """Հակադարձել L-ը առաջ փոխարինմամբ

    http://en.wikipedia.org/wiki/Triangular_matrix#Forward_and_back_substitution
    """
    m = L.getRowAmount()
    inverse = [[(0, 1) for i in my_range(m)] for j in my_range(m)]

    for a in my_range(m):
        bVector = [(0, 1) for i in my_range(m)]
        bVector[a] = (1, 1)

        xVector = []
        for x in my_range(m):
            the_sum = (0, 1)

            for i in my_range(x):
                toAdd = frac_mult(L.getCell(x, i), xVector[i])
                the_sum = frac_add(the_sum, toAdd)

            the_sum = frac_reduc(the_sum)
            value = frac_sub(bVector[x], the_sum)
            value = frac_mult(value, L.getCell(x, x))
            value = frac_reduc(value)
            xVector.append(value)

        for i in my_range(m):
            inverse[i][a] = xVector[i]

    return Matrix(inverse, m, m)


def __backward_substitution(U):
    """Հակադարձել U-ն հետ փոխարինմամբ"""

    m = U.getRowAmount()
    inverse = [[(0, 1) for i in my_range(m)]
               for j in my_range(m)]

    for a in my_range(m):
        bVector = [(0, 1) for i in my_range(m)]
        bVector[a] = (1, 1)

        xVector = []
        for x in my_reversed(my_range(m)):
            the_sum = (0, 1)

            for i in my_reversed(my_range(x+1, m)):
                toAdd = frac_mult(U.getCell(x, i), xVector[m-1 - i])
                the_sum = frac_add(the_sum, toAdd)

            the_sum = frac_reduc(the_sum)
            value = frac_sub(bVector[x], the_sum)
            value = frac_div(value, U.getCell(x, x))
            value = frac_reduc(value)
            xVector.append(value)

        for i in my_range(m):
            inverse[m-1-i][a] = xVector[i]

    return Matrix(inverse, m, m)


def matrixInverse(A):
    """Հակադարձել A մատրիցը"""
    # եթե մատրիցը 0-ական է
    if matrixDeterminant(A) == 0:
        return None

    # հաշվել A-ի LUP դեկոմպոզիցիան of A. PA = LU
    decomposition = __LUP_decomposition(A)

    # Հակադարձել L-ը առաջ փոխարինմամբ
    L_inv = __forward_substitution(decomposition[0])
    # Հակադարձել U-ն հետ փոխարինմամբ
    U_inv = __backward_substitution(decomposition[1])

    P = decomposition[2]

    # PA = LU
    # -> (PA)^-1 = (LU)^-1
    # -> A^-1 * P^-1 = U^-1 * L^-1
    # -> A^-1 = U^-1 * L^-1 * P
    C = matrixMultiplication(U_inv, L_inv)
    return matrixMultiplication(C, P)
