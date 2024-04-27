class RoundKeyGeneration:
    def __init__(self, key, round: int):
        self.key = key
        self.round = int(bin(round), 2)
        self.key_holder = []
        self.round_key = ""

    def key_split(self):
        temp = self.key
        k0 = int(temp[0:6], 2)
        k1 = int(('0b' + temp[6:10]), 2)
        k2 = int(('0b' + temp[10:14]), 2)
        k3 = int(('0b' + temp[14:18]), 2)
        self.key_holder = [k0, k1, k2, k3]

    def nibble_Sub(self, nibble):
        sBox = {
            0b0000: 0b1110,
            0b0001: 0b0100,
            0b0010: 0b1101,
            0b0011: 0b0001,
            0b0100: 0b0010,
            0b0101: 0b1111,
            0b0110: 0b1011,
            0b0111: 0b1000,
            0b1000: 0b0011,
            0b1001: 0b1010,
            0b1010: 0b0110,
            0b1011: 0b1100,
            0b1100: 0b0101,
            0b1101: 0b1001,
            0b1110: 0b0000,
            0b1111: 0b0111,
        }

        return sBox[nibble]

    def round_key_gen(self):
        w0 = self.key_holder[0] ^ self.round ^ self.nibble_Sub(nibble=self.key_holder[3])
        w1 = self.key_holder[1] ^ w0
        w2 = self.key_holder[2] ^ w1
        w3 = self.key_holder[3] ^ w2
        self.key_holder = [w0, w1, w2, w3]

    def key_format(self):
        self.key_split()
        self.round_key_gen()
        w0 = format(self.key_holder[0], '#06b').replace("0b", "")
        w1 = format(self.key_holder[1], '#06b').replace("0b", "")
        w2 = format(self.key_holder[2], '#06b').replace("0b", "")
        w3 = format(self.key_holder[3], '#06b').replace("0b", "")
        self.round_key = format((int(("0b" + w0 + w1 + w2 + w3), 2)), '#018b')
        return self.round_key
