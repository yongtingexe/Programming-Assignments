# author = Lee Yong Ting 0132307
# Everything is written as functions so feel free to import

def interface():
    # Boolean variable to determine when to terminate
    QUIT = False

    # User interface implemented using a while loop
    # Continuosly take in command and execute until
    # user chooses to exit
    while not QUIT:
        # Menu
        print("\nMenu" +
              "\n1. Number Conversion" +
              "\n2. Floating Point Representation" +
              "\n3. Exit")
        opt = input("Command: ")
        
        # Number Conversion
        if int(opt) == 1:
            # Bases to select from and print as message
            bases = ["Decimal", "Binary", "Hexadecimal"]
            msg = ""
            print("\nDecimal = D, Binary = B, Hexadecimal = H")
            inp_base = input("Input Base: ")
            out_base = input("Output Base: ")
            
            # Get input base name first then output base
            # Match the first character for result
            for base in bases:
                if inp_base == base[0]:
                    msg = base + " to "
            for base in bases:
                if out_base == base[0]:
                    msg += base
            print("\n" + msg)    
            num = input("Number to convert: ")
            # Pass to switch to determine which operation to run
            switch(num, inp_base, out_base)

        # Floating point representation
        elif int(opt) == 2:
            inp_num = input("\nDecimal in Real Number: ")
            print(float_pt_rep(inp_num))
        
        else:
            print("\n")
            QUIT = True


# Determine operation based on input and
# output bases selected by user
def switch(num, inp_base, out_base):
    if inp_base == 'D':
        if out_base == 'B':
            print(dec_to_bin(num))
        elif out_base == 'H':
            print(dec_to_hex(num))
    elif inp_base == 'B':
        if out_base == 'D':
            print(bin_to_dec(num))
        elif out_base == 'H':
            print(bin_to_hex(num))
    elif inp_base == 'H':
        if out_base == 'D':
            print(hex_to_dec(num))
        elif out_base == 'B':
            print(hex_to_bin(num))


# Decimal to Binary
def dec_to_bin(num: str) -> str:
    num = int(num)
    res = ""
    # Divide by 2 repeatedly until reaches 0
    # Remainder found each loop is added to the front
    # of the string, similar to reading bottom up in
    # long division
    # Final string after loop is the result
    while num > 0:                
        res = str(num % 2) + res     
        num = num // 2               
    return res


# Decimal to Hexadecimal
def dec_to_hex(num: str) -> str:
    alphabet = ["A", "B", "C", "D", "E", "F"]
    res = ""
    num = int(num)
    # Divide by 16 repeatedly until reaches 0
    # Remainder found each loop is added to the front
    # of the string, similar to reading bottom up in
    # long division
    # Final string after loop is the result
    while num > 0:
        remainder = num % 16
        if remainder < 10:
            res = str(remainder) + res
        # Convert remainder >= 10 to alphabets
        # Remainder minus 10 is same as the
        # index of its alphabet in the list
        else:
            res = alphabet[remainder - 10] + res 
        num = num // 16
    return res


# Binary to Decimal
def bin_to_dec(num: str) -> int:
    # Reverse the binary string
    num = num[::-1]
    res = 0
    # Read by bit from left to right(smallest to biggest place)
    # Multiplies each bit with 2 to the power of its place value
    # Multiplication result is added to the sum each loop
    # Result decimal is the sum
    for i in range(len(num)):
        res += (int(num[i]) * (2 ** i))
    return res


# Binary to Hexadecimal
def bin_to_hex(num: str) -> str:
    hex_table = [("0000", "0"), ("0001", "1"), ("0010", "2"), ("0011", "3"),
                 ("0100", "4"), ("0101", "5"), ("0110", "6"), ("0111", "7"),
                 ("1000", "8"), ("1001", "9"), ("1010", "A"), ("1011", "B"),
                 ["1100", "C"], ("1101", "D"), ("1110", "E"), ("1111", "F")]
    quads, res = [], ""
    # Group every 4 bits of the string together starting from the back
    # and store them in a list
    # Keep at most 4 bits without grouping
    while len(num) > 4:
        quads.append(num[-4:])
        num = num[:-4]
    # Pad last group of bits with 0s if shorter than 4 bits
    quads.append(("0" * (4 - len(num))) + num)
    # Iterate through each group
    # Search through the hex table and find its corresponding hex value
    # Each hex value found is added to the back of the result string
    for quad in quads:
        for pair in hex_table:
            if quad == pair[0]:
                res += pair[1]
    # Reverse the result to get back the correct order since
    # the input string is read from the back
    return res[::-1]


# Hexadecimal to Decimal
def hex_to_dec(num: str) -> int:
    res = 0
    # Initialise two lists which function as rows to form a table
    alphabet = ["A", "B", "C", "D", "E", "F"]
    val = [10, 11, 12, 13, 14, 15]
    # Reverse the string
    num = num[::-1]
    # Read by digit from left to right(smallest to biggest place)
    # Multiplies each digit with 16 to the power of its place value
    # Multiplication result is added to the sum each loop
    # Result decimal is the sum
    for i in range(len(num)):
        # Convert alphabet back to number by referring to the table
        if num[i] in alphabet:
            res += val[alphabet.index(num[i])] * (16 ** i)
        else:
            res += int(num[i]) * (16 ** i)
    return res


# Hexadecimal to Binary
def hex_to_bin(num: str) -> str:
    hex_table = [("0000", "0"), ("0001", "1"), ("0010", "2"), ("0011", "3"),
                 ("0100", "4"), ("0101", "5"), ("0110", "6"), ("0111", "7"),
                 ("1000", "8"), ("1001", "9"), ("1010", "A"), ("1011", "B"),
                 ["1100", "C"], ("1101", "D"), ("1110", "E"), ("1111", "F")]
    res = ""
    # Read by digit from left to right
    # Search through the table to find its corresponding decimal value
    # Each value found is added to the back of the string
    for digit in num:
        for pair in hex_table:
            if digit == pair[1]:
                res += pair[0]
    # Remove the extra 0s at the front by slicing them away
    # and return the final string
    return res[res.index("1"):]


# Convert real number to binary floating point
def float_pt_rep(num: str) -> str:
    sign_bit = "0"
    exp_bit = integral_mantissa = fractional_mantissa = res_mantissa = res = ""
    num = float(num)
    
    # Determine the sign bit and modulus the value
    if num < 0:
        sign_bit = "1"
        num = abs(num)
    
    # Convert the value to binary form
    # Integral part and fractional part computed separately
    # Compute only the integral part if value given is a whole number
    if not "." in str(num):
        # Reuse the previous function to convert decimal to binary
        integral_mantissa = dec_to_bin(num)
    else:
        integral, fractional = int(num), num - int(num)
        # Values < 1 do not need to compute the integral part
        # eg: 0.3
        if integral != 0:
            integral_mantissa = dec_to_bin(integral)
        # For fractional, multiply by 2 repeatedly
        # Integer found for each multiplication result is added
        # to the back of the string
        # Keep fractional in the form of fraction
        # by subtracting 1 from it when it goes above 1
        # Final string after loop is the fractional in binary
        while fractional != 0 or len(fractional_mantissa) < 16:
            fractional *= 2
            if fractional >= 1:
                fractional_mantissa += "1"
                fractional -= 1
            else:
                fractional_mantissa += "0"

    # Compute the exponent and adjust the binary value to form the mantissa
    # Starting from left, locate the first high bit in the binary value
    # Shift the value to the place before the first high bit
    if integral_mantissa != "":
        # Binary value > 1 has integral part
        # thus shift value to the left by slicing
        # Exponent equals to the number of places shifted
        exp = len(integral_mantissa) - (integral_mantissa.index("1") + 1)
        res_mantissa = integral_mantissa[integral_mantissa.index("1") + 1:] + fractional_mantissa
    else:
        # Binary value < 1 has no integral part
        # thus shift value to the right by slicing
        # Exponent equals to the number of places shifted
        exp = -(fractional_mantissa.index("1") + 1)
        res_mantissa = integral_mantissa + fractional_mantissa[fractional_mantissa.index("1") + 1:]
    # Compute the exponent and convert to binary
    exp_bit = dec_to_bin(127 + exp)
    # Pad the exponent bits with 0s to the front if lesser than 8 bits
    exp_bit = ("0" * (8 - len(exp_bit))) + exp_bit 
    # Pad the mantissa with 0s to the back if shorter than 23 bits
    res_mantissa += "0" * (23 - len(res_mantissa))
    # Recurring fractions can result in a long mantissa string
    # Slice the string to keep exactly only 23 bits
    if len(res_mantissa) > 23:
        res_mantissa = res_mantissa[:23]

    # Join all the bits together and form the result string
    res = sign_bit + " | " + exp_bit + " | " + res_mantissa
    return res



if __name__ == "__main__":
    interface()