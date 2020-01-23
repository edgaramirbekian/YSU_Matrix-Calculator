from .my_algorithms import my_split, my_strip, my_lower
from .calculator import frac_reduc
from .Matrix import Matrix
import sys

# Դարձնել այս մոդուլը Pyrhon 2 համատեղելի.
if sys.version_info[0] == 2:
    input = raw_input


def __ask_input(string):
    """Հարցնել օգտվողի ինֆորմացիա 'string' փոփոխականի միջոցով."""
    try:
        input_data = input(string)
    except (KeyboardInterrupt, EOFError):
        print("\nՑտեսություն!")
        sys.exit(0)
    return input_data


def __is_number(n):
    """Պարզել տրված արգումենտը թիվ է թե ոչ"""
    try:
        # Տողերը կարող են փոխարկվել լողացող թվով թվերի եթե ճիշտ ձևով են գրված
        float(n)
        return True
    except:
        return False


def __parse_float(string):
    """Փորձել ստանալ լողացող թվով թիվ տողից"""
    elem = my_split(string, ".")

    # Տողը լող․ կետով թվի փոխարկելի ձևով չի գրված
    if len(elem) == 1:
        elem = my_split(string, ",")

    # Տողը լող․ կետով թվի փոխարկելի ձևով է գրված
    if len(elem) == 2:
        # Ամբողջ կամ տասնավոր մասը թիվ չէ
        if not (__is_number(elem[0])) or not (__is_number(elem[1])):
            return None

        numerator = int(elem[0]) * 10 ** len(elem[1])
        if numerator >= 0:
            numerator += int(elem[1])
        else:
            numerator -= int(elem[1])

        denominator = 10 ** len(elem[1])
        frac = (numerator, denominator)

        return frac_reduc(frac)

    return None


def __parse_fraction(string):
    """Փոխարկել տողի մի մասը. Վերադարձնել none եթե տվյալը մեկ մասից չէ բաղկացած"""
    elem = my_split(string, "/")

    if len(elem) == 2:
        # Ստուգել տողի կոտորոկային կամ լող․ կետով թվ․ փոխարկելու հնարավորությունը
        frac_1 = __parse_float(elem[0])
        frac_2 = __parse_float(elem[1])

        if not frac_1:
            if not __is_number(elem[0]):
                return None
            frac_1 = (int(elem[0]), 1)

        if not frac_2:
            if not __is_number(elem[1]):
                return None
            frac_2 = (int(elem[1]), 1)

        numerator = frac_1[0] * frac_2[1]
        denominator = frac_1[1] * frac_2[0]
        frac = (numerator, denominator)
        return frac_reduc(frac)

    return None


def __parse_values(row):
    """Փոխարկել տողը զանգվածի"""
    values = []
    args = my_split(row, " ")

    for i in range(len(args)):
        elem = __parse_fraction(args[i])

        if not elem:                      # elem-ը մի ամբողջություն չէ
            elem = __parse_float(args[i])

        if not elem:                      # elem-ը լող․ կետով թիվ չէ
            if not __is_number(args[i]):  # elem-ը թիվ չէ
                return None
            elem = (int(args[i]), 1)

        values.append(elem)

    return values


def parseMatrix():
    """Խնդրել օգտվողին ներդնել մատրից գործողություն կատարելու և նոր մատրից վերադարձնելու համար"""

    rows = []

    print("")
    print("Ներմուծեք մատրիցի տարրերը տող առ տող․ enter-ը նշանակում է տողի վերջ.")

    row = my_strip(__ask_input("տող: "))

    # Ցիկլով անցնել մինչև որ դատարկ տողի հանդիպելը.
    while row:
        newRow = __parse_values(row)

        # Օգտվողը տվել է սխալ ինֆորմացիա
        if not newRow:
            print("")
            print("Օգտվողը տվել է սխալ ինֆորմացիա")
            print("Խնդրում եմ, գրիր տողերը ճշգրիտ")
            print("Թույլատրելի է միայն ամբողջ թվեր, լողացող կետով կամ կոտորակային թվեր "
                  "առանց փակագծերի և այլ նշանների")

        # Օգտվողը փորձում է ներմուծել ավելի շատ արժեքներ քան տողի չափսն է
        elif len(rows) > 0 and len(newRow) != len(rows[0]):
            print("")
            print("Դուք ներմուծել եք տարրերի սխալ քանակություն")
            print("Ուշադրություն դարձրեք տեղերի չափսի և տվյալների քանակության վրա")

        else:
            rows.append(newRow)

        row = my_strip(__ask_input("տող: "))

    # Տողեր տրված չեն
    if len(rows) == 0:
        return None

    ret = Matrix(rows, len(rows), len(rows[0]))
    return ret


def parseOperator():
    """հարցնել գործողության տիպը"""

    print("")

    print("Ի՞նչ գործողություն եք ցանկանում իրականացնել հաջորդիվ")
    print("Կախված ձեր ընտրությունից հնարավոր է ուրիշ մատրից մուտքագրելու անհրաժեշտություն")

    print("")

    print("+:         Ավելացնել մեկ այլ մատրից ստացվածին")
    print("-:         Հանել ուրիշ մատրից ստացվածից")
    print("*:         Բազմապատկել ուրիշ մատրից ստացվածին")
    print("det:       Հաշվել ստացված մատրիցի դետերմինանտը")
    print("inverse:   Հակադարձել ստացված մատրիցը եթե հնարավոր է")
    print("scalar:    Բազմապատկել ստացված մատրիցը սկալյարով")
    print("transpose: Հաշվել ստացված մատրիցի տրանսպոզիցիան")
    print("print:     Տպել ստացված մատրիցը")

    print("")

    operator = my_lower(my_strip(__ask_input("Operator: ")))
    while operator not in ["*",
                           "-",
                           "+",
                           "det",
                           "scalar",
                           "inverse",
                           "invert",
                           "-1",
                           "print",
                           "transpose"]:
        print("Խնդրում եմ ընտրեք վալիդ գործողություն")
        operator = my_lower(my_strip(__ask_input("Գործողություն: ")))

    return operator


def parseScalar():
    """Հարցնել օգտվողին սկալյար արտադրիչ"""
    print("")

    scalar = __ask_input("Ներմուծել սկալյար մեծություն ամբողջ թվով: ")

    # Օգտվողը պեպտք է մուտքագրի ամբողջ թիվ որպես սկալյար
    while not __is_number(scalar):
        scalar = __ask_input("Ներմուծել սկալյար մեծություն ամբողջ թվով: ")

    if scalar // 1 == scalar:
        return int(scalar)
    return scalar


def askToContinue():
    """Հարցնել ստացված մատրիցի հետ գործողություն կատարելու որոշման մասին"""

    print("")
    print("Ուզում ե՞ք կիրառել այլ գործողություն ստացված մատրիցի հետ")

    a = my_lower(__ask_input("Այո/Ոչ մուտքագրել Y կամ N: "))
    print("")

    while(a != "y" and a != "n"):
        a = my_lower(__ask_input("Այո/Ոչ մուտքագրել Y կամ N: "))

    if a == "y":
        return True
    return False
