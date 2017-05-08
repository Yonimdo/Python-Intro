class SimpleWriter():
    def render(self, s):
        return "*{}*".format(s)


class BetterWriter(SimpleWriter):
    def render(self, s):
        # resp = SimpleWriter.render(self,s)
        resp = super().render(s)
        # py-2 resp = super(BetterWriter, self).render(s)
        return "!{}!".format(resp)


class MuchBetterWriter(BetterWriter):
    def render(self, s):
        # resp = SimpleWriter.render(self,s)
        resp = super().render(s)
        # py-2 resp = super(BetterWriter, self).render(s)
        return "@{}@".format(resp)


bw = MuchBetterWriter()
print(bw.render("yoni"))
