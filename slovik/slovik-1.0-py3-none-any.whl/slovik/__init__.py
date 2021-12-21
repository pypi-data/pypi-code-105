def ns(number, base):
    digit = 1
    answer = 0
    while number > 0:
        answer = answer + digit*(number % base)
        digit = digit * 10
        number = number // base
    return(answer)

def nsstr(number, base):
    answer = ""
    str16 = "0"
    for i in range(0, 20):
        str16 = str16 + "0"
    str16 = str16[0:10] + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while number > 0:
        rest = str(number%base)
        if int(rest) < 10:
            answer = str(int(rest))+answer
            number = number // base
        if int(rest) >= 10:
            answer = str16[int(rest)] + answer
            number= number // base
    return(answer)

def ns10(number, basefrom):
    count = 0
    base = basefrom
    answer = 0
    while number > 0:
        answer = answer + (base**count)*(number % 10)
        count+=1
        number = number // 10
    return(answer)

