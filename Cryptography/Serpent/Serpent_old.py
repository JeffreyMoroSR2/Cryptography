import textwrap, math

class Serpent(object):
    def __init__(self, key_, a, round_amount_=32):
        self.temp = 0
        self.key = key_ & 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
        self.round_amount = round_amount_
        self.a = a


    def PblockBegin(self, p=5):
        a = self.a
        if p !=5:
            a = p

        if len(bin(a)) < 130:
            g = 130 - len(bin(a))
            g = g * '0'
            a = bin(a)[2:] + g
        else:
            a = bin(a)[2:]

        arr = [0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99, 4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70, 102, 7, 39, 71, 103, 8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107, 12, 44, 76, 108, 13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111, 16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19, 51, 83, 115, 20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119, 24, 56, 88, 120, 25, 57, 89, 121, 26, 58, 90, 122, 27, 59, 91, 123, 28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95, 127]
        mylist = list(a)
        a = [mylist[i] for i in arr]
        a = '0b' + ''.join(a)
        a = int(a, 2)
        self.a = a


    def PblockEnd(self):
        a = self.a
        # Кінцева перестановка
        if len(bin(a)) < 130:
            g = 130 - len(bin(a))
            g = g * '0'
            a = bin(a)[2:] + g
        else:
            a = bin(a)[2:]

        arr = []

        b = 0
        i = 0
        j = 0

        while j < 16:
            i = 0
            if j == 4:
                b = 1
            elif j == 8:
                b = 2
            elif j == 12:
                b = 3
            j += 1
            while i < 8:
                arr.append(b)
                b += 4
                i += 1

        mylist = list(a)
        a = [mylist[i] for i in arr]
        a = '0b' + ''.join(a)
        a = int(a, 2)
        self.a = a

    def Round(self):
        self.PblockBegin()
        self.PblockEnd()
        self.key_gen()

        #XOR
        self.temp = self.a ^ self.key
        self.temp = bin(self.temp)[2:]

        #Таблична заміна(покищо тільки для S0)
        self.temp = textwrap.wrap(self.temp, 4)


        S0 = [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12]
        S1 = [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4]
        S2 = [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2]
        S3 = [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14]
        S4 = [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13]
        S5 = [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1]
        S6 = [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0]
        S7 = [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]


        arr = []

        for i in self.temp:
            i = int(i, 2)
            i = S0[i]
            arr.append(i)

        self.temp = arr


        arr = []
        for i in self.temp:
            if len(bin(i)[2:]) < 4:
                g = 4 - len(bin(i)[2:])
                g = g * '0'
                i = g + bin(i)[2:]
                arr.append(i)
            else:
                arr.append(bin(i)[2:])



        self.temp = ''.join(arr)



    def Sbox(self, x_ = 100, Sbox_index = 0):
        Sbox = [
            [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],
            [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],
            [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2],
            [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],
            [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13],
            [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],
            [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0],
            [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]
        ]
        x = x_ & 0xffffffff
        y = Sbox[Sbox_index][(x >> 28) & 0xf] << 28 | \
            Sbox[Sbox_index][(x >> 24) & 0xf] << 24 | \
            Sbox[Sbox_index][(x >> 20) & 0xf] << 20 | \
            Sbox[Sbox_index][(x >> 16) & 0xf] << 16 | \
            Sbox[Sbox_index][(x >> 12) & 0xf] << 12 | \
            Sbox[Sbox_index][(x >> 8) & 0xf] << 8 | \
            Sbox[Sbox_index][(x >> 4) & 0xf] << 4 | \
            Sbox[Sbox_index][(x >> 0) & 0xf] << 0

        return y




    def linear_transform(self):
        pass

    def Sdvig(self, x, y):
        x = ((x << y) & 0xffffffff) | (x >> 32-y) & 0xffffffff
        return x

    def key_gen(self):

        #Розширення ключа
        if len(bin(self.key)) < 258:
            g = 255 - len(bin(self.key))
            g = g * '0'
            self.key = bin(self.key)[2:] + '1' + g + '00'
        #Вибір підключів із ключа
        self.key = textwrap.wrap(self.key, 32)
        W = self.key
        print(W)
        fi = (math.sqrt(5) + 1) / 2
        for i in range (131):
            h1 = int(W[i], 2)
            h2 = int(W[i + 3], 2)
            h3 = int(W[i + 5], 2)
            h4 = int(W[i + 7], 2)
            H = h1 + h2 + h3 + h4 + 0x9e3779b9 + i

            W_temp = self.Sdvig(H, 11)
            W_temp = bin(W_temp)[2:]
            W.append(W_temp)
            #W[8 + i] = (int(W[i], 2) + int(W[i + 3], 2) + int(W[i + 5], 2) + int(W[i + 7], 2) + int(fi) + i) << 11 & 0xffffffff


        for i in range (131):
            k1 = int(W[4*i], 2)
            k2 = int(W[4*i + 1], 2)
            k3 = int(W[4*i + 2], 2)
            k4 = int(W[4*i + 3], 2)

            k1 = self.Sbox(k1, 0)
            k2 = self.Sbox(k2, 0)
            k3 = self.Sbox(k3, 0)
            k4 = self.Sbox(k4, 0)

            K = k1 + k2 + k3 + k4
            K = self.PblockBegin(K)
            print(K)







a = 1002
key = 128
serpent = Serpent(key, a)
serpent.key_gen()