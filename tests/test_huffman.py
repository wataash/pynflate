from pytest import fixture
from src.pynflate.huffman import Codec, huffman, compress
from src.pynflate.huffman import tree_encode


@fixture
def codec():
    c = Codec()

    c.update('a', '0')
    c.update('b', '10')
    c.update('c', '11')

    return c


class TestCodec:
    def test_interface(self):
        codec = Codec()
        codec.update('a', '010')
        assert codec.encode('a') == '010'
        assert codec.decode('010') == 'a'

    def test_many_letters(self, codec):
        assert codec.encode('b') == '10'
        assert codec.decode('0') == 'a'

    def test_two_letter_encoding(self, codec):
        assert codec.encode('ab') == '010'

    def test_two_letter_decoding(self, codec):
        assert codec.decode('010') == 'ab'

    def test_complex_coding(self, codec):
        assert codec.encode('cca') == '11110'
        assert codec.decode('1110010') == 'cbab'


class TestHuffman:
    def test_interface(self):
        codes = huffman({'a': 1, 'b': 2})
        assert codes == {'a': '0', 'b': '1'}

    def test_two_letters(self):
        codes = huffman({'c': 3, 'd': 4})
        assert codes == {'c': '0', 'd': '1'}

    def test_three_letters(self):
        codes = huffman({'a': 1, 'b': 2, 'c': 5})
        assert codes == {'a': '00', 'b': '01', 'c': '1'}

    def test_equal_frequencies(self):
        codes = huffman({'a': 1, 'b': 1})
        assert codes == {'a': '0', 'b': '1'}

    def test_complex_case(self):
        # freq 1 4 5 7 10
        #      c d b e  a
        #      ^ ^
        # c 0
        # d 1
        # -
        # 5  5 7 10
        # b cd e  a
        # ^ ^^
        # b 0
        # c 1 0
        # d 1 1
        # -
        # 7 10  10
        # e  a bcd
        # ^  ^
        # a 1
        # b   0
        # c   01
        # d   11
        # e 0
        # -
        #  10 17
        # bcd ae
        # ^^^ ^^
        # a 1 1
        # b 0 0
        # c 0 01
        # d 0 11
        # e 1 0
        codes = huffman({
            'a': 10, 'b': 5,
            'c': 1, 'd': 4,
            'e': 7
        })
        assert codes == {
            'a': '11', 'b': '00',
            'c': '010', 'd': '011',
            'e': '10'
        }

    def test_corner_cases(self):
        assert huffman({}) == {}
        assert huffman({'a': 1}) == {'a': '0'}


class TestCompress:
    def test_interface(self):
        assert compress('') == ''

    def test_one_char(self):
        assert compress('a') == '0'

    def test_two_chars(self):
        # a 1
        # b 0
        assert compress('aba') == '101'


class TestEncodeTree:
    def test_interface(self):
        # len('0')
        assert tree_encode(['0']) == [1]

    def test_real_case(self):
        # len('0') len('10') len('110') len('111')
        tree = ['0', '10', '110', '111']
        codes = [1, 2, 3, 3]
        assert tree_encode(tree) == codes
