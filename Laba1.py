def f(tokens):
    if len(tokens) == 0:
        raise ValueError("Ошибка: пустое выражение!")
    for token in tokens:
        if token.isalpha() and token != "abs":
            raise ValueError("Ошибка: неизвестное имя!")
    for token in tokens:
        if not token.isalpha() and token != "!=":
            try:
                float(token)
            except ValueError:
                if token not in ["+", "-", "*", "/", "(", ")"]:
                    raise ValueError("Ошибка: некорректная запись!")
    if tokens[-1] == "abs":
        raise ValueError("Ошибка: неправильный вызов abs")
    for i in range(len(tokens) - 1):
        if tokens[i] == "abs" and tokens[i+1] != "(":
            raise ValueError("Ошибка: неправильный вызов abs!")
        
    if tokens[-1] in ["+","-","*","/","!="]:
        raise ValueError("Ошибка: выражение не закончено!")
    depth = 0
    for token in tokens:
        if token == "(":
            depth +=1
        if token == ")":
            depth -=1
        if depth < 0:
            raise ValueError("Ошибка: неправильный порядок скобок!")
    if depth > 0:
        raise ValueError("Ошибка: не хватает закрывающей скобки!")
    operators = ["+","-","*","/","!="]
    for i in range(len(tokens) - 1):
        if tokens[i] in operators and tokens[i + 1] in operators:
            raise ValueError("Ошибка: некорректное выражение")
    for i in range(len(tokens) - 1):
        first_is_number = False
        second_is_number = False
        try:
            float(tokens[i])
            first_is_number = True
        except ValueError:
            pass
        
        try:
            float(tokens[i + 1])
            second_is_number = True
        except ValueError:
            pass

        if first_is_number and second_is_number:
            raise ValueError("Ошибка: два числа подряд")
    if tokens.count("!=") > 1:
        raise ValueError("Ошибка: несколько операторов != в выражении!")
    if "!=" in tokens:
        index = tokens.index("!=")
        left = tokens[:index]
        right = tokens[index + 1:]
        return float(f(left)) != float(f(right))
    while "(" in tokens:
        start = tokens.index("(")
        depth = 0
        end = None
        for i in range(start , len(tokens)):
            if tokens[i] == "(": depth += 1
            elif tokens[i] == ")":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end is None:
            raise ValueError("Ошибка: не хватает закрывающей скобки!")
        inside = tokens[start + 1: end]
        inside_result = f(inside)
        if start > 0 and tokens[start - 1] == 'abs':
            tokens[start - 1: end + 1] = [str(abs(inside_result))]
        else:
            tokens[start : end + 1] = [str(inside_result)]
    for i in range(len(tokens) - 1):
        first_is_number = False
        second_is_number = False
        try:
            float(tokens[i])
            first_is_number = True
        except ValueError:
            pass
        try:
            float(tokens[i + 1])
            second_is_number = True
        except ValueError:
            pass
        if first_is_number and second_is_number:
            raise ValueError("Ошибка: между числами нет оператора")
        
    i = 1
    while i < len(tokens) - 1:
        operator = tokens[i]
        if operator == "*":
            a = float(tokens[i - 1])
            b = float(tokens[i + 1])
            value = a * b
            tokens[i-1:i+2] = [str(value)]
            i = 1
        elif operator == "/":
            a = float(tokens[i - 1])
            b = float(tokens[i + 1])
            value = a / b
            tokens[i-1:i+2] = [str(value)]
            i = 1
        else:
            i+=2
    result = float(tokens[0])
    i = 1
    while i < len(tokens):
        operator = tokens[i]
        b = float(tokens[i+1])
        if operator == "+":
            result += b
        elif operator == "-":
            result -= b
        i += 2
    return result

while True:
    expression = input("Введите выражение: ")
    if expression == 'break':
        break
    try:
        
        tokens = []
        number = ""
        i = 0
        while i < len(expression):
            char = expression[i]
            if char == "!" and i + 1 < len(expression) and expression[i + 1] == "=":
                if number != "":
                    tokens.append(number)
                    number = ""
                tokens.append("!=")
                i+=2
            else:
                if char.isdigit() or char == "." or char.isalpha():
                    number += char
                else:
                    if number != "":
                        tokens.append(number)
                        number = ""
                    if char != " ":
                        if char not in ["+","-","*","/","(",")"]:
                            raise ValueError("Ошибка: недопустимый символ!")
                        tokens.append(char)
                i+=1
        if number != "":
            tokens.append(number)
        for i in range(len(tokens) - 1):
            if tokens[i] in ["+","-"] and tokens[i+1] in ["+","-"]:
                if i == 0 or tokens[i - 1] not in ["*","/","("]:
                    raise ValueError("Ошибка: несколько знаков подряд!")
        i = 0
        while i < len(tokens):
            if tokens[i] == "-" and (i == 0 or tokens[i - 1] in ["+","-","*","/","("]):
                if i + 1 >= len(tokens):
                    raise ValueError("Ошибка: после минуса нету числа")
                if tokens[i+1] == "(":
                    tokens[i:i+1] = ["-1", "*"]
                    i+=2
                    continue
                try:
                    float(tokens[i+1])
                except ValueError:
                    raise ValueError("Ошибка: после минуса ожидалось число!")
                else:
                    tokens[i:i+2] = [str(-float(tokens[i+1]))]
            elif tokens[i] == "+" and (i == 0 or tokens[i - 1] in ["+","-","*","/","("]):
                tokens[i:i+1] = []
            else:
                i+=1
        result = f(tokens)
        print(result)
    except ZeroDivisionError:
        print("Ошибка: деление на ноль!")
    except ValueError as e:
        print(e)
