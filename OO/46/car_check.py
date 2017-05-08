class Report:
    TEST_RESULT = """

    Results for car #30-210-18
    * Wheels: OK
    * Brakes: OK
    * Lights: Failed
    * Gear: OK
    NOT PASSED

    """.strip()

    def __init__(self,licence_number):
        self.licence_number = licence_number
        self.checks=[]

    def add_check(self,name,is_passed):
        self.checks.append((name,is_passed))

    def passed(self):
        for name,val in self.checks:
            if not val:
                return False
        return True

    def render(self):
        str="Results for car #{}\n".format(self.licence_number)
        passed = "PASSED"
        for name,val in self.checks:
            tmp = 'OK'
            if not val:
                tmp = "Failed"
                passed = "NOT PASSED"
            str+= "* {}: {}\n".format(name, tmp )
        str +=passed
        return str