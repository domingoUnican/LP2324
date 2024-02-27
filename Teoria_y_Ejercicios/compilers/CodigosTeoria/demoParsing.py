lista_tokens = [('NUM',3), '*', ('NUM',4)]

def factor (lista_tokens):

    tokens = lista_tokens[0]

    if tokens [0] == 'NUM':

        return tokens[1]

    else:

        if tokens [0] == '(':
            valor = exp(lista_tokens[1:])
            if lista_tokens[0] == ')':
               return valor

            else:
                return "ERROR"


def term(lista_tokens):
    valor = factor(lista_tokens)
    if len(lista_tokens) > 1:
        if lista_tokens[0] =='*':
            valor = valor* term(lista_tokens[1:])
        return valor



