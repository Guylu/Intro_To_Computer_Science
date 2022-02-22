def largest_and_smallest(num1, num2, num3):
    """the func gets 3 numbers, and returns the largest one, followed by
    the smallest one"""
    max_num = num3  # max_num = largest number. assuming num3 is the largest
    min_num = num1  # min_num = smallest number. assuming num1 is the smallest
    if(num1 > num2):
        min_num = num2  # knowing num2<num1, we will assign min=num2,
        # and if we wont find a smaller number, min_num will stay as num2
        if(num1 > num3):
            max_num = num1  # if we got here then: num1>num3 and num1>num2(
            # previous "if") then num1 is max_num!
            if(num3 < num2):
                min_num = num3  # if we got here then, num3<num2 and num3<num1
    elif(num2 > num3):
        max_num = num2  # by the same logic num2>num3 and num2>num1(first
        # "if"). that means max_num = num2
        if(num3 < num1):
            min_num = num3  # by the same logic,mun3<num1 and num3<num2.
            # min=num3

    return max_num, min_num  # if we got here without entering any of the code
    # above in the "if" statements, that means our initial assumption of
    # max_num = num3, and min_num = num1, was correct, and we can return
    # those values.
