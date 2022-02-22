import math
def shape_area():
    """ multi choice function, the user gets prompted to input a number to
    represent a shape:
    1: circle.
    2: rectangle
    3: same sided triangle
    the function then asks to input the details of the shape(radius,
    length..) and returns the area"""
    shape = input("Choose shape (1=circle, 2=rectangle, 3=triangle): ")  #
    # shape is a string that holds the users picked shape
    if(shape == "1"):  # circle
        radius = float(input())  # asks for the circles radius
        return(math.pi * (radius**2))  # calculates pi * R^2, and returns
        # the value
    elif(shape == "2"):  # rectangle
        first_square_side = float(input())
        second_square_side = float(input())
        return(first_square_side * second_square_side)  # area of rectangle
        #  formula
    elif(shape == "3"):  # same sided triangle
        triangle_side = float(input())
        return (math.sqrt(3)/4) * triangle_side**2  # returns the calculated
        #  area from formula
    else:  # didn't choose a valid number
        return None