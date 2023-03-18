""" Algorithms of compression """

import doctest

class LZ77:
    """
    LZ77 Algorithm
    >>> lz_77_encoder = LZ77(5)
    >>> encoded = lz_77_encoder.encode("abacabacdbacacacd")
    >>> print(encoded)
    [(0, 0, 'a'), (0, 0, 'b'), (2, 1, 'c'), (4, 4, 'd'), (4, 3, 'a'), (2, 3, 'd')]
    >>> print(lz_77_encoder.decode(encoded))
    abacabacdbacacacd
    >>> encoded = lz_77_encoder.encode("abababababababbabababba")
    >>> print(encoded)
    [(0, 0, 'a'), (0, 0, 'b'), (2, 12, 'b'), (5, 4, 'a'), (4, 1, 'b'), (5, 1, '')]
    >>> print(lz_77_encoder.decode(encoded))
    abababababababbabababba
    >>> encoded = lz_77_encoder.encode("")
    >>> print(encoded)
    []
    >>> print(lz_77_encoder.decode(encoded))
    <BLANKLINE>
    """
    def __init__(self, buffer) -> None:
        self.buffer_len = buffer

    def decode(self, decoded):
        """ Decodes given message using LZ77 """
        message = ""
        for code in decoded:
            if code[0] == 0:
                message += code[2]
                continue
            remainder = code[1]%code[0]
            whole_part = code[1] // code[0]
            add_message = message[-code[0]:] * whole_part + message[-code[0]: -code[0] + remainder]
            message += add_message + code[2]
        return message

    def longest_match(self ,buffer, message):
        """ Finds longest match if message part and buffer """
        max_step = 0
        max_start = 0

        start = 0
        step = 0
        for index, letter_buf in enumerate(buffer):
            if letter_buf == message[0]:
                start = len(buffer) - index
                step = 1
                for index_message, letter in enumerate(message[1:]):
                    if not letter == buffer[(index_message + 1)%start + index]:
                        break
                    step += 1
                if max_step < step:
                    max_step = step
                    max_start = start

        return (0, 0) if not max_step else (max_start, max_step)

    def encode(self, message):
        """ Encodes message with LZ77 algorithm"""
        pos_cursor = 0
        buffer = ""
        encoded = []
        while pos_cursor != len(message):

            start, steps = self.longest_match(buffer, message[pos_cursor:])
            buffer += message[pos_cursor: pos_cursor + steps + 1]
            buffer = buffer[-self.buffer_len:]
            if (pos_cursor + steps) >= len(message):
                encoded.append((start, steps, ""))
                break
            encoded.append((start, steps, message[pos_cursor + steps]))
            pos_cursor += steps + 1
        return encoded

class LZW:
    """
    LZW Algorithm
    >>> lzw_encoder = LZW()
    >>> start_message = "abacabac"
    >>> dictionary, code = lzw_encoder.encode(start_message)
    >>> dictionary
    {'a': 0, 'b': 1, 'c': 2, 'ab': 3, 'ba': 4, 'ac': 5, 'ca': 6, 'aba': 7, 'ac ': 8}
    >>> code
    [0, 1, 0, 2, 3, 5]
    >>> message = lzw_encoder.decode(dictionary, code)
    >>> message
    'abacabac'
    >>> message == start_message
    True

    >>> start_message = "nasjdjsdfhj abfdh1hv h12vh 1h3 vg3g\
42g34v2g34v2gh34 v2g34 v4gh23vgb aasbhd asd"
    >>> dictionary, code = lzw_encoder.encode(start_message)
    >>> message = lzw_encoder.decode(dictionary, code)
    >>> message == start_message
    True

    >>> start_message = " "
    >>> dictionary, code = lzw_encoder.encode(start_message)
    >>> message = lzw_encoder.decode(dictionary, code)
    >>> message == start_message
    True
    """

    def decode(self, dictionary, code):
        """ Decodes message with LZW algorithm """
        message = ""
        for integer in code:
            message += list(dictionary.keys())[integer]
        return message

    def find_line(self, message, dictionary):
        """ Finds biggest line in dictionary """
        for index in range(1, len(message) + 1):
            if message[:index] == message[:index+1] or len(message) == 1:
                return message[:index] + " "
            if message[:index] in dictionary and message[:index+1] not in dictionary:
                return message[:index+1]

    def init_dictionary(self, message):
        """ Inits one unit dictionary """
        return {letter:index for index, letter in enumerate("".join(sorted(set(message))))}

    def encode(self, message):
        """ Encodes message using LZW algorithm """
        dictionary = self.init_dictionary(message)
        pos_cursor = 0
        code = []
        while True:
            line = self.find_line(message[pos_cursor:] , dictionary)
            if line is None:
                break
            code.append(dictionary[line[:-1]])
            dictionary[line] = len(dictionary)
            pos_cursor += len(line) - 1
        return dictionary, code

class HuffmanEncoder:
    """
    Huffman Algorithm
    >>> huffman_encoder = HuffmanEncoder()
    >>> huffman_encoder.encode_probabilities([0.4,0.18,0.1, 0.1, 0.07, 0.06, 0.05, 0.04])
    [(0.4, '1'), (0.18, '001'), (0.1, '011'), (0.1, '0000'),\
 (0.07, '0100'), (0.06, '0101'), (0.05, '00010'), (0.04, '00011')]
    >>> huffman_encoder.encode("text test 7342734y72y347 dbhfs dbfhbsdhf ")
    '100110111100000110011000101000001001101000101011000110100010101110011011001110100\
0101001100011010101100000000010010000110101011000010000010110010101000000000010001'
    >>> huffman_encoder.decode('1001101111000001100110001010000010011010001010\
11000110100010101110011011001110100010100110001101010110000000001001000011\
0101011000010000010110010101000000000010001')
    'text test 7342734y72y347 dbhfs dbfhbsdhf '
    """
    def __init__(self) -> None:
        """ Init Huffman Encoder """
        self.codes = []

    def find_probabilities(self, text):
        """ Finds probabilities for given text """
        probabilities = {}
        for char in text:
            if char not in probabilities:
                probabilities[char] = 0
            probabilities[char] += 1

        return [num/len(text) for num in probabilities.values()], [key for key in probabilities]

    def encode_with_codes(self, text):
        """ Encode text with codes """
        coded = ""
        key_list = list(self.codes.keys())
        val_list = list(self.codes.values())
        for element in text:
            coded += key_list[val_list.index(element)]
        return coded

    def encode(self, text):
        """ Encodes message with five"""
        probabilities, alphabet = self.find_probabilities(text)
        codes = self.encode_probabilities(probabilities)
        self.codes = {element[0][1]:element[1] for element in list(zip(codes, alphabet))}

        return self.encode_with_codes(text)

    def encode_probabilities(self, probabilities):
        """ Encodes alphabet based on probabilies """
        probabilities = sorted(probabilities, reverse=True)
        if len(probabilities) == 2:
            return [(probabilities[0], "0"), (probabilities[1], "1")]

        num1 = probabilities.pop()
        num2 = probabilities.pop()

        codes = self.encode_probabilities(probabilities + [num1 + num2])
        find_first =  next((element for element in codes if element[0] == num1+num2), None)

        codes.append((num2, find_first[1] + "0"))
        codes.append((num1, find_first[1] + "1"))
        codes.remove(find_first)

        return codes

    def decode(self, code):
        """ Decodes message using huffman algorithm """
        i_1 = 0
        i_2 = 0
        decoded_text = ""
        while i_2 != len(code):
            i_2 += 1
            if code[i_1:i_2] in self.codes:
                decoded_text += self.codes[code[i_1:i_2]]
                i_1 = i_2
        return decoded_text

class DeflateEncoder:
    """
    Deflate algorithm encoder
    >>> deflate_encoder = DeflateEncoder(5)
    >>> code = deflate_encoder.encode(" q, ()82rkwyy gq4")
    >>> deflate_encoder.decode(code)
    ' q, ()82rkwyy gq4'
    """
    def __init__(self, buffer) -> None:
        """ Inits deflate encoder """
        self.haffman_encoder = HuffmanEncoder()
        self.lz77_encoder = LZ77(buffer)

    def encode(self, text):
        """ Encodes message using deflate algoithm """
        coded = repr(self.lz77_encoder.encode(text))\
        .replace(", ", ",,").replace("),,(", ",,")[2:-2]
        return self.haffman_encoder.encode(coded)

    def divide_in_three(self, list_divide):
        """ Generator which divides list in three """
        index = 0
        while index < len(list_divide):
            yield [int(list_divide[index]),
                 int(list_divide[index + 1]), list_divide[index + 2][1:-1]]
            index += 3

    def decode(self, code):
        """ Decodes message using Deflate algorithm """
        decoded = self.haffman_encoder.decode(code)
        codes = list(self.divide_in_three(decoded.split(",,")))
        return self.lz77_encoder.decode(codes)

doctest.testmod()
