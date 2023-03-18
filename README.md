# Алгоритми стиску
### LZ77 Algorithm

LZ77 (Lempel-Ziv-1977) — це проста, але напрочуд ефективна форма стиснення даних, яка використовує зовсім інший підхід, ніж кодування Хаффмана. LZ77 — це метод, заснований на словнику, що означає, що він намагається стиснути дані, кодуючи довгі рядки символів, які називаються фразами, як маленькі маркери, які посилаються на записи в словнику. Стиснення досягається використанням відносно невеликих токенів замість довших фраз, які кілька разів з’являються в даних. Як і у випадку з кодуванням Хаффмана, важливо розуміти, що символ не обов’язково є символом тексту: символом може бути будь-яка кількість даних, яку ми виберемо, але часто він коштує один байт.

```
class LZ77:
    decode(decoded) - Decodes given message
    longest_match(buffer, message) - Finds longest match if message part and buffer
    encode(message) - Encodes message
```



### LZW Algorithm

Алгоритм LZW є дуже поширеним методом стиснення. Цей алгоритм зазвичай використовується у форматі GIF і, за бажанням, у форматах PDF і TIFF.Стиснення LZW працює шляхом зчитування послідовності символів, групування символів у рядки та перетворення рядків у коди. Оскільки коди займають менше місця, ніж рядки, які вони замінюють, ми отримуємо стиснення.

Наша реалізаці алгоритсу LZW має такі методи:
```
class LZW:
    decode(dictionary, code) - Decodes message with LZW algorithm
    find_line( message, dictionary) - Finds biggest line in dictionary
    init_dictionary(message) - Inits one unit dictionary
    encode(message) - Encodes message 
```
### Huffman Algorithm

Huffman coding is a lossless data compression algorithm. The idea is to assign variable-length codes to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters. 
The variable-length codes assigned to input characters are Prefix Codes, means the codes (bit sequences) are assigned in such a way that the code assigned to one character is not the prefix of code assigned to any other character. This is how Huffman Coding makes sure that there is no ambiguity when decoding the generated bitstream. 

```
class HuffmanEncoder:
    find_probabilities(text) - Finds probabilities for given text
    encode_with_codes(text) - Encode text with codes
    encode(text) - Encodes message with five
    encode_probabilities(probabilities) - Encodes alphabet based on probabilies
    decode(code) - Decodes message using huffman algorithm
```

### Deflate Algorithm

In computing, Deflate (stylized as DEFLATE) is a lossless data compression file format that uses a combination of LZ77 and Huffman coding.

```
class DeflateEncoder:
    encode(text) - Encodes message using deflate algoithm
    divide_in_three(list_divide) - Generator which divides list in three
    decode(code) - Decodes message using Deflate algorithm
```

Algorithms - laba.py

Analysys - analysys.ipynb
