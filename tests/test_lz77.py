from src.pynflate.lz77 import Lz77
from src.pynflate.lz77 import Codeword


class TestLz77(object):
    def test_empty(self):
        lz77 = Lz77(6)
        codewords = list(lz77.compress(''))
        assert codewords == []

    def test_one_char(self):
        lz77 = Lz77(6)
        original = 'x'

        codewords = list(lz77.compress(original))
        assert codewords == [(0, 0, 'x')]

        decompressed = lz77.decompress(codewords)
        assert decompressed == original

    def test_all_same(self):
        lz77 = Lz77(6)
        original = 'xxxxxxxxxx'

        codewords = list(lz77.compress(original))
        assert codewords == [(0, 0, 'x'), (1, 8, 'x')]

        decompressed = lz77.decompress(codewords)
        assert decompressed == original

    def test_nothing_special(self):
        lz77 = Lz77(6)
        # https://www.cs.cmu.edu/afs/cs/project/pscico-guyb/realworld/www/slidesF08/suffixcompress.pdf
        original = 'aacaacabcabaaac'

        codewords = list(lz77.compress(original))
        assert codewords == [(0, 0, 'a'), (1, 1, 'c'), (3, 4, 'b'), (3, 3, 'a'), (1, 2, 'c')]

        decompressed = lz77.decompress(codewords)
        assert decompressed == original

        #             0<=0         1<=4         2<=5         4<=7         0<=0
        codewords = [(0, 0, 'a'), (1, 4, 'b'), (2, 5, 'c'), (4, 7, 'd'), (0, 0, 'e')]
        #                    a
        #            back 1  \|
        #             4 chars: a a a a + b
        #                     back 2 \___/
        #                   5 chars: a b a b a + c
        #                         back 4 \_______/
        #                                 7 chars: a b a c a b a + d
        #                                                       back 0 \/
        #                                                         0 char: + e
        # aaaaabababacabacabade
        codewords = [Codeword(x[0], x[1], x[2]) for x in codewords]
        tmp = lz77.decompress(codewords)
        # 'aaaaabababacabacabade'

        return