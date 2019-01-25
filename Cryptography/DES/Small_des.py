
class small_des(object):
    def __init__(self, key_, round_amount_):
        self.temp = 0
        self.key = key_ & 0b11111111
        self.round_amount = round_amount_
        self.round_key = self.key_gen()

    def Enc(self, temp_):
        self.temp = temp_ & 0b11111111

        self.PblockBegin()

        i = 0
        while i < self.round_amount:
            self.Round(self.round_key[i])
            i = i + 1
            print('\t', self.temp)
        self.ChangeLeftRight()

        self.PblockEnd()

        return self.temp

    def Dec(self, temp_):
        self.temp = temp_ & 0b11111111

        self.PblockBegin()

        i = 0
        while i < self.round_amount:
            self.Round(self.round_key[self.round_amount - i - 1])
            i = i + 1
            print('\t', self.temp)
        self.ChangeLeftRight()

        self.PblockEnd()

        return self.temp

    def PblockBegin(self):
        self.temp = ((self.temp & 0b00000001) << 7) | \
                    ((self.temp & 0b00001000) << 3) | \
                    ((self.temp & 0b01000000) >> 1) | \
                    ((self.temp & 0b10000000) >> 3) | \
                    ((self.temp & 0b00000100) << 1) | \
                    ((self.temp & 0b00100000) >> 3) | \
                    ((self.temp & 0b00010000) >> 3) | \
                    ((self.temp & 0b00000010) >> 1)

    def PblockEnd(self):
        self.temp = ((self.temp & 0b10000000) >> 7) | \
                    ((self.temp & 0b01000000) >> 3) | \
                    ((self.temp & 0b00100000) >> 1) | \
                    ((self.temp & 0b00010000) << 3) | \
                    ((self.temp & 0b00001000) >> 1) | \
                    ((self.temp & 0b00000100) << 3) | \
                    ((self.temp & 0b00000010) << 3) | \
                    ((self.temp & 0b00000001) << 1)

    def Round(self, round_key):
        left = ((self.temp & 0b11110000) >> 4)
        right = ((self.temp & 0b00001111) >> 0)
        tempF = self.FunctionF(right, round_key)
        left = left ^ tempF
        self.temp = (right << 4) | left

    def FunctionF(self, right, round_key):
        result = right ^ round_key
        result = ((result & 0b1110) >> 1) | \
                 ((result & 0b0001) << 3)
        return result

    def ChangeLeftRight(self):
        self.temp = ((self.temp & 0b11110000) >> 4) | \
                    ((self.temp & 0b00001111) << 4)

    def key_gen(self):
        key_temp = self.key
        key_list = []
        i = 0
        while i < self.round_amount:
            key_temp = ((key_temp & 0b11111110) >> 1) | \
                       ((key_temp & 0b00000001) << 7)
            round_key = key_temp & 0b1111
            key_list.append(round_key)
            i = i + 1
        print(key_list)
        return key_list



a = 1
print(f'a = {a}')
key = 174
round_amount = 11
DES = small_des(key_=key, round_amount_=round_amount)
b = DES.Enc(a)
print(f'b = {b}')
c = DES.Dec(b)
print(f'c = {c}')