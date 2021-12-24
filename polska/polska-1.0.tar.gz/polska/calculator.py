def polska(expression: str):
    """Преобразование в обратную польскую запись вводимого числа
    >>> polska('1+2+3')
    '12+3+'
    """
    variations = {'0': ('four', 'one', 'one', 'one', 'one', 'one', 'five'),
                  '1': ('two', 'two', 'two', 'one', 'one', 'one', 'two'),
                  '2': ('two', 'two', 'two', 'one', 'one', 'one', 'two'),
                  '3': ('two', 'two', 'two', 'two', 'two', 'one', 'two'),
                  '4': ('two', 'two', 'two', 'two', 'two', 'one', 'two'),
                  '5': ('five', 'one', 'one', 'one', 'one', 'one', 'three')}
    cipher = {'!': 0,
              '+': 1,
              '-': 2,
              '*': 3,
              '/': 4,
              '(': 5,
              ')': 6}
    checkout = ['!']
    checklist = 'abcdefghijklmnopqrstuvwxyz1234567890/+-*()'
    expression = list(expression)
    if expression.count('(') != expression.count(')'):
        raise ValueError('Проверьте правильность написания скобок')
    elif not set(expression).issubset(checklist):
        raise ValueError('Выражение введено неверно')

    expression.append('!')
    result = []
    for i in expression:
        strelka = 0
        while strelka == 0:
            if i.isdigit() or i.isalpha():
                result.append(i)
                strelka += 1
            else:
                func = variations[str(cipher[checkout[-1]])][int(cipher[i])]
                if func == 'one':
                    checkout.append(i)
                elif func == 'two':
                    result.append(checkout[-1])
                    checkout.pop()
                    continue
                elif func == 'three':
                    checkout.pop()
                elif func == 'four':
                    f"Переработанный результат:\n{''.join(result)}"
                elif func == 'five':
                    raise ValueError('Ошибка в написании формулы, попробуйте снова')

                strelka += 1
    return ''.join(result)





