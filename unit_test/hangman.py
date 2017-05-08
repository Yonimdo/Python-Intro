class Hangman(object):

    def __init__(self,secret_word,tries_num):
        self.secret_word = secret_word
        self.guessed_word = ['?' for v in secret_word]
        self.tries_num = tries_num

    def status(self):
        return "".join(self.guessed_word)

    def guess(self,char):
        if self.tries_num<=0:
            raise GameOver(self.secret_word)
        counter = 0
        self.tries_num -=1
        for i, v in enumerate(self.secret_word):
            if char==v:
                counter+=1
                self.guessed_word[i]=char
        return counter

    def won(self):
        return self.secret_word == "".join(self.guessed_word)

class GameOver(Exception):
    def __init__(self, word):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, 'The word was "{}"'.format(word))

