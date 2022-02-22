import math

INSERT_COEFFICIENTS = "Insert coefficients a, b, and c: "
NO_SOLUTION = "The equation has no solutions"
ONE_SOLUTION = "The equation has 1 solution:"
TWO_SOLUTIONS = "The equation has 2 solutions:"

def quadratic_equation(a,b,c):
    """the func gets 3 number witch describe a quadratic equation = ax^2 +
    bx + c, and returns the 0/1/2 solutions(0 solutions return None,
    1 solution returns a number, None)"""
    root = b**2 - 4*(a*c)  # the calculation inside the root(in the equation)
    if(root < 0):
        return None,None  # 0 solution in case of a negative number inside
        # the square root
    elif(root == 0):  # in case of a zero, there only one solution.
        return (-b / 2*a, None)  # calculates the final step, and returns
        # the single solution.
    root = math.sqrt(root)  # calculates the square root(using math),
    # and puts it
    # inside the same variable.
    possible_root1 = -b + root  # final calculation in the formulas numerator
    possible_root2 = -b - root  # for each of the solutions.
    return possible_root1 / (2*a), possible_root2 / (2*a)  # returns the final
    #  calculation of the entire formula(once for each solution.

def quadratic_equation_user_input():
    """ a func that receives nothing.
    it opens a dialog with the user, and gets an input of a string
    containing the 3 coefficients for a quadratic equation.
    then it will convert them into float and use the "quadratic_equation"
    func to print the solutions to the equation"""
    sting_of_coefficients = input(INSERT_COEFFICIENTS)
    # sting_of_coefficients is the string input from user, containing a,b,c
    a, b, c = sting_of_coefficients.split()  # splits the entire string
    #  by the " " character, into 3 different strings witch will contain the 3
    # coefficients
    possible_solution1, possible_solution2 = quadratic_equation(float(a),
                                                                float(b),
                                                                float(c))
    # solves the equation, and puts the solutions into possible_solution1,
    # possible_solution2
    if(possible_solution1 == None):
        if(possible_solution2 == None):  # possible_solution1,
            # possible_solution2 = None: no solutions
            print(NO_SOLUTION)
            return
        # if we got here then, possible_solution1 = None,
        # but possible_solution2 is the single solution
        print(ONE_SOLUTION, possible_solution2)
        return
    if(possible_solution2 == None):
        #  if we got here then, possible_solution2 = None,
        # but possible_solution1 is the single solution
        print(ONE_SOLUTION, possible_solution1)
        return
    # if none of the "returns" triggered, then there are 2 solution
    print(TWO_SOLUTIONS, possible_solution1, "and",
          possible_solution2)
    return
