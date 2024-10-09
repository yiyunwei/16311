def p3(n):
    # Yiyun Wei
    # yiyunwei
    #
    # 16-311 Homework 0
    # Hannah
    #
    # This function returns the nth Fibonacci Number.
    #
    # Put your code here
    x = 0
    y = 1
    if(n == 0):
        return 0
    elif (n == 1):
        return 1
    for i in range(n-1):
        result = x + y
        x = y
        y = result
    return result