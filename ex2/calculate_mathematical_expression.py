def calculate_mathematical_expression(num1, num2, operation):
    """receives 3 vars.
    num1\num2 = numbers, operation = the operation to conduct between the
    numbers. the function returns the result of the operation on the
    numbers"""
    if(operation == "+"):  # the operation is addition
        return num1 + num2
    elif(operation == "-"):  # the operation is subtraction
        return num1 - num2
    elif(operation == "/" and num2 != 0):  # the operation is division(not
        # by 0)
        return num1 / num2
    elif(operation == "*"):  # the operation is multiplication
        return num1 * num2
    return none  # if the operation is invalid(not + - * /) or devising by
    # 0, then return none

def calculate_from_string(math_string):
    """ the function receives a string containing a math formula to
    calculate the result of. the string contains two numbers separated by a
    math operation. the func returns a float of the result. """
    num1, operation, num2 = math_string.split(" ")  # a string function
    # witch will split the " " separated characters into 3 variables.
    return calculate_mathematical_expression(float(num1), float(num2),
                                             operation)  # the 3 variables
    # are sent to "calculate_mathematical_expression" to calculate the result


