import unittest
from unit_test.hangman import Hangman
from unit_test.hangman import GameOver


class TestHangman(unittest.TestCase):
    def setUp(self):
        self.game = Hangman("hello", 10)

    def test_status(self):
        self.assertEquals(self.game.status(), "?????")

    def test_good_guess(self):
        self.game.guess('h')
        self.assertEquals(self.game.status(), "h????")

    def test_bad_guess(self):
        self.game.guess('s')
        self.assertEquals(self.game.status(), "?????")

    def test_multiple_guess(self):
        self.game.guess('l')
        self.assertEquals(self.game.status(), "??ll?")

    def test_multiple_good_guess(self):
        self.game.guess('h')
        self.assertEquals(self.game.status(), "h????")
        self.game.guess('i')
        self.assertEquals(self.game.status(), "h????")
        self.game.guess('e')
        self.assertEquals(self.game.status(), "he???")
        self.game.guess('l')
        self.assertEquals(self.game.status(), "hell?")

    def test_game_over(self):
        def f(x):
            for i in range(x):
                self.game.guess('g')

        self.assertRaises(GameOver, f, 11)

    def test_game_over_2(self):
        with self.assertRaises(GameOver):
            for i in range(11):
                self.game.guess('z')

    def test_game_won(self):
        self.game.guess('h')
        self.game.guess('e')
        self.game.guess('l')
        self.game.guess('o')
        self.assertTrue(self.game.won())


if __name__ == '__main__':
    unittest.main()
