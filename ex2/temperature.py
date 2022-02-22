def is_it_summer_yet(verge_temperature ,day1_temp, day2_temp, day3_temp):
    """a function that receives 1 verge temperature to test against. it
    also gets 3 recorded temperatures.
    if 2 or more of the recorded temperatures are above the verge
    temperature, then the function returns true, otherwise it returns false"""
    count_over_verge = 0  # a counter to count the amount of days that are
    #  above the verge temperature.
    if (day1_temp > verge_temperature):  # test day1
        count_over_verge += 1  # in case it is above the verge, the counter
        #  is added a value of 1.
    if (day2_temp > verge_temperature):  # test day2
        count_over_verge += 1
    if (day3_temp > verge_temperature):  # test day3
        count_over_verge += 1
    return(count_over_verge > 1)  # if more than 1 recorded temperatures
    # are above the verge, then the function returns true, other wise it
    # will return false.
