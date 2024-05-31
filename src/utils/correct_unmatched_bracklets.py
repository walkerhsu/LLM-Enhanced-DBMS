# Description: This function corrects the unmatched brackets in the given command.
# Example:
# ({)
# ({}{{})

def correct_unmatched_brackets(command:str):
    # brackets type: (), {}, []
    stack = []
    i = 0
    while i < len(command):
        if command[i] == "(":
            stack.append("(")
        elif command[i] == "{":
            stack.append("{")
        elif command[i] == "[":
            stack.append("[")
        target_bracklet = command[i]
        if command[i] == ")" or command[i] == "}" or command[i] == "]":
            while (len(stack) != 0) and (i < len(command)):
                # ()
                if (stack[-1] == "("):
                    if (target_bracklet == ")"):
                        stack.pop()
                        break
                    command = command[:i] + ')' + command[i:]
                    i += 1
                    stack.pop()
                # {}
                elif (stack[-1] == "{"):
                    if (target_bracklet == "}"):
                        stack.pop()
                        break
                    command = command[:i] + '}' + command[i:]
                    i += 1
                    stack.pop()
                # []
                elif (stack[-1] == "["):
                    if (target_bracklet == "]"):
                        stack.pop()
                        break
                    command = command[:i] + ']' + command[i:]
                    i += 1
                    stack.pop()
        i += 1
    if len(stack) != 0:
        print(stack)
        for bracket in reversed(stack):
            if bracket == "(":
                command += ")"
            elif bracket == "{":
                command += "}"
            elif bracket == "[":
                command += "]"

    return command