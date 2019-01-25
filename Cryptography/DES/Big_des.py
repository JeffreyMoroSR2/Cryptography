
class small_des(object):
    def __init__(self, key_, round_amount_):
        self.temp = 0
        self.key = key_ & 0b11111111111111111111111111111111111111111111111111111111
        self.round_amount = round_amount_
        self.round_key = self.key_gen()

    def Enc(self, temp_):
        self.temp = temp_ & 0b1111111111111111111111111111111111111111111111111111111111111111

        self.PblockBegin()

        i = 0
        while i < self.round_amount:
            self.Round(self.round_key[i])
            i = i + 1
            #print('\t', self.temp)
        self.ChangeLeftRight()

        self.PblockEnd()

        return self.temp

    def Dec(self, temp_):
        self.temp = temp_ & 0b1111111111111111111111111111111111111111111111111111111111111111

        self.PblockBegin()

        i = 0
        while i < self.round_amount:
            self.Round(self.round_key[self.round_amount - i - 1])
            i = i + 1
            #print('\t', self.temp)
        self.ChangeLeftRight()

        self.PblockEnd()

        return self.temp

    def PblockBegin(self):
        self.temp = ((self.temp & 0b0000000000000000000000000000000000000000000000000000000001000000) << 57) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000100000000000000) << 48) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000010000000000000000000000) << 39) | \
                    ((self.temp & 0b0000000000000000000000000000000001000000000000000000000000000000) << 30) | \
                    ((self.temp & 0b0000000000000000000000000100000000000000000000000000000000000000) << 21) | \
                    ((self.temp & 0b0000000000000000010000000000000000000000000000000000000000000000) << 12) | \
                    ((self.temp & 0b0000000001000000000000000000000000000000000000000000000000000000) << 3) | \
                    ((self.temp & 0b0100000000000000000000000000000000000000000000000000000000000000) >> 6) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000010000) << 51) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000001000000000000) << 42) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000100000000000000000000) << 33) | \
                    ((self.temp & 0b0000000000000000000000000000000000010000000000000000000000000000) << 24) | \
                    ((self.temp & 0b0000000000000000000000000001000000000000000000000000000000000000) << 15) | \
                    ((self.temp & 0b0000000000000000000100000000000000000000000000000000000000000000) << 6) | \
                    ((self.temp & 0b0000000000010000000000000000000000000000000000000000000000000000) >> 3) | \
                    ((self.temp & 0b0001000000000000000000000000000000000000000000000000000000000000) >> 12) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000000100) << 45) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000010000000000) << 36) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000001000000000000000000) << 27) | \
                    ((self.temp & 0b0000000000000000000000000000000000000100000000000000000000000000) << 18) | \
                    ((self.temp & 0b0000000000000000000000000000010000000000000000000000000000000000) << 9) | \
                    ((self.temp & 0b0000000000000000000001000000000000000000000000000000000000000000) << 0) | \
                    ((self.temp & 0b0000000000000100000000000000000000000000000000000000000000000000) >> 9) | \
                    ((self.temp & 0b0000010000000000000000000000000000000000000000000000000000000000) >> 18) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000000001) << 39) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000100000000) << 30) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000010000000000000000) << 21) | \
                    ((self.temp & 0b0000000000000000000000000000000000000001000000000000000000000000) << 12) | \
                    ((self.temp & 0b0000000000000000000000000000000100000000000000000000000000000000) << 3) | \
                    ((self.temp & 0b0000000000000000000000010000000000000000000000000000000000000000) >> 6) | \
                    ((self.temp & 0b0000000000000001000000000000000000000000000000000000000000000000) >> 15) | \
                    ((self.temp & 0b0000000100000000000000000000000000000000000000000000000000000000) >> 24) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000010000000) << 24) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000001000000000000000) << 15) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000100000000000000000000000) << 6) | \
                    ((self.temp & 0b0000000000000000000000000000000010000000000000000000000000000000) >> 3) | \
                    ((self.temp & 0b0000000000000000000000001000000000000000000000000000000000000000) >> 12) | \
                    ((self.temp & 0b0000000000000000100000000000000000000000000000000000000000000000) >> 21) | \
                    ((self.temp & 0b0000000010000000000000000000000000000000000000000000000000000000) >> 30) | \
                    ((self.temp & 0b1000000000000000000000000000000000000000000000000000000000000000) >> 39) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000100000) << 18) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000010000000000000) << 9) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000001000000000000000000000) << 0) | \
                    ((self.temp & 0b0000000000000000000000000000000000100000000000000000000000000000) >> 9) | \
                    ((self.temp & 0b0000000000000000000000000010000000000000000000000000000000000000) >> 18) | \
                    ((self.temp & 0b0000000000000000001000000000000000000000000000000000000000000000) >> 27) | \
                    ((self.temp & 0b0000000000100000000000000000000000000000000000000000000000000000) >> 36) | \
                    ((self.temp & 0b0010000000000000000000000000000000000000000000000000000000000000) >> 45) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000001000) << 12) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000100000000000) << 3) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000010000000000000000000) >> 6) | \
                    ((self.temp & 0b0000000000000000000000000000000000001000000000000000000000000000) >> 15) | \
                    ((self.temp & 0b0000000000000000000000000000100000000000000000000000000000000000) >> 24) | \
                    ((self.temp & 0b0000000000000000000010000000000000000000000000000000000000000000) >> 33) | \
                    ((self.temp & 0b0000000000001000000000000000000000000000000000000000000000000000) >> 42) | \
                    ((self.temp & 0b0000100000000000000000000000000000000000000000000000000000000000) >> 51) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000000010) << 6) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000001000000000) >> 3) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000100000000000000000) >> 12) | \
                    ((self.temp & 0b0000000000000000000000000000000000000010000000000000000000000000) >> 21) | \
                    ((self.temp & 0b0000000000000000000000000000001000000000000000000000000000000000) >> 30) | \
                    ((self.temp & 0b0000000000000000000000100000000000000000000000000000000000000000) >> 39) | \
                    ((self.temp & 0b0000000000000010000000000000000000000000000000000000000000000000) >> 48) | \
                    ((self.temp & 0b0000001000000000000000000000000000000000000000000000000000000000) >> 57)



    def PblockEnd(self):
        self.temp = ((self.temp & 0b0000000000000000000000000000000000000001000000000000000000000000) << 39) | \
                    ((self.temp & 0b0000000100000000000000000000000000000000000000000000000000000000) << 6) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000010000000000000000) << 45) | \
                    ((self.temp & 0b0000000000000001000000000000000000000000000000000000000000000000) << 12) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000100000000) << 51) | \
                    ((self.temp & 0b0000000000000000000000010000000000000000000000000000000000000000) << 18) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000000001) << 57) | \
                    ((self.temp & 0b0000000000000000000000000000000100000000000000000000000000000000) << 24) | \
                    ((self.temp & 0b0000000000000000000000000000000000000010000000000000000000000000) << 30) | \
                    ((self.temp & 0b0000001000000000000000000000000000000000000000000000000000000000) >> 3) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000100000000000000000) << 36) | \
                    ((self.temp & 0b0000000000000010000000000000000000000000000000000000000000000000) << 3) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000001000000000) << 42) | \
                    ((self.temp & 0b0000000000000000000000100000000000000000000000000000000000000000) << 9) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000000010) << 48) | \
                    ((self.temp & 0b0000000000000000000000000000001000000000000000000000000000000000) << 15) | \
                    ((self.temp & 0b0000000000000000000000000000000000000100000000000000000000000000) << 21) | \
                    ((self.temp & 0b0000010000000000000000000000000000000000000000000000000000000000) >> 12) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000001000000000000000000) << 27) | \
                    ((self.temp & 0b0000000000000100000000000000000000000000000000000000000000000000) >> 6) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000010000000000) << 33) | \
                    ((self.temp & 0b0000000000000000000001000000000000000000000000000000000000000000) << 0) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000000100) << 39) | \
                    ((self.temp & 0b0000000000000000000000000000010000000000000000000000000000000000) << 6) | \
                    ((self.temp & 0b0000000000000000000000000000000000001000000000000000000000000000) << 12) | \
                    ((self.temp & 0b0000100000000000000000000000000000000000000000000000000000000000) >> 21) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000010000000000000000000) << 18) | \
                    ((self.temp & 0b0000000000001000000000000000000000000000000000000000000000000000) >> 15) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000100000000000) << 24) | \
                    ((self.temp & 0b0000000000000000000010000000000000000000000000000000000000000000) >> 9) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000001000) << 30) | \
                    ((self.temp & 0b0000000000000000000000000000100000000000000000000000000000000000) >> 3) | \
                    ((self.temp & 0b0000000000000000000000000000000000010000000000000000000000000000) << 3) | \
                    ((self.temp & 0b0001000000000000000000000000000000000000000000000000000000000000) >> 30) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000100000000000000000000) << 9) | \
                    ((self.temp & 0b0000000000010000000000000000000000000000000000000000000000000000) >> 24) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000001000000000000) << 15) | \
                    ((self.temp & 0b0000000000000000000100000000000000000000000000000000000000000000) >> 18) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000010000) << 21) | \
                    ((self.temp & 0b0000000000000000000000000001000000000000000000000000000000000000) >> 12) | \
                    ((self.temp & 0b0000000000000000000000000000000000100000000000000000000000000000) >> 6) | \
                    ((self.temp & 0b0010000000000000000000000000000000000000000000000000000000000000) >> 39) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000001000000000000000000000) << 0) | \
                    ((self.temp & 0b0000000000100000000000000000000000000000000000000000000000000000) >> 33) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000010000000000000) << 6) | \
                    ((self.temp & 0b0000000000000000001000000000000000000000000000000000000000000000) >> 27) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000000100000) << 12) | \
                    ((self.temp & 0b0000000000000000000000000010000000000000000000000000000000000000) >> 21) | \
                    ((self.temp & 0b0000000000000000000000000000000001000000000000000000000000000000) >> 15) | \
                    ((self.temp & 0b0100000000000000000000000000000000000000000000000000000000000000) >> 48) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000010000000000000000000000) >> 9) | \
                    ((self.temp & 0b0000000001000000000000000000000000000000000000000000000000000000) >> 42) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000100000000000000) >> 3) | \
                    ((self.temp & 0b0000000000000000010000000000000000000000000000000000000000000000) >> 36) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000001000000) << 3) | \
                    ((self.temp & 0b0000000000000000000000000100000000000000000000000000000000000000) >> 30) | \
                    ((self.temp & 0b0000000000000000000000000000000010000000000000000000000000000000) >> 24) | \
                    ((self.temp & 0b1000000000000000000000000000000000000000000000000000000000000000) >> 57) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000100000000000000000000000) >> 18) | \
                    ((self.temp & 0b0000000010000000000000000000000000000000000000000000000000000000) >> 51) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000001000000000000000) >> 12) | \
                    ((self.temp & 0b0000000000000000100000000000000000000000000000000000000000000000) >> 45) | \
                    ((self.temp & 0b0000000000000000000000000000000000000000000000000000000010000000) >> 6) | \
                    ((self.temp & 0b0000000000000000000000001000000000000000000000000000000000000000) >> 39)



    def Round(self, round_key):
        left = ((self.temp & 0b1111111111111111111111111111111100000000000000000000000000000000) >> 32)
        right = ((self.temp & 0b0000000000000000000000000000000011111111111111111111111111111111) >> 0)
        tempF = self.FunctionF(right, round_key)
        left = left ^ tempF
        self.temp = (right << 32) | left

    def FunctionF(self, right, round_key):
        # P-block expansion
        a = right
        a = bin(a) + '0000000000000000'
        a = int(a, 2)
        right = a

        right = ((right & 0b000000000000000000000000000000010000000000000000) << 31) | \
                ((right & 0b111110000000000000000000000000000000000000000000) >> 1) | \
                ((right & 0b000110000000000000000000000000000000000000000000) >> 3) | \
                ((right & 0b000001111000000000000000000000000000000000000000) >> 3) | \
                ((right & 0b000000011000000000000000000000000000000000000000) >> 5) | \
                ((right & 0b000000000111100000000000000000000000000000000000) >> 5) | \
                ((right & 0b000000000001100000000000000000000000000000000000) >> 7) | \
                ((right & 0b000000000000011110000000000000000000000000000000) >> 7) | \
                ((right & 0b000000000000000110000000000000000000000000000000) >> 9) | \
                ((right & 0b000000000000000001111000000000000000000000000000) >> 9) | \
                ((right & 0b000000000000000000011000000000000000000000000000) >> 11) | \
                ((right & 0b000000000000000000000111100000000000000000000000) >> 11) | \
                ((right & 0b000000000000000000000001100000000000000000000000) >> 13) | \
                ((right & 0b000000000000000000000000011110000000000000000000) >> 13) | \
                ((right & 0b000000000000000000000000000110000000000000000000) >> 15) | \
                ((right & 0b000000000000000000000000000001110000000000000000) >> 15) | \
                ((right & 0b100000000000000000000000000000000000000000000000) >> 47)

        # XOR
        result = right ^ round_key

        if(len(bin(result)[2:]) < 48):
            a = 48 - len(bin(result)[2:])
            result = (a * '0') + bin(result)[2:]
        else:
            result = bin(result)[2:]
        # S-box
        # S1
        test = (result)[:-42]
        line = test[0] + test[-1]
        column = test[1:-1]

        if (line == '00' and column == '0000'):
            result1 = 14
        elif (line == '00' and column == '0001'):
            result1 = 4
        elif (line == '00' and column == '0010'):
            result1 = 13
        elif (line == '00' and column == '0011'):
            result1 = 1
        elif (line == '00' and column == '0100'):
            result1 = 2
        elif (line == '00' and column == '0101'):
            result1 = 15
        elif (line == '00' and column == '0110'):
            result1 = 11
        elif (line == '00' and column == '0111'):
            result1 = 8
        elif (line == '00' and column == '1000'):
            result1 = 3
        elif (line == '00' and column == '1001'):
            result1 = 10
        elif (line == '00' and column == '1010'):
            result1 = 6
        elif (line == '00' and column == '1011'):
            result1 = 12
        elif (line == '00' and column == '1100'):
            result1 = 5
        elif (line == '00' and column == '1101'):
            result1 = 9
        elif (line == '00' and column == '1110'):
            result1 = 0
        elif (line == '00' and column == '1111'):
            result1 = 7

        if (line == '01' and column == '0000'):
            result1 = 0
        elif (line == '01' and column == '0001'):
            result1 = 15
        elif (line == '01' and column == '0010'):
            result1 = 7
        elif (line == '01' and column == '0011'):
            result1 = 4
        elif (line == '01' and column == '0100'):
            result1 = 14
        elif (line == '01' and column == '0101'):
            result1 = 2
        elif (line == '01' and column == '0110'):
            result1 = 13
        elif (line == '01' and column == '0111'):
            result1 = 1
        elif (line == '01' and column == '1000'):
            result1 = 10
        elif (line == '01' and column == '1001'):
            result1 = 6
        elif (line == '01' and column == '1010'):
            result1 = 12
        elif (line == '01' and column == '1011'):
            result1 = 11
        elif (line == '01' and column == '1100'):
            result1 = 9
        elif (line == '01' and column == '1101'):
            result1 = 5
        elif (line == '01' and column == '1110'):
            result1 = 3
        elif (line == '01' and column == '1111'):
            result1 = 8

        if (line == '10' and column == '0000'):
            result1 = 4
        elif (line == '10' and column == '0001'):
            result1 = 1
        elif (line == '10' and column == '0010'):
            result1 = 14
        elif (line == '10' and column == '0011'):
            result1 = 8
        elif (line == '10' and column == '0100'):
            result1 = 13
        elif (line == '10' and column == '0101'):
            result1 = 6
        elif (line == '10' and column == '0110'):
            result1 = 2
        elif (line == '10' and column == '0111'):
            result1 = 11
        elif (line == '10' and column == '1000'):
            result1 = 15
        elif (line == '10' and column == '1001'):
            result1 = 12
        elif (line == '10' and column == '1010'):
            result1 = 9
        elif (line == '10' and column == '1011'):
            result1 = 7
        elif (line == '10' and column == '1100'):
            result1 = 3
        elif (line == '10' and column == '1101'):
            result1 = 10
        elif (line == '10' and column == '1110'):
            result1 = 5
        elif (line == '10' and column == '1111'):
            result1 = 0

        if (line == '11' and column == '0000'):
            result1 = 15
        elif (line == '11' and column == '0001'):
            result1 = 12
        elif (line == '11' and column == '0010'):
            result1 = 8
        elif (line == '11' and column == '0011'):
            result1 = 2
        elif (line == '11' and column == '0100'):
            result1 = 4
        elif (line == '11' and column == '0101'):
            result1 = 9
        elif (line == '11' and column == '0110'):
            result1 = 1
        elif (line == '11' and column == '0111'):
            result1 = 7
        elif (line == '11' and column == '1000'):
            result1 = 5
        elif (line == '11' and column == '1001'):
            result1 = 11
        elif (line == '11' and column == '1010'):
            result1 = 3
        elif (line == '11' and column == '1011'):
            result1 = 14
        elif (line == '11' and column == '1100'):
            result1 = 10
        elif (line == '11' and column == '1101'):
            result1 = 0
        elif (line == '11' and column == '1110'):
            result1 = 6
        elif (line == '11' and column == '1111'):
            result1 = 13

        # S2
        test = (result)[6:-36]
        line = test[0] + test[-1]
        column = test[1:-1]

        if (line == '00' and column == '0000'):
            result2 = 15
        elif (line == '00' and column == '0001'):
            result2 = 1
        elif (line == '00' and column == '0010'):
            result2 = 8
        elif (line == '00' and column == '0011'):
            result2 = 14
        elif (line == '00' and column == '0100'):
            result2 = 6
        elif (line == '00' and column == '0101'):
            result2 = 11
        elif (line == '00' and column == '0110'):
            result2 = 3
        elif (line == '00' and column == '0111'):
            result2 = 4
        elif (line == '00' and column == '1000'):
            result2 = 9
        elif (line == '00' and column == '1001'):
            result2 = 7
        elif (line == '00' and column == '1010'):
            result2 = 2
        elif (line == '00' and column == '1011'):
            result2 = 13
        elif (line == '00' and column == '1100'):
            result2 = 12
        elif (line == '00' and column == '1101'):
            result2 = 0
        elif (line == '00' and column == '1110'):
            result2 = 5
        elif (line == '00' and column == '1111'):
            result2 = 10

        if (line == '01' and column == '0000'):
            result2 = 3
        elif (line == '01' and column == '0001'):
            result2 = 13
        elif (line == '01' and column == '0010'):
            result2 = 4
        elif (line == '01' and column == '0011'):
            result2 = 7
        elif (line == '01' and column == '0100'):
            result2 = 15
        elif (line == '01' and column == '0101'):
            result2 = 2
        elif (line == '01' and column == '0110'):
            result2 = 8
        elif (line == '01' and column == '0111'):
            result2 = 14
        elif (line == '01' and column == '1000'):
            result2 = 12
        elif (line == '01' and column == '1001'):
            result2 = 0
        elif (line == '01' and column == '1010'):
            result2 = 1
        elif (line == '01' and column == '1011'):
            result2 = 10
        elif (line == '01' and column == '1100'):
            result2 = 6
        elif (line == '01' and column == '1101'):
            result2 = 9
        elif (line == '01' and column == '1110'):
            result2 = 11
        elif (line == '01' and column == '1111'):
            result2 = 5

        if (line == '10' and column == '0000'):
            result2 = 0
        elif (line == '10' and column == '0001'):
            result2 = 14
        elif (line == '10' and column == '0010'):
            result2 = 7
        elif (line == '10' and column == '0011'):
            result2 = 11
        elif (line == '10' and column == '0100'):
            result2 = 10
        elif (line == '10' and column == '0101'):
            result2 = 4
        elif (line == '10' and column == '0110'):
            result2 = 13
        elif (line == '10' and column == '0111'):
            result2 = 1
        elif (line == '10' and column == '1000'):
            result2 = 5
        elif (line == '10' and column == '1001'):
            result2 = 8
        elif (line == '10' and column == '1010'):
            result2 = 12
        elif (line == '10' and column == '1011'):
            result2 = 6
        elif (line == '10' and column == '1100'):
            result2 = 9
        elif (line == '10' and column == '1101'):
            result2 = 3
        elif (line == '10' and column == '1110'):
            result2 = 2
        elif (line == '10' and column == '1111'):
            result2 = 15

        if (line == '11' and column == '0000'):
            result2 = 13
        elif (line == '11' and column == '0001'):
            result2 = 8
        elif (line == '11' and column == '0010'):
            result2 = 10
        elif (line == '11' and column == '0011'):
            result2 = 1
        elif (line == '11' and column == '0100'):
            result2 = 3
        elif (line == '11' and column == '0101'):
            result2 = 15
        elif (line == '11' and column == '0110'):
            result2 = 4
        elif (line == '11' and column == '0111'):
            result2 = 2
        elif (line == '11' and column == '1000'):
            result2 = 11
        elif (line == '11' and column == '1001'):
            result2 = 6
        elif (line == '11' and column == '1010'):
            result2 = 7
        elif (line == '11' and column == '1011'):
            result2 = 12
        elif (line == '11' and column == '1100'):
            result2 = 0
        elif (line == '11' and column == '1101'):
            result2 = 5
        elif (line == '11' and column == '1110'):
            result2 = 14
        elif (line == '11' and column == '1111'):
            result2 = 9

        # S3
        test = (result)[12:-30]
        line = test[0] + test[-1]
        column = test[1:-1]

        if (line == '00' and column == '0000'):
            result3 = 10
        elif (line == '00' and column == '0001'):
            result3 = 0
        elif (line == '00' and column == '0010'):
            result3 = 9
        elif (line == '00' and column == '0011'):
            result3 = 14
        elif (line == '00' and column == '0100'):
            result3 = 6
        elif (line == '00' and column == '0101'):
            result3 = 3
        elif (line == '00' and column == '0110'):
            result3 = 15
        elif (line == '00' and column == '0111'):
            result3 = 5
        elif (line == '00' and column == '1000'):
            result3 = 1
        elif (line == '00' and column == '1001'):
            result3 = 13
        elif (line == '00' and column == '1010'):
            result3 = 7
        elif (line == '00' and column == '1011'):
            result3 = 11
        elif (line == '00' and column == '1100'):
            result3 = 12
        elif (line == '00' and column == '1101'):
            result3 = 4
        elif (line == '00' and column == '1110'):
            result3 = 2
        elif (line == '00' and column == '1111'):
            result3 = 8

        if (line == '01' and column == '0000'):
            result3 = 13
        elif (line == '01' and column == '0001'):
            result3 = 7
        elif (line == '01' and column == '0010'):
            result3 = 0
        elif (line == '01' and column == '0011'):
            result3 = 9
        elif (line == '01' and column == '0100'):
            result3 = 3
        elif (line == '01' and column == '0101'):
            result3 = 4
        elif (line == '01' and column == '0110'):
            result3 = 6
        elif (line == '01' and column == '0111'):
            result3 = 10
        elif (line == '01' and column == '1000'):
            result3 = 2
        elif (line == '01' and column == '1001'):
            result3 = 8
        elif (line == '01' and column == '1010'):
            result3 = 5
        elif (line == '01' and column == '1011'):
            result3 = 14
        elif (line == '01' and column == '1100'):
            result3 = 12
        elif (line == '01' and column == '1101'):
            result3 = 11
        elif (line == '01' and column == '1110'):
            result3 = 15
        elif (line == '01' and column == '1111'):
            result3 = 1

        if (line == '10' and column == '0000'):
            result3 = 13
        elif (line == '10' and column == '0001'):
            result3 = 6
        elif (line == '10' and column == '0010'):
            result3 = 4
        elif (line == '10' and column == '0011'):
            result3 = 9
        elif (line == '10' and column == '0100'):
            result3 = 8
        elif (line == '10' and column == '0101'):
            result3 = 15
        elif (line == '10' and column == '0110'):
            result3 = 3
        elif (line == '10' and column == '0111'):
            result3 = 0
        elif (line == '10' and column == '1000'):
            result3 = 11
        elif (line == '10' and column == '1001'):
            result3 = 1
        elif (line == '10' and column == '1010'):
            result3 = 2
        elif (line == '10' and column == '1011'):
            result3 = 12
        elif (line == '10' and column == '1100'):
            result3 = 5
        elif (line == '10' and column == '1101'):
            result3 = 10
        elif (line == '10' and column == '1110'):
            result3 = 14
        elif (line == '10' and column == '1111'):
            result3 = 7

        if (line == '11' and column == '0000'):
            result3 = 1
        elif (line == '11' and column == '0001'):
            result3 = 10
        elif (line == '11' and column == '0010'):
            result3 = 13
        elif (line == '11' and column == '0011'):
            result3 = 0
        elif (line == '11' and column == '0100'):
            result3 = 6
        elif (line == '11' and column == '0101'):
            result3 = 9
        elif (line == '11' and column == '0110'):
            result3 = 8
        elif (line == '11' and column == '0111'):
            result3 = 7
        elif (line == '11' and column == '1000'):
            result3 = 4
        elif (line == '11' and column == '1001'):
            result3 = 15
        elif (line == '11' and column == '1010'):
            result3 = 14
        elif (line == '11' and column == '1011'):
            result3 = 3
        elif (line == '11' and column == '1100'):
            result3 = 11
        elif (line == '11' and column == '1101'):
            result3 = 5
        elif (line == '11' and column == '1110'):
            result3 = 2
        elif (line == '11' and column == '1111'):
            result3 = 12

        # S4
        test = (result)[18:-24]
        line = test[0] + test[-1]
        column = test[1:-1]

        if (line == '00' and column == '0000'):
            result4 = 7
        elif (line == '00' and column == '0001'):
            result4 = 13
        elif (line == '00' and column == '0010'):
            result4 = 14
        elif (line == '00' and column == '0011'):
            result4 = 3
        elif (line == '00' and column == '0100'):
            result4 = 0
        elif (line == '00' and column == '0101'):
            result4 = 6
        elif (line == '00' and column == '0110'):
            result4 = 9
        elif (line == '00' and column == '0111'):
            result4 = 10
        elif (line == '00' and column == '1000'):
            result4 = 1
        elif (line == '00' and column == '1001'):
            result4 = 2
        elif (line == '00' and column == '1010'):
            result4 = 8
        elif (line == '00' and column == '1011'):
            result4 = 5
        elif (line == '00' and column == '1100'):
            result4 = 11
        elif (line == '00' and column == '1101'):
            result4 = 12
        elif (line == '00' and column == '1110'):
            result4 = 4
        elif (line == '00' and column == '1111'):
            result4 = 15

        if (line == '01' and column == '0000'):
            result4 = 13
        elif (line == '01' and column == '0001'):
            result4 = 8
        elif (line == '01' and column == '0010'):
            result4 = 11
        elif (line == '01' and column == '0011'):
            result4 = 5
        elif (line == '01' and column == '0100'):
            result4 = 6
        elif (line == '01' and column == '0101'):
            result4 = 15
        elif (line == '01' and column == '0110'):
            result4 = 0
        elif (line == '01' and column == '0111'):
            result4 = 3
        elif (line == '01' and column == '1000'):
            result4 = 4
        elif (line == '01' and column == '1001'):
            result4 = 7
        elif (line == '01' and column == '1010'):
            result4 = 2
        elif (line == '01' and column == '1011'):
            result4 = 12
        elif (line == '01' and column == '1100'):
            result4 = 1
        elif (line == '01' and column == '1101'):
            result4 = 10
        elif (line == '01' and column == '1110'):
            result4 = 14
        elif (line == '01' and column == '1111'):
            result4 = 9

        if (line == '10' and column == '0000'):
            result4 = 10
        elif (line == '10' and column == '0001'):
            result4 = 6
        elif (line == '10' and column == '0010'):
            result4 = 9
        elif (line == '10' and column == '0011'):
            result4 = 0
        elif (line == '10' and column == '0100'):
            result4 = 12
        elif (line == '10' and column == '0101'):
            result4 = 11
        elif (line == '10' and column == '0110'):
            result4 = 7
        elif (line == '10' and column == '0111'):
            result4 = 13
        elif (line == '10' and column == '1000'):
            result4 = 15
        elif (line == '10' and column == '1001'):
            result4 = 1
        elif (line == '10' and column == '1010'):
            result4 = 3
        elif (line == '10' and column == '1011'):
            result4 = 14
        elif (line == '10' and column == '1100'):
            result4 = 5
        elif (line == '10' and column == '1101'):
            result4 = 2
        elif (line == '10' and column == '1110'):
            result4 = 8
        elif (line == '10' and column == '1111'):
            result4 = 4

        if (line == '11' and column == '0000'):
            result4 = 3
        elif (line == '11' and column == '0001'):
            result4 = 15
        elif (line == '11' and column == '0010'):
            result4 = 0
        elif (line == '11' and column == '0011'):
            result4 = 6
        elif (line == '11' and column == '0100'):
            result4 = 10
        elif (line == '11' and column == '0101'):
            result4 = 1
        elif (line == '11' and column == '0110'):
            result4 = 13
        elif (line == '11' and column == '0111'):
            result4 = 8
        elif (line == '11' and column == '1000'):
            result4 = 9
        elif (line == '11' and column == '1001'):
            result4 = 4
        elif (line == '11' and column == '1010'):
            result4 = 5
        elif (line == '11' and column == '1011'):
            result4 = 11
        elif (line == '11' and column == '1100'):
            result4 = 12
        elif (line == '11' and column == '1101'):
            result4 = 7
        elif (line == '11' and column == '1110'):
            result4 = 2
        elif (line == '11' and column == '1111'):
            result4 = 14

        # S5
        test = (result)[24:-18]
        line = test[0] + test[-1]
        column = test[1:-1]

        if (line == '00' and column == '0000'):
            result5 = 2
        elif (line == '00' and column == '0001'):
            result5 = 12
        elif (line == '00' and column == '0010'):
            result5 = 4
        elif (line == '00' and column == '0011'):
            result5 = 1
        elif (line == '00' and column == '0100'):
            result5 = 7
        elif (line == '00' and column == '0101'):
            result5 = 10
        elif (line == '00' and column == '0110'):
            result5 = 11
        elif (line == '00' and column == '0111'):
            result5 = 6
        elif (line == '00' and column == '1000'):
            result5 = 8
        elif (line == '00' and column == '1001'):
            result5 = 5
        elif (line == '00' and column == '1010'):
            result5 = 3
        elif (line == '00' and column == '1011'):
            result5 = 15
        elif (line == '00' and column == '1100'):
            result5 = 13
        elif (line == '00' and column == '1101'):
            result5 = 0
        elif (line == '00' and column == '1110'):
            result5 = 14
        elif (line == '00' and column == '1111'):
            result5 = 9

        if (line == '01' and column == '0000'):
            result5 = 14
        elif (line == '01' and column == '0001'):
            result5 = 11
        elif (line == '01' and column == '0010'):
            result5 = 2
        elif (line == '01' and column == '0011'):
            result5 = 12
        elif (line == '01' and column == '0100'):
            result5 = 4
        elif (line == '01' and column == '0101'):
            result5 = 7
        elif (line == '01' and column == '0110'):
            result5 = 13
        elif (line == '01' and column == '0111'):
            result5 = 1
        elif (line == '01' and column == '1000'):
            result5 = 5
        elif (line == '01' and column == '1001'):
            result5 = 0
        elif (line == '01' and column == '1010'):
            result5 = 15
        elif (line == '01' and column == '1011'):
            result5 = 10
        elif (line == '01' and column == '1100'):
            result5 = 3
        elif (line == '01' and column == '1101'):
            result5 = 9
        elif (line == '01' and column == '1110'):
            result5 = 8
        elif (line == '01' and column == '1111'):
            result5 = 6

        if (line == '10' and column == '0000'):
            result5 = 4
        elif (line == '10' and column == '0001'):
            result5 = 2
        elif (line == '10' and column == '0010'):
            result5 = 1
        elif (line == '10' and column == '0011'):
            result5 = 11
        elif (line == '10' and column == '0100'):
            result5 = 10
        elif (line == '10' and column == '0101'):
            result5 = 13
        elif (line == '10' and column == '0110'):
            result5 = 7
        elif (line == '10' and column == '0111'):
            result5 = 8
        elif (line == '10' and column == '1000'):
            result5 = 15
        elif (line == '10' and column == '1001'):
            result5 = 9
        elif (line == '10' and column == '1010'):
            result5 = 12
        elif (line == '10' and column == '1011'):
            result5 = 5
        elif (line == '10' and column == '1100'):
            result5 = 6
        elif (line == '10' and column == '1101'):
            result5 = 3
        elif (line == '10' and column == '1110'):
            result5 = 0
        elif (line == '10' and column == '1111'):
            result5 = 14

        if (line == '11' and column == '0000'):
            result5 = 11
        elif (line == '11' and column == '0001'):
            result5 = 8
        elif (line == '11' and column == '0010'):
            result5 = 12
        elif (line == '11' and column == '0011'):
            result5 = 7
        elif (line == '11' and column == '0100'):
            result5 = 1
        elif (line == '11' and column == '0101'):
            result5 = 14
        elif (line == '11' and column == '0110'):
            result5 = 2
        elif (line == '11' and column == '0111'):
            result5 = 13
        elif (line == '11' and column == '1000'):
            result5 = 6
        elif (line == '11' and column == '1001'):
            result5 = 15
        elif (line == '11' and column == '1010'):
            result5 = 0
        elif (line == '11' and column == '1011'):
            result5 = 9
        elif (line == '11' and column == '1100'):
            result5 = 10
        elif (line == '11' and column == '1101'):
            result5 = 4
        elif (line == '11' and column == '1110'):
            result5 = 5
        elif (line == '11' and column == '1111'):
            result5 = 3

        # S6
        test = (result)[30:-12]
        line = test[0] + test[-1]
        column = test[1:-1]

        if (line == '00' and column == '0000'):
            result6 = 12
        elif (line == '00' and column == '0001'):
            result6 = 1
        elif (line == '00' and column == '0010'):
            result6 = 10
        elif (line == '00' and column == '0011'):
            result6 = 15
        elif (line == '00' and column == '0100'):
            result6 = 9
        elif (line == '00' and column == '0101'):
            result6 = 2
        elif (line == '00' and column == '0110'):
            result6 = 6
        elif (line == '00' and column == '0111'):
            result6 = 8
        elif (line == '00' and column == '1000'):
            result6 = 0
        elif (line == '00' and column == '1001'):
            result6 = 13
        elif (line == '00' and column == '1010'):
            result6 = 3
        elif (line == '00' and column == '1011'):
            result6 = 4
        elif (line == '00' and column == '1100'):
            result6 = 14
        elif (line == '00' and column == '1101'):
            result6 = 7
        elif (line == '00' and column == '1110'):
            result6 = 5
        elif (line == '00' and column == '1111'):
            result6 = 11

        if (line == '01' and column == '0000'):
            result6 = 10
        elif (line == '01' and column == '0001'):
            result6 = 15
        elif (line == '01' and column == '0010'):
            result6 = 4
        elif (line == '01' and column == '0011'):
            result6 = 2
        elif (line == '01' and column == '0100'):
            result6 = 7
        elif (line == '01' and column == '0101'):
            result6 = 12
        elif (line == '01' and column == '0110'):
            result6 = 9
        elif (line == '01' and column == '0111'):
            result6 = 5
        elif (line == '01' and column == '1000'):
            result6 = 6
        elif (line == '01' and column == '1001'):
            result6 = 1
        elif (line == '01' and column == '1010'):
            result6 = 13
        elif (line == '01' and column == '1011'):
            result6 = 14
        elif (line == '01' and column == '1100'):
            result6 = 0
        elif (line == '01' and column == '1101'):
            result6 = 11
        elif (line == '01' and column == '1110'):
            result6 = 3
        elif (line == '01' and column == '1111'):
            result6 = 8

        if (line == '10' and column == '0000'):
            result6 = 9
        elif (line == '10' and column == '0001'):
            result6 = 14
        elif (line == '10' and column == '0010'):
            result6 = 15
        elif (line == '10' and column == '0011'):
            result6 = 5
        elif (line == '10' and column == '0100'):
            result6 = 2
        elif (line == '10' and column == '0101'):
            result6 = 8
        elif (line == '10' and column == '0110'):
            result6 = 12
        elif (line == '10' and column == '0111'):
            result6 = 3
        elif (line == '10' and column == '1000'):
            result6 = 7
        elif (line == '10' and column == '1001'):
            result6 = 0
        elif (line == '10' and column == '1010'):
            result6 = 4
        elif (line == '10' and column == '1011'):
            result6 = 10
        elif (line == '10' and column == '1100'):
            result6 = 1
        elif (line == '10' and column == '1101'):
            result6 = 13
        elif (line == '10' and column == '1110'):
            result6 = 11
        elif (line == '10' and column == '1111'):
            result6 = 6

        if (line == '11' and column == '0000'):
            result6 = 4
        elif (line == '11' and column == '0001'):
            result6 = 3
        elif (line == '11' and column == '0010'):
            result6 = 2
        elif (line == '11' and column == '0011'):
            result6 = 12
        elif (line == '11' and column == '0100'):
            result6 = 9
        elif (line == '11' and column == '0101'):
            result6 = 5
        elif (line == '11' and column == '0110'):
            result6 = 15
        elif (line == '11' and column == '0111'):
            result6 = 10
        elif (line == '11' and column == '1000'):
            result6 = 11
        elif (line == '11' and column == '1001'):
            result6 = 14
        elif (line == '11' and column == '1010'):
            result6 = 1
        elif (line == '11' and column == '1011'):
            result6 = 7
        elif (line == '11' and column == '1100'):
            result6 = 6
        elif (line == '11' and column == '1101'):
            result6 = 0
        elif (line == '11' and column == '1110'):
            result6 = 8
        elif (line == '11' and column == '1111'):
            result6 = 13

        # S7
        test = (result)[36:-6]
        line = test[0] + test[-1]
        column = test[1:-1]

        if (line == '00' and column == '0000'):
            result7 = 4
        elif (line == '00' and column == '0001'):
            result7 = 11
        elif (line == '00' and column == '0010'):
            result7 = 2
        elif (line == '00' and column == '0011'):
            result7 = 14
        elif (line == '00' and column == '0100'):
            result7 = 15
        elif (line == '00' and column == '0101'):
            result7 = 0
        elif (line == '00' and column == '0110'):
            result7 = 8
        elif (line == '00' and column == '0111'):
            result7 = 13
        elif (line == '00' and column == '1000'):
            result7 = 3
        elif (line == '00' and column == '1001'):
            result7 = 12
        elif (line == '00' and column == '1010'):
            result7 = 9
        elif (line == '00' and column == '1011'):
            result7 = 7
        elif (line == '00' and column == '1100'):
            result7 = 5
        elif (line == '00' and column == '1101'):
            result7 = 10
        elif (line == '00' and column == '1110'):
            result7 = 6
        elif (line == '00' and column == '1111'):
            result7 = 1

        if (line == '01' and column == '0000'):
            result7 = 13
        elif (line == '01' and column == '0001'):
            result7 = 0
        elif (line == '01' and column == '0010'):
            result7 = 11
        elif (line == '01' and column == '0011'):
            result7 = 7
        elif (line == '01' and column == '0100'):
            result7 = 4
        elif (line == '01' and column == '0101'):
            result7 = 9
        elif (line == '01' and column == '0110'):
            result7 = 1
        elif (line == '01' and column == '0111'):
            result7 = 10
        elif (line == '01' and column == '1000'):
            result7 = 14
        elif (line == '01' and column == '1001'):
            result7 = 3
        elif (line == '01' and column == '1010'):
            result7 = 5
        elif (line == '01' and column == '1011'):
            result7 = 12
        elif (line == '01' and column == '1100'):
            result7 = 2
        elif (line == '01' and column == '1101'):
            result7 = 15
        elif (line == '01' and column == '1110'):
            result7 = 8
        elif (line == '01' and column == '1111'):
            result7 = 6

        if (line == '10' and column == '0000'):
            result7 = 1
        elif (line == '10' and column == '0001'):
            result7 = 4
        elif (line == '10' and column == '0010'):
            result7 = 11
        elif (line == '10' and column == '0011'):
            result7 = 13
        elif (line == '10' and column == '0100'):
            result7 = 12
        elif (line == '10' and column == '0101'):
            result7 = 3
        elif (line == '10' and column == '0110'):
            result7 = 7
        elif (line == '10' and column == '0111'):
            result7 = 14
        elif (line == '10' and column == '1000'):
            result7 = 10
        elif (line == '10' and column == '1001'):
            result7 = 15
        elif (line == '10' and column == '1010'):
            result7 = 6
        elif (line == '10' and column == '1011'):
            result7 = 8
        elif (line == '10' and column == '1100'):
            result7 = 0
        elif (line == '10' and column == '1101'):
            result7 = 5
        elif (line == '10' and column == '1110'):
            result7 = 9
        elif (line == '10' and column == '1111'):
            result7 = 2

        if (line == '11' and column == '0000'):
            result7 = 6
        elif (line == '11' and column == '0001'):
            result7 = 11
        elif (line == '11' and column == '0010'):
            result7 = 13
        elif (line == '11' and column == '0011'):
            result7 = 8
        elif (line == '11' and column == '0100'):
            result7 = 1
        elif (line == '11' and column == '0101'):
            result7 = 4
        elif (line == '11' and column == '0110'):
            result7 = 10
        elif (line == '11' and column == '0111'):
            result7 = 7
        elif (line == '11' and column == '1000'):
            result7 = 9
        elif (line == '11' and column == '1001'):
            result7 = 5
        elif (line == '11' and column == '1010'):
            result7 = 0
        elif (line == '11' and column == '1011'):
            result7 = 15
        elif (line == '11' and column == '1100'):
            result7 = 14
        elif (line == '11' and column == '1101'):
            result7 = 2
        elif (line == '11' and column == '1110'):
            result7 = 3
        elif (line == '11' and column == '1111'):
            result7 = 12

        # S8
        test = (result)[42:]
        line = test[0] + test[-1]
        column = test[1:-1]

        if (line == '01' and column == '0000'):
            result8 = 13
        elif (line == '01' and column == '0001'):
            result8 = 2
        elif (line == '01' and column == '0010'):
            result8 = 8
        elif (line == '01' and column == '0011'):
            result8 = 4
        elif (line == '01' and column == '0100'):
            result8 = 6
        elif (line == '01' and column == '0101'):
            result8 = 15
        elif (line == '01' and column == '0110'):
            result8 = 11
        elif (line == '01' and column == '0111'):
            result8 = 1
        elif (line == '01' and column == '1000'):
            result8 = 10
        elif (line == '01' and column == '1001'):
            result8 = 9
        elif (line == '01' and column == '1010'):
            result8 = 3
        elif (line == '01' and column == '1011'):
            result8 = 14
        elif (line == '01' and column == '1100'):
            result8 = 5
        elif (line == '01' and column == '1101'):
            result8 = 0
        elif (line == '01' and column == '1110'):
            result8 = 12
        elif (line == '01' and column == '1111'):
            result8 = 7

        if (line == '10' and column == '0000'):
            result8 = 1
        elif (line == '10' and column == '0001'):
            result8 = 15
        elif (line == '10' and column == '0010'):
            result8 = 13
        elif (line == '10' and column == '0011'):
            result8 = 8
        elif (line == '10' and column == '0100'):
            result8 = 10
        elif (line == '10' and column == '0101'):
            result8 = 3
        elif (line == '10' and column == '0110'):
            result8 = 7
        elif (line == '10' and column == '0111'):
            result8 = 4
        elif (line == '10' and column == '1000'):
            result8 = 12
        elif (line == '10' and column == '1001'):
            result8 = 5
        elif (line == '10' and column == '1010'):
            result8 = 6
        elif (line == '10' and column == '1011'):
            result8 = 11
        elif (line == '10' and column == '1100'):
            result8 = 0
        elif (line == '10' and column == '1101'):
            result8 = 14
        elif (line == '10' and column == '1110'):
            result8 = 9
        elif (line == '10' and column == '1111'):
            result8 = 2

        if (line == '00' and column == '0000'):
            result8 = 7
        elif (line == '00' and column == '0001'):
            result8 = 11
        elif (line == '00' and column == '0010'):
            result8 = 4
        elif (line == '00' and column == '0011'):
            result8 = 1
        elif (line == '00' and column == '0100'):
            result8 = 9
        elif (line == '00' and column == '0101'):
            result8 = 12
        elif (line == '00' and column == '0110'):
            result8 = 14
        elif (line == '00' and column == '0111'):
            result8 = 2
        elif (line == '00' and column == '1000'):
            result8 = 0
        elif (line == '00' and column == '1001'):
            result8 = 6
        elif (line == '00' and column == '1010'):
            result8 = 10
        elif (line == '00' and column == '1011'):
            result8 = 13
        elif (line == '00' and column == '1100'):
            result8 = 15
        elif (line == '00' and column == '1101'):
            result8 = 3
        elif (line == '00' and column == '1110'):
            result8 = 5
        elif (line == '00' and column == '1111'):
            result8 = 8

        if (line == '11' and column == '0000'):
            result8 = 2
        elif (line == '11' and column == '0001'):
            result8 = 1
        elif (line == '11' and column == '0010'):
            result8 = 14
        elif (line == '11' and column == '0011'):
            result8 = 7
        elif (line == '11' and column == '0100'):
            result8 = 4
        elif (line == '11' and column == '0101'):
            result8 = 10
        elif (line == '11' and column == '0110'):
            result8 = 8
        elif (line == '11' and column == '0111'):
            result8 = 13
        elif (line == '11' and column == '1000'):
            result8 = 15
        elif (line == '11' and column == '1001'):
            result8 = 12
        elif (line == '11' and column == '1010'):
            result8 = 9
        elif (line == '11' and column == '1011'):
            result8 = 0
        elif (line == '11' and column == '1100'):
            result8 = 3
        elif (line == '11' and column == '1101'):
            result8 = 5
        elif (line == '11' and column == '1110'):
            result8 = 6
        elif (line == '11' and column == '1111'):
            result8 = 11

        if (len(bin(result1)[2:]) < 4):
            a = len(bin(result1)[2:])
            u = 4 - a
            result1 = (u * '0') + bin(result1)[2:]
        else:
            result1 = bin(result1)[2:]

        if (len(bin(result2)[2:]) < 4):
            a = len(bin(result2)[2:])
            u = 4 - a
            result2 = (u * '0') + bin(result2)[2:]
        else:
            result2 = bin(result2)[2:]

        if (len(bin(result3)[2:]) < 4):
            a = len(bin(result3)[2:])
            u = 4 - a
            result3 = (u * '0') + bin(result3)[2:]
        else:
            result3 = bin(result3)[2:]

        if (len(bin(result4)[2:]) < 4):
            a = len(bin(result4)[2:])
            u = 4 - a
            result4 = (u * '0') + bin(result4)[2:]
        else:
            result4 = bin(result4)[2:]

        if (len(bin(result5)[2:]) < 4):
            a = len(bin(result5)[2:])
            u = 4 - a
            result5 = (u * '0') + bin(result5)[2:]
        else:
            result5 = bin(result5)[2:]

        if (len(bin(result6)[2:]) < 4):
            a = len(bin(result6)[2:])
            u = 4 - a
            result6 = (u * '0') + bin(result6)[2:]
        else:
            result6 = bin(result6)[2:]

        if (len(bin(result7)[2:]) < 4):
            a = len(bin(result7)[2:])
            u = 4 - a
            result7 = (u * '0') + bin(result7)[2:]
        else:
            result7 = bin(result7)[2:]

        if (len(bin(result8)[2:]) < 4):
            a = len(bin(result8)[2:])
            u = 4 - a
            result8 = (u * '0') + bin(result8)[2:]
        else:
            result8 = bin(result8)[2:]

        result = result1 + result2 + result3 + result4 + result5 + result6 + result7 + result8

        result = int(result, 2)

        # P-box
        result = ((result & 0b00000000000000010000000000000000) << 15) | \
                 ((result & 0b00000010000000000000000000000000) << 5) | \
                 ((result & 0b00000000000000000001000000000000) << 17) | \
                 ((result & 0b00000000000000000000100000000000) << 17) | \
                 ((result & 0b00000000000000000000000000001000) << 24) | \
                 ((result & 0b00000000000100000000000000000000) << 6) | \
                 ((result & 0b00000000000000000000000000010000) << 21) | \
                 ((result & 0b00000000000000001000000000000000) << 9) | \
                 ((result & 0b10000000000000000000000000000000) >> 8) | \
                 ((result & 0b00000000000000100000000000000000) << 5) | \
                 ((result & 0b00000000000000000000001000000000) << 12) | \
                 ((result & 0b00000000000000000000000001000000) << 14) | \
                 ((result & 0b00001000000000000000000000000000) >> 8) | \
                 ((result & 0b00000000000000000100000000000000) << 4) | \
                 ((result & 0b00000000000000000000000000000010) << 16) | \
                 ((result & 0b00000000010000000000000000000000) >> 6) | \
                 ((result & 0b01000000000000000000000000000000) >> 15) | \
                 ((result & 0b00000001000000000000000000000000) >> 10) | \
                 ((result & 0b00000000000000000000000100000000) << 5) | \
                 ((result & 0b00000000000001000000000000000000) >> 6) | \
                 ((result & 0b00000000000000000000000000000001) << 11) | \
                 ((result & 0b00000000000000000000000000100000) << 5) | \
                 ((result & 0b00100000000000000000000000000000) >> 20) | \
                 ((result & 0b00000000100000000000000000000000) >> 15) | \
                 ((result & 0b00000000000000000010000000000000) >> 6) | \
                 ((result & 0b00000000000010000000000000000000) >> 13) | \
                 ((result & 0b00000000000000000000000000000100) << 3) | \
                 ((result & 0b00000100000000000000000000000000) >> 22) | \
                 ((result & 0b00000000000000000000010000000000) >> 7) | \
                 ((result & 0b00000000001000000000000000000000) >> 19) | \
                 ((result & 0b00010000000000000000000000000000) >> 27) | \
                 ((result & 0b00000000000000000000000010000000) >> 7)

        return result

    def ChangeLeftRight(self):
        self.temp = ((self.temp & 0b1111111111111111111111111111111100000000000000000000000000000000) >> 32) | \
                    ((self.temp & 0b0000000000000000000000000000000011111111111111111111111111111111) << 32)

    def key_gen(self):
        key_temp = self.key
        key_list = []
        key = key_temp
        i = 0
        while i < self.round_amount:
            if (len(bin(key)[2:]) < 64):
                a = 64 - len(bin(key)[2:])
                key = (a * '0') + bin(key)[2:]
            else:
                key = bin(key)[2:]

                # Deleting 8, 16, 24, 32, 40, 48, 56, 64 elements
            key = list(key)
            del key[7], key[14], key[21], key[28], key[35], key[42], key[49], key[56]
            key = ''.join(key)

            key = int(key, 2)

            # 10       #20       #30       #40       #50
            # 12345678901234567890123456789012345678901234567890123456
            key = ((key & 0b00000000000000000000000000000000000000000000000001000000) << 49) | \
                  ((key & 0b00000000000000000000000000000000000000000010000000000000) << 41) | \
                  ((key & 0b00000000000000000000000000000000000100000000000000000000) << 33) | \
                  ((key & 0b00000000000000000000000000001000000000000000000000000000) << 25) | \
                  ((key & 0b00000000000000000000010000000000000000000000000000000000) << 17) | \
                  ((key & 0b00000000000000100000000000000000000000000000000000000000) << 9) | \
                  ((key & 0b00000000000000000100000000000000000000000000000000000000) << 1) | \
                  ((key & 0b10000000000000000000000000000000000000000000000000000000) << 0) | \
                  ((key & 0b00000000000000000000000000000000000000000000000000100000) << 42) | \
                  ((key & 0b00000000000000000000000000000000000000000001000000000000) << 34) | \
                  ((key & 0b00000000000000000000000000000000000010000000000000000000) << 26) | \
                  ((key & 0b00000000000000000000000000000100000000000000000000000000) << 18) | \
                  ((key & 0b00000000000000000000001000000000000000000000000000000000) << 10) | \
                  ((key & 0b00000000000000010000000000000000000000000000000000000000) << 2) | \
                  ((key & 0b00000000100000000000000000000000000000000000000000000000) >> 6) | \
                  ((key & 0b01000000000000000000000000000000000000000000000000000000) >> 14) | \
                  ((key & 0b00000000000000000000000000000000000000000000000000010000) << 35) | \
                  ((key & 0b00000000000000000000000000000000000000000000100000000000) << 27) | \
                  ((key & 0b00000000000000000000000000000000000001000000000000000000) << 19) | \
                  ((key & 0b00000000000000000000000000000010000000000000000000000000) << 11) | \
                  ((key & 0b00000000000000000000000100000000000000000000000000000000) << 3) | \
                  ((key & 0b00000000000000001000000000000000000000000000000000000000) >> 5) | \
                  ((key & 0b00000000010000000000000000000000000000000000000000000000) >> 13) | \
                  ((key & 0b00100000000000000000000000000000000000000000000000000000) >> 21) | \
                  ((key & 0b00000000000000000000000000000000000000000000000000001000) << 28) | \
                  ((key & 0b00000000000000000000000000000000000000000000010000000000) << 20) | \
                  ((key & 0b00000000000000000000000000000000000000100000000000000000) << 12) | \
                  ((key & 0b00000000000000000000000000000000000100000000000000000000) << 4) | \
                  ((key & 0b00000000000000000000000000000000000000000000000000000001) << 27) | \
                  ((key & 0b00000000000000000000000000000000000000000000000010000000) << 19) | \
                  ((key & 0b00000000000000000000000000000000000000000100000000000000) << 11) | \
                  ((key & 0b00000000000000000000000000000000001000000000000000000000) << 3) | \
                  ((key & 0b00000000000000000000000000010000000000000000000000000000) >> 5) | \
                  ((key & 0b00000000000000000000100000000000000000000000000000000000) >> 13) | \
                  ((key & 0b00000000000001000000000000000000000000000000000000000000) >> 21) | \
                  ((key & 0b00000010000000000000000000000000000000000000000000000000) >> 29) | \
                  ((key & 0b00000000000000000000000000000000000000000000000000000010) << 18) | \
                  ((key & 0b00000000000000000000000000000000000000000000000100000000) << 10) | \
                  ((key & 0b00000000000000000000000000000000000000001000000000000000) << 2) | \
                  ((key & 0b00000000000000000000000000000000010000000000000000000000) >> 6) | \
                  ((key & 0b00000000000000000000000000100000000000000000000000000000) >> 14) | \
                  ((key & 0b00000000000000000001000000000000000000000000000000000000) >> 22) | \
                  ((key & 0b00000000000010000000000000000000000000000000000000000000) << 30) | \
                  ((key & 0b00000100000000000000000000000000000000000000000000000000) >> 38) | \
                  ((key & 0b00000000000000000000000000000000000000000000000000000100) >> 9) | \
                  ((key & 0b00000000000000000000000000000000000000000000001000000000) << 1) | \
                  ((key & 0b00000000000000000000000000000000000000010000000000000000) >> 7) | \
                  ((key & 0b00000000000000000000000000000000100000000000000000000000) >> 15) | \
                  ((key & 0b00000000000000000000000001000000000000000000000000000000) >> 23) | \
                  ((key & 0b00000000000000000010000000000000000000000000000000000000) >> 31) | \
                  ((key & 0b00000000000100000000000000000000000000000000000000000000) >> 39) | \
                  ((key & 0b00001000000000000000000000000000000000000000000000000000) >> 47) | \
                  ((key & 0b00000000000000000000000010000000000000000000000000000000) >> 28) | \
                  ((key & 0b00000000000000000100000000000000000000000000000000000000) >> 36) | \
                  ((key & 0b00000000001000000000000000000000000000000000000000000000) >> 44) | \
                  ((key & 0b00010000000000000000000000000000000000000000000000000000) >> 52)

            C0 = ((key & 0b11111111111111111111111111110000000000000000000000000000) << 0)
            D0 = ((key & 0b00000000000000000000000000001111111111111111111111111111) << 0)

            if i == 1 or i == 2 or i == 9 or i == 16:
                C0 = C0 << 1
                D0 = D0 << 1
            else:
                C0 = C0 << 2
                D0 = D0 << 2

            round_key = C0 + D0

                                                 #10       #20       #30       #40       #50
                                      # 12345678901234567890123456789012345678901234567890123456
            round_key = ((round_key & 0b00000000000001000000000000000000000000000000000000000000) << 13) | \
                        ((round_key & 0b00000000000000001000000000000000000000000000000000000000) << 15) | \
                        ((round_key & 0b00000000001000000000000000000000000000000000000000000000) << 8) | \
                        ((round_key & 0b00000000000000000000000100000000000000000000000000000000) << 20) | \
                        ((round_key & 0b10000000000000000000000000000000000000000000000000000000) >> 4) | \
                        ((round_key & 0b00001000000000000000000000000000000000000000000000000000) >> 1) | \
                        ((round_key & 0b00100000000000000000000000000000000000000000000000000000) >> 4) | \
                        ((round_key & 0b00000000000000000000000000010000000000000000000000000000) << 20) | \
                        ((round_key & 0b00000000000000100000000000000000000000000000000000000000) << 6) | \
                        ((round_key & 0b00000100000000000000000000000000000000000000000000000000) >> 4) | \
                        ((round_key & 0b00000000000000000000100000000000000000000000000000000000) << 10) | \
                        ((round_key & 0b00000000010000000000000000000000000000000000000000000000) >> 2) | \
                        ((round_key & 0b00000000000000000000001000000000000000000000000000000000) << 10) | \
                        ((round_key & 0b00000000000000000010000000000000000000000000000000000000) << 5) | \
                        ((round_key & 0b00000000000100000000000000000000000000000000000000000000) >> 3) | \
                        ((round_key & 0b00010000000000000000000000000000000000000000000000000000) >> 12) | \
                        ((round_key & 0b00000000000000000000000001000000000000000000000000000000) << 9) | \
                        ((round_key & 0b00000001000000000000000000000000000000000000000000000000) >> 10) | \
                        ((round_key & 0b00000000000000010000000000000000000000000000000000000000) >> 3) | \
                        ((round_key & 0b00000010000000000000000000000000000000000000000000000000) >> 13) | \
                        ((round_key & 0b00000000000000000000000000100000000000000000000000000000) << 6) | \
                        ((round_key & 0b00000000000000000001000000000000000000000000000000000000) >> 2) | \
                        ((round_key & 0b00000000000010000000000000000000000000000000000000000000) >> 10) | \
                        ((round_key & 0b01000000000000000000000000000000000000000000000000000000) >> 22) | \
                        ((round_key & 0b00000000000000000000000000000000000000001000000000000000) << 16) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000000000010000) << 26) | \
                        ((round_key & 0b00000000000000000000000000000010000000000000000000000000) << 4) | \
                        ((round_key & 0b00000000000000000000000000000000000010000000000000000000) << 9) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000001000000000) << 8) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000000000000010) << 25) | \
                        ((round_key & 0b00000000000000000000000000000100000000000000000000000000) >> 1) | \
                        ((round_key & 0b00000000000000000000000000000000000000010000000000000000) << 8) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000000000100000) >> 18) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000100000000000) << 11) | \
                        ((round_key & 0b00000000000000000000000000000000100000000000000000000000) >> 2) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000000100000000) << 12) | \
                        ((round_key & 0b00000000000000000000000000000000000000000001000000000000) << 7) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000000010000000) << 11) | \
                        ((round_key & 0b00000000000000000000000000000000000000100000000000000000) << 0) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000000000000001) << 16) | \
                        ((round_key & 0b00000000000000000000000000000000010000000000000000000000) >> 7) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000000000001000) << 11) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000010000000000) << 3) | \
                        ((round_key & 0b00000000000000000000000000000000000000000100000000000000) >> 2) | \
                        ((round_key & 0b00000000000000000000000000000000000000000000000001000000) << 5) | \
                        ((round_key & 0b00000000000000000000000000000000000100000000000000000000) >> 10) | \
                        ((round_key & 0b00000000000000000000000000001000000000000000000000000000) >> 18) | \
                        ((round_key & 0b00000000000000000000000000000001000000000000000000000000) >> 16)

            if(len(bin(round_key)[2:]) < 56):
                t = 56 - len(bin(round_key)[2:])
                round_key =  (t * '0') +  bin(round_key)[2:]
            else:
                round_key = bin(round_key)

            round_key = (round_key)[:-8]


            round_key = int(round_key, 2)

            key_list.append(round_key)


            i = i + 1


        return key_list



'''
    def key_gen(self):
        key_temp = self.key
        key_list = []
        i = 0
        while i < self.round_amount:
            key_temp = ((key_temp & 0b11111111111111111111111111111111111111111111111111111110) >> 1) | \
                       ((key_temp & 0b00000000000000000000000000000000000000000000000000000001) << 55)
            round_key = key_temp & 0b111111111111111111111111111111111111111111111111
            key_list.append(round_key)
            i = i + 1
        #print(key_list)
        return key_list
'''


a = 11125411106087900573
print(f'a = {a}')
key = 324234234
round_amount = 16
DES = small_des(key_=key, round_amount_=round_amount)
b = DES.Enc(a)
print(f'b = {b}')
c = DES.Dec(b)
print(f'c = {c}')