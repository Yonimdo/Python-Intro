import calendar


class MyTextCalendar(calendar.TextCalendar):
    # --- WRITE YOUR CODE HERE --- #

    def formatday(self, day, weekday, width):
        """
        Returns a formatted day.
        """
        s = super().formatday(day, weekday, width)
        if '7' in s or (day and day % 7 == 0) :
            s = " *"
        return s


c = MyTextCalendar()
result = c.formatmonth(2014, 5)
print("My calendar:")
print("-" * 40)
print(result)
print("-" * 40)

expected = '''      May 2014
Mo Tu We Th Fr Sa Su
          1  2  3  4
 5  6  *  8  9 10 11
12 13  * 15 16  * 18
19 20  * 22 23 24 25
26  *  * 29 30 31
'''
print("Expected:")
print("-" * 40)
print(expected)
print("-" * 40)

assert result == expected
