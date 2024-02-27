lista_tokens = [('NUM',3), '+', '*', ('NUM',4), '-', ('NUM',5)]


def accept(tipp):
    return

def expression(lista_tokes):

    valor = term(lista_tokens)
    if len(lista_tokens) == 1:  #expresion: term
        return term(lista_tokens[0])
    else:
        if lista_tokens[1] == '*':
            return term(lista_tokens[0:1]) + expresion(lista_tokens[2:])
        if lista_tokens[1] == '-':
            return term(lista_tokens[0:1]) - expresion(lista_tokens[2:])
         
    
def factor (lista_tokens):

    tokens = lista_tokens[0]

    if tokens [0] == 'NUM':

        return token[1]

    else:

        if tokens [0] == '(':
            valor = exp(lista_tokens[1:])
            if lista_tokens[0] == ')':
               return valor

            else:
                return "ERROR"


def term(lista_tokens):
   #esta parte corresponde a term: factor
   if len(lista_tokens) == 1:  
       return facttor(lista_tokens)
   # la lista de tokens es mas larga term: factor '*' term
   else: 
       return factor(lista_tokens[0]) * term(lista_tokens[2:])



