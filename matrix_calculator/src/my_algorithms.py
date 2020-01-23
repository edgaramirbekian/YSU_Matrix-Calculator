import sys

# Python 3 համատեղելիություն
if sys.version_info[0] == 3:
    # unicode հայտարարված չէ Python 3-ում սակայն այն անհրաժեշտ է ոչ ascii սիմվոլների հետ աշխատելուց Python 2-ում
    unicode = str


def __is_number(n):
    """Պարզել արգումենտը թիվ է թե ոչ"""
    return isinstance(n, float) or isinstance(n, int)


def __is_string(s):
    """Պարզել արգումենտը տող է թե ոչ"""
    return isinstance(s, str) or isinstance(s, unicode)


def my_abs(n):
    """Հաշվել մոդուլային արժեքը"""
    if n < 0:
        return -n
    return n


def my_gcd(n, m):
    """Հաշվել ամենամեծ ընդհանուր բաժանարարը n-ի և m-ի օգտագործելով Շտեյնի ալգորիթմը"""

    unit = 1
    if m < 0:
        unit = -1
    n = my_abs(n)
    m = my_abs(m)

    if n == m == 0:
        return 0
    if n == 0:
        return unit * m
    if m == 0:
        return n
    if n == m:
        return unit * n

    if n < m:
        n, m = m, n

    # Exp-ը ամենամեծ երկուսի աստիճանն է որը բաժանվում է և n-ի և m-ի.
    exp = 0
    # Երբ n-ը և m-ը երկուսն էլ զույգ են, երկուսն էլ բաժանել 2-ի, և մեկով ավելացնել exp-ը.
    while (n | m) & 1 == 0:
        n >>= 1
        m >>= 1
        exp += 1

    while n & 1 == 0:
        n >>= 1

    while n != 0:
        if n < m:
            n, m = m, n

        n -= m
        while n != 0 and n & 1 == 0:
            n >>= 1

    return unit * (m << exp)


def my_max(x, *args):
    """Վերադարձնել մաքսիմումը տրված թվերից կամ զանգվածից"""

    # Եթե ոչ դատարկ զանգված է տրված
    if isinstance(x, list) and len(x) > 0:
        greatest = x[0]
        i = 0
        while i < len(x):
            # Եթե զանգվածում առկա են միայն թվեր
            if not (__is_number(x[i])):
                raise TypeError('Սպասվում է ամբողջ թիվ կամ լողացող կետով թիվ')
            if x[i] > x[0]:
                greatest = x[i]
            i += 1
        return greatest

    # Եթե տրված է թիվ
    if __is_number(x):
        greatest = x
        i = 0

        while i < len(args):
            if not __is_number(args[i]):
                raise TypeError('Սպասվում է ամբողջ թիվ կամ լողացող կետով թիվ')
            if args[i] > x:
                greatest = args[i]
            i += 1
        return greatest

    raise TypeError(
        'Սպասվում է ամբողջ թվերի կամ լողացող կետով թվերի զանգված կամ հաջորդականություն')


def my_range(x, *args):
    """Վերադարձնել ամբողջ թվերի զանգված"""
    # Ներքևի սահման
    lower = 0
    # Սկզբի սահման
    upper = x

    if len(args) == 1:
        lower = x
        upper = args[0]

    ret = []
    i = lower
    while i < upper:
        ret.append(i)
        i += 1

    return ret


def my_reversed(x):
    """Շրջել զանվածը"""

    ret = []
    i = len(x) - 1
    while i >= 0:
        ret.append(x[i])
        i -= 1
    return ret


def my_split(s, char):
    """Բսժանել տողը զանգվածի"""
    if not __is_string(s):
        raise TypeError('Expected a string.')

    result = []
    current_string = ""
    for i in my_range(len(s)):
        # i:s-րդ սիմվոլը
        c = s[i]

        if c == char:
            result.append(current_string)
            current_string = ""
            continue
        current_string += c
    result.append(current_string)
    return result


def my_strip(s):
    """Ջնջել բացատները տողից"""
    if not __is_string(s):
        raise TypeError('Expected a string.')

    #i-ն առաջին ոչ բացատ սիմվոլի ինդեքսն է
    i = 0
    while i < len(s) and s[i] == ' ':
        i += 1

    # j-ն վերջին ոչ բացատ սիմվոլի ինդեքսն է
    j = len(s) - 1
    while j >= 0 and s[j] == ' ':
        j -= 1

    # արդյունքը կլինի տեղի այս մասը s[i] + ... + s[j].
    result = ""
    for char in my_range(i, j+1):
        result += s[char]

    return result


def my_lower(s):

    if not __is_string(s):
        raise TypeError('Expected a string.')

    uppers = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowers = u"abcdefghijklmnopqrstuvwxyz"

    result = ""
    for i in my_range(len(s)):
        char = s[i]
        for j in my_range(len(uppers)):
            # Եթե մեծատառ է դարձնել փոքրատառ
            if char == uppers[j]:
                char = lowers[j]
        result += char

    return result
