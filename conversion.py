def decimal_to_binary(decimal):
    """
    returns a verbose instruction on converting from decimal to binary bases, along with the result.
    """
    instructions = ""
    result = ""
    while decimal != 0:
        quotient = decimal//2
        remainder = decimal%2
        result += str(remainder)
        instructions += f"{decimal} is divided by 2, giving a quotient of {quotient} and a remainder of {remainder}. The remainder {remainder} will be added to the binary digits result to get {result}.\n"
        decimal = quotient
    result = result[::-1]
    instructions += f"Reverse the binary digit result to get {result}."
    return (instructions, result)

def binary_to_decimal(binary):
    """
    Returns a verbose instruction on converting from binary to decimal bases, along with the result.
    """
    instructions = ""
    result = 0
    for i, digit in enumerate(reversed(binary)):
        if digit == '1':
            result += 2**i
            instructions += f"The {i+1}-th binary digit from the right is 1, so add 2^{i} ({2**i}) to the decimal result to get {result}.\n"
        else:
            instructions += f"The {i+1}-th binary digit from the right is 0, there is no need to add anything to the decimal result.\n"
    return (instructions, result)

def decimal_to_hexadecimal(decimal):
    """
    Returns a verbose instruction on converting from decimal to hexadecimal bases, along with the result.
    """
    instructions = ""
    result = ""
    while decimal != 0:
        quotient = decimal//16
        remainder = decimal%16
        if remainder < 10:
            result += str(remainder)
            instructions += f"{decimal} is divided by 16, giving a quotient of {quotient} and a remainder of {remainder}. The remainder {remainder} will be added to the hexadecimal digits result to get {result}.\n"
        else:
            hex_letters = ['A', 'B', 'C', 'D', 'E', 'F']
            hex_digit = hex_letters[remainder - 10]
            result += hex_digit
            instructions += f"{decimal} is divided by 16, giving a quotient of {quotient} and a remainder of {remainder}. The letter {hex_digit} ({hex_digit}={remainder}) will be added to the hexadecimal digits result to get {result}.\n"
        decimal = quotient
    result = result[::-1]
    instructions += f"Reverse the hexadecimal digit result to get {result}."
    return (instructions, result)

def hexadecimal_to_decimal(hexadecimal):
    """
    Returns a verbose instruction on converting from hexadecimal to decimal bases, along with the result.
    """
    instructions = ""
    result = 0
    for i, digit in enumerate(reversed(hexadecimal)):
        if digit.isdigit():
            result += int(digit) * (16**i)
            instructions += f"The {i+1}-th hexadecimal digit from the right is {digit}, so add {digit} * 16^{i} to the decimal result to get {result}.\n"
        else:
            hex_letters = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
            result += hex_letters[digit] * (16**i)
            instructions += f"The {i+1}-th hexadecimal digit from the right is {digit}, which represents {hex_letters[digit]}, so add {hex_letters[digit]} * 16^{i} to the decimal result to get {result}.\n"
    return (instructions, result)

#main
#print(decimal_to_hexadecimal(123456))