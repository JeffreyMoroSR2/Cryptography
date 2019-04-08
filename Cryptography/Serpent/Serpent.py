import textwrap
from math import sqrt

class Serpent(object):
    def __init__(self, key_):
        self.temp = 0
        self.key = key_ & 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

    def Enc(self, temp_):
        self.temp = temp_ & 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

        self.PblockBegin()
        self.Round()
        self.PblockEnd()
        print(self.temp)

    def Dec(self, temp_):
        self.temp = temp_ & 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

        self.PblockBegin()
        self.DecRound()
        self.PblockEnd()
        print(self.temp)

    def PblockBegin(self):
        if self.temp.bit_length() < 128:
            self.temp = self.temp << (128 - self.temp.bit_length())

        #Робота з рядками!!! Замінити на побітові зсуви!!!
        arr = [0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99, 4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70,
               102, 7, 39, 71, 103, 8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107, 12, 44, 76, 108,
               13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111, 16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19,
               51, 83, 115, 20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119, 24, 56, 88, 120, 25, 57,
               89, 121, 26, 58, 90, 122, 27, 59, 91, 123, 28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95,
               127]

        self.temp = bin(self.temp)[2:]
        mylist = list(self.temp)
        self.temp = [mylist[i] for i in arr]
        self.temp = '0b' + ''.join(self.temp)
        self.temp = int(self.temp, 2)

    def PblockEnd(self):
        if self.temp.bit_length() < 128:
            self.temp = self.temp << (128 - self.temp.bit_length())

        # Робота з рядками!!! Замінити на побітові зсуви!!!
        arr = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100,
               104, 108, 112, 116, 120, 124, 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73,
               77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46,
               50, 54, 58, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126, 3, 7, 11, 15, 19,
               23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119,
               123, 127]

        self.temp = bin(self.temp)[2:]
        mylist = list(self.temp)
        self.temp = [mylist[i] for i in arr]
        self.temp = '0b' + ''.join(self.temp)
        self.temp = int(self.temp, 2)

    def Round(self):

        for i in range(32):
            self.round_number = i
            self.round_key = self.key_gen()

            self.temp = self.temp ^ self.round_key
            self.temp = self.Sbox(self.temp, self.round_number)

            arr = textwrap.wrap(bin(self.temp)[2:], 32)
            self.temp = self.linear_transform(int(arr[0], 2), int(arr[1], 2), int(arr[2], 2), int(arr[3], 2))

    def DecRound(self):
        for i in range(32):
            self.round_number = i
            self.round_key = self.key_gen()

            self.temp = self.temp ^ self.round_key
            self.temp = self.InvSbox(self.temp, self.round_number)

            arr = textwrap.wrap(bin(self.temp)[2:], 32)
            self.temp = self.linear_transform(int(arr[0], 2), int(arr[1], 2), int(arr[2], 2), int(arr[3], 2))

    def Sbox(self, block, round_number):
        if block.bit_length() < 128:
            block = block << (128 - block.bit_length())


        S = [[3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12], [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],
             [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2], [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],
             [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13], [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],
             [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0], [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]]


        block = textwrap.wrap(bin(block)[2:], 4)
        arr = []

        for i in block:
            i = int(i, 2)
            if round_number > 7:
                round_number = round_number % 8
            i = S[round_number][i]
            if i.bit_length() < 4:
                i = i << (4 - i.bit_length())
            arr.append(bin(i)[2:])

        block = arr
        block = int(''.join(block), 2)

        return block

    def InvSbox(self, block, round_number):
        if block.bit_length() < 128:
            block = block << (128 - block.bit_length())

        S = [[13, 3, 11, 0, 10, 6, 5, 12, 1, 14, 4, 7, 15, 9, 8, 2,], [5, 8, 2, 14, 15, 6, 12, 3, 11, 4, 7, 9, 1, 13, 10, 0],
             [12, 9, 15, 4, 11, 14, 1, 2, 0, 3, 6, 13, 5, 8, 10, 7], [0, 9, 10, 7, 11, 14, 6, 13, 3, 5, 12, 2, 4, 8, 15, 1],
             [5, 0, 8, 3, 10, 9, 7, 14, 2, 12, 11, 6, 4, 15, 13, 1], [8, 15, 2, 9, 4, 1, 13, 14, 11, 6, 5, 3, 7, 12, 10, 0],
             [15, 10, 1, 13, 5, 3, 6, 0, 4, 9, 14, 7, 2, 12, 8, 11], [3, 0, 6, 13, 9, 14, 15, 8, 5, 12, 11, 7, 10, 1, 4, 2]]

        block = textwrap.wrap(bin(block)[2:], 4)
        arr = []

        for i in block:
            i = int(i, 2)
            if round_number > 7:
                round_number = round_number % 8
            i = S[round_number][i]
            if i.bit_length() < 4:
                i = i << (4 - i.bit_length())
            arr.append(bin(i)[2:])

        block = arr
        block = int(''.join(block), 2)

        return block

    def linear_transform(self, W0, W1, W2, W3):
        W0 = self.Sdvig(W0, 13)
        W2 = self.Sdvig(W2, 3)
        W1 = W1 ^ W0 ^ W2
        W3 = W3 ^ W2 ^ self.Sdvig(W0, 3)
        W1 = self.Sdvig(W1, 1)
        W3 = self.Sdvig(W3, 7)
        W0 = W0 ^ W1 ^ W3
        W2 = W2 ^ W3 ^ self.Sdvig(W1, 7)
        W0 = self.Sdvig(W0, 5)
        W2 = self.Sdvig(W2, 22)

        return W0 + W1 + W2 + W3

    def Sdvig(self, x, y):
        #Цю функцію треба доробити
        x = ((x << y) & 0xffffffff) | (x >> 32-y) & 0xffffffff
        return x

    def key_gen(self):
        #Робота з рядками!
        if self.key.bit_length() < 256:
            self.key = int(bin(self.key) + '1', 2)
            self.key = self.key << (256 - self.key.bit_length())

        W = []
        W.append(textwrap.wrap(bin(self.key)[2:], 32))
        W = W[0]

        for i in range(8):
            W[i] = int(('0b' + ''.join(W[i])), 2)

        i = 8
        fi = (sqrt(5) + 1) / 2
        while i < 132:
            W.append(self.Sdvig((W[i - 8] ^ W[i - 5] ^ W[i - 3] ^ W[i - 1] ^ int(fi) ^ i), 11))
            i += 1

        K = []
        i = 0
        x = 0
        y = 0
        arr_round = [3, 2, 1, 0, 7, 6, 5, 4]

        while i < 132:
            z = bin(W[i])[2:] + bin(W[i + 1])[2:] + bin(W[i + 2])[2:] + bin(W[i + 3])[2:]
            if y > 7:
                y = 0
            K.append(self.Sbox(int(z, 2), arr_round[y]))
            x += 1
            i += 4
            y += 1

        return K[self.round_number]

serpent = Serpent(5)
serpent.Enc(100)
serpent.Dec(248565635277080605316196426476167364608)