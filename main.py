from round_key_generation import RoundKeyGeneration


def binary_Converter(text_input):
    plaintext = text_input.strip()
    w0 = format(int(bin(ord(plaintext[0])), 2), '#010b')
    w1 = format(int(bin(ord(plaintext[1])), 2), '#010b')
    w2 = format(int(bin(ord(plaintext[2])), 2), '#010b')
    w3 = format(int(bin(ord(plaintext[3])), 2), '#010b')

    block_cipher_1 = w0 + w1.replace("0b", "")
    block_cipher_2 = w2 + w3.replace("0b", "")

    return [block_cipher_1, block_cipher_2]


def nibble_Sub(instance: list):
    output = []
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

    for block in range(0, 2, 1):
        result = [format(sBox[int(nibble, 2)], '#06b') for nibble in instance[block]]
        output.append(result)
    return output


def shift_Rows(instance: list):
    output = []
    results = [[blocks[0], blocks[3], blocks[2], blocks[1]] for blocks in instance]

    for result in results:
        s0 = result[0].replace("0b", "")
        s1 = result[1].replace("0b", "")
        s2 = result[2].replace("0b", "")
        s3 = result[3].replace("0b", "")
        shift_result = format(int(('0b' + s0 + s1 + s2 + s3), 2), '#018b')
        output.append(shift_result)
    return output


def split_instance_4bits(instances: list):
    nibbles = []
    for instance in instances:
        d0 = int(instance[0:6], 2)
        d1 = int(('0b' + instance[6:10]), 2)
        d2 = int(('0b' + instance[10:14]), 2)
        d3 = int(('0b' + instance[14:18]), 2)
        nibbles.append([d0, d1, d2, d3])
    return nibbles


def MixColumn(instances: list):
    output = []
    nibbles_blocks = split_instance_4bits(instances)
    for nibbles_block in nibbles_blocks:
        d0 = nibbles_block[0]
        d1 = nibbles_block[1]
        d2 = nibbles_block[2]
        d3 = nibbles_block[3]
        # -------------------------------------- MixColumn in Mini-AES -------------------------------------------------#
        # m0 = 3d0 XOR 2 d1
        # m1 = 2d0 XOR 3 d1
        # m2 = 3d2 XOR 2 d3
        # m3 = 2d2 XOR 3 d3
        # Modulo reduction polynomial = X^4 + x + 1 = 0b0000000000010011 ....

        d0_mul2 = (d0 << 1) ^ 0b10011 if ((d0 << 1) & 0b10000) else d0 << 1
        d1_mul2 = (d1 << 1) ^ 0b10011 if ((d1 << 1) & 0b10000) else d1 << 1
        d2_mul2 = (d2 << 1) ^ 0b10011 if ((d2 << 1) & 0b10000) else d2 << 1
        d3_mul2 = (d3 << 1) ^ 0b10011 if ((d3 << 1) & 0b10000) else d3 << 1

        m0 = format(((d0_mul2 ^ d0) ^ d1_mul2), '#06b').replace("0b", "")
        m1 = format((d0_mul2 ^ (d1_mul2 ^ d1)), '#06b').replace("0b", "")
        m2 = format(((d2_mul2 ^ d2) ^ d3_mul2), '#06b').replace("0b", "")
        m3 = format((d2_mul2 ^ (d3_mul2 ^ d3)), '#06b').replace("0b", "")

        result = "0b" + m0 + m1 + m2 + m3
        output.append(result)
    return output


def add_round_key(instances: list[str], roundkey: str):
    output = []
    first_block_cipher = int(instances[0], 2)
    second_block_cipher = int(instances[1], 2)
    round_key = int(roundkey, 2)
    result_1 = format((first_block_cipher ^ round_key), '#018b')
    result_2 = format(second_block_cipher ^ round_key, '#018b')

    results = [result_1, result_2]
    for result in results:
        d0 = result[0:6]
        d1 = f"0b{result[6:10]}"
        d2 = f"0b{result[10:14]}"
        d3 = f"0b{result[14:18]}"

        output.append([d0, d1, d2, d3])
    return output


text = input("Please input your 4 letter word: ")
key_0 = '0b1001011110100011'
key_0 = format(int(key_0, 2), '#018b')

rnd_key_01 = RoundKeyGeneration(key_0, 1)
key_1 = rnd_key_01.key_format()

rnd_key_02 = RoundKeyGeneration(key_1, 2)
key_2 = rnd_key_02.key_format()

print(key_1)
print(key_2)

text_Bin = binary_Converter(text)
text_initial = add_round_key(text_Bin, key_0)
text_Sub = nibble_Sub(text_initial)
text_Shift = shift_Rows(text_Sub)
text_mixColumn = MixColumn(text_Shift)

ls_initial = add_round_key(text_mixColumn, key_1)
ls_sub = nibble_Sub(ls_initial)
ls_shift = shift_Rows(ls_sub)
ls_addkey = add_round_key(ls_shift, key_2)

print(f"The binary form of your plaintext is = {text_Bin}")
print(f"result after Add round key of the plaintext is = {text_initial}")
print(f"result after Nibble sub of the Instance is = {text_Sub}")
print(f"result after shiftRows is: {text_Shift}")
print(f"result after MixColumn is: {text_mixColumn}")
print(f"result after Add round key of the Instance is: {ls_initial}")

print("\nNow proceed last round....\n")
print(f"result after nibble sub of the Instance 1 is: {ls_sub}")
print(f"result after shift row of the Instance 1 is: {ls_shift}")
print(f"Ciphertext is: {ls_addkey}")
