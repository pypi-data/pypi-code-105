import dis


# Метакласс для проверки соответствия сервера:
class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):

        methods = []

        attrs = []

        for func in clsdict:

            try:

                return_func = dis.get_instructions(clsdict[func])

            except TypeError:
                pass
            else:

                for i in return_func:
                    print(i)

                    if i.opname == 'LOAD_GLOBAL':  # i - Instruction,
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        print(methods)

        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо'
                            ' в серверном классе')

        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')

        super().__init__(clsname, bases, clsdict)


class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        # Список методов, которые используются в функциях класса:
        methods = []
        for func in clsdict:
            # Пробуем
            try:
                return_func = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
            except TypeError:
                pass
            else:
                # Раз функция, разбираем код, получая используемые методы.
                for i in return_func:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)

        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе обнаружено использование '
                                'запрещённого метода')

        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, '
                            'работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)
