from algorithms import Node, DLL

def decimal_to_binary(decimal):
    """
    returns a verbose instruction on converting from decimal to binary bases, along with the result.
    """
    instructions = ""
    result = ""
    instructions_list = DLL()
    while decimal != 0:
        quotient = decimal//2
        remainder = decimal%2
        result += str(remainder)
        instructions += f"{decimal} is divided by 2, giving a quotient of {quotient} and a remainder of {remainder}. The remainder {remainder} will be added to the binary digits result.\n"
        instructions_list.insert_back((f"{decimal} is divided by 2, giving a quotient of {quotient} and a remainder of {remainder}. The remainder {remainder} will be added to the binary digits result.)", result))
        decimal = quotient
    instructions += f"Reverse the binary digit result."
    result = result[::-1]
    return (instructions, result, instructions_list)

# main
# print(decimal_to_binary(123456))