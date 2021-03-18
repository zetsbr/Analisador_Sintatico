#autor: João Vitor de Andrade Porto
#para usar favor tenhar um arquivo chamado txt.txt contendo o código em lalgol
num=['1','2','3','4','5','6','7','8','9','0','.']
ch=['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
alfabeto=ch+num
operador=['+','-','*','/']
cmd=['read','write','if','then','else','while','do','begin','end','procedure','program','real','integer','var']
separador=[' ','(',')',',',';',':=',':','\n','{','}']
relacional=['=','<>','>=','<=','>','<']
reservado=operador+cmd+separador+relacional
linha=1
erro=[]
token=""
txt=open('txt.txt')
texto=txt.read()
texto=texto+'\n'
i=0
i_ant=i
ret=''
def Analisador_Lexico(i):
    global texto, erro, linha, reservado, relacional, separador, cmd, operador, alfabeto
    achou=False
    token=''
    retorno=''
    while(i<len(texto) and not(achou)):
        if(texto[i]=='\n'):
            linha=linha+1
        elif(texto[i]=='{'):
            while(texto[i]!='}'):
                i=i+1
        elif(texto[i] != ' '):
            if(not(texto[i] in alfabeto) and not(texto[i] in reservado)):
                se='erro na linha {}: caracter invalido em {}'.format(linha,texto[i])
                erro.append(se)
                #print(texto[i] + ' - ' + 'erro')
                retorno='erro_lexico'
            else:
                token=token+texto[i]
                if((texto[i+1] in separador) or (texto[i+1] in operador) or (texto[i] in separador) or (texto[i] in relacional) or (texto[i] in operador) or (texto[i+1]+texto[i+2] in separador) or (texto[i+1]+texto[i+2] in relacional) or (texto[i+1] in relacional) or (not(texto[i+1] in alfabeto) and not(texto[i+1] in reservado))):
                    if((token in reservado) or (token=='end.') or (token=='.')):
                        if(token=='end.'):
                            i=i-1
                            token=token[:-1]
                        if((token in relacional) and (texto[i+1] in relacional)):
                            i=i+1
                            token=token+texto[i]
                        #print(token + ' - ' + token)
                        retorno=token
                    elif(list(filter(token.startswith,num))!= []):
                        if(not(any(l in [c for c in token] for l in ch))):
                            if('.' in token):
                                if(not(token.endswith('.'))):
                                    #print(token + ' - ' + 'real')
                                    retorno='real'
                                else:
                                    se='erro na linha {}: numero real incompleto em {}'.format(linha,token)
                                    erro.append(se)
                                    #print(token + ' - ' + 'erro')
                                    retorno='erro_lexico'
                            else:
                                #print(token + ' - ' + 'inteiro')
                                retorno='integer'
                        else:
                            se='erro na linha {}: numero mal formado em {}'.format(linha,token)
                            erro.append(se)
                            #print(token + ' - ' + 'erro')
                            retorno='erro_lexico'
                    else:
                        if(not('.' in token)):
                            #print(token + ' - ' + 'identificador')
                            retorno='ident'
                        else:
                            se='erro na linha {}:identificador mal formado em {}'.format(linha,token)
                            erro.append(se)
                            #print(token + ' - ' + 'erro')
                            retorno='erro_lexico'
                    achou=True
                    token=''
        i=i+1   
    return(i,retorno)

def fator():
    global i,ret,i_ant
    if(ret=='(' or ret=='ident' or ret=='integer' or ret=='real'):
        if(ret=='('):
            i_ant=i
            i,ret=Analisador_Lexico(i)
            expressao()
            i_ant=i
            i,ret=Analisador_Lexico(i)
            if(not(ret==')')):
                se='erro na linha {}: esperado ")" mas foi obtido "{}"'.format(linha,ret)
                erro.append(se)
    else:
        se='erro na linha {}: esperado "(" ou "ident" ou "integer" ou "real" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)

def op_mul():
    global i,ret,i_ant
    if(not(ret=='*' or ret=='/')):
        se='erro na linha {}: esperado "*" ou "/" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)

def mais_fatores():
    global i,ret,i_ant
    if(ret=='*' or ret=='/'):
        op_mul()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        fator()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        mais_fatores()
    else:
        i=i_ant

def termo():
    global i,ret,i_ant
    op_un()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    fator()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    mais_fatores()

def op_ad():
    global i,ret,i_ant
    if(not(ret=='+' or ret=='-')):
        se='erro na linha {}: esperado "+" ou "-" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)

def outros_termos():
    global i,ret,i_ant
    if(ret=='+' or ret=='-'):
        op_ad()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        termo()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        outros_termos()
    else:
        i=i_ant

def op_un():
    global i,ret,i_ant
    if(not(ret=='+' or ret=='-')):
        i=i_ant

def expressao():
    global i,ret,i_ant
    termo()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    outros_termos()

def relacao():
    global i,ret,i_ant
    if(not(ret=='=' or ret=='<>' or ret=='>=' or ret=='<=' or ret=='>' or ret=='<')):
        se='erro na linha {}: esperado "=" ou "<>" ou ">=" ou "<=" ou ">" ou "<" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)

def condicao():
    global i,ret,i_ant
    expressao()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    relacao()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    expressao()

def comandos():
    global i,ret,i_ant
    if(ret=='read' or ret=='write' or ret=='while' or ret=='if' or ret=='ident' or ret=='begin'):
        cmd()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret==';')):
            se='erro na linha {}: esperado ";" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        comandos()
    else:
        i=i_ant
        
def cmd():
    global i,ret,i_ant
    if(ret=='read'):
        if(not(ret=='(')):
            se='erro na linha {}: esperado "(" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        variaveis()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret==')')):
            se='erro na linha {}: esperado ")" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
    elif(ret=='write'):
        if(not(ret=='(')):
            se='erro na linha {}: esperado "(" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        variaveis()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret==')')):
            se='erro na linha {}: esperado ")" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
    elif(ret=='while'):
        condicao()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret=='do')):
            se='erro na linha {}: esperado "do" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        cmd()
    elif(ret=='if'):
        condicao()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret=='then')):
            se='erro na linha {}: esperado "then" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        cmd()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        pfalsa()
    elif(ret=='ident'):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(ret==':='):
            i_ant=i
            i,ret=Analisador_Lexico(i)
            expressao()
        else:
            lista_arg()
    elif(ret=='begin'):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        comandos()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret=='end')):
            se='erro na linha {}: esperado "end" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
    
def lista_arg():
    global i,ret,i_ant
    if(ret=='('):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        argumentos()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret==')')):
            se='erro na linha {}: esperado ")" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
    else:
        i=i_ant

def mais_ident():
    global i,ret,i_ant
    if(ret==';'):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        argumentos()
    else:
        i=i_ant

def pfalsa():
    global i,ret,i_ant
    if(ret=='else'):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        cmd()
    else:
        i=i_ant

def argumentos():
    global i,ret,i_ant
    if(not(ret=='ident')):
        se='erro na linha {}: esperado "ident" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    mais_ident()

def tipo_var():
    global i,ret,i_ant
    if(not(ret=='integer' or ret=='real')):
        #print(ret)
        se='erro na linha {}: esperado "integer" ou "real" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)

def mais_var():
    global i,ret,i_ant
    if(ret==','):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        #print(ret)
        variaveis()
    else:
        i=i_ant
        
def variaveis():
    global i,ret,i_ant
    if(not(ret=='ident')):
        se='erro na linha {}: esperado "ident" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    #print(ret)
    mais_var()

def dc_v():
    global i,ret,i_ant
    if(ret=='var'):
        #print(ret)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        #print(ret)
        variaveis()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        #print(ret)
        if(not(ret==':')):
            se='erro na linha {}: esperado ":" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        #print(ret)
        tipo_var()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret==';')):
            se='erro na linha {}: esperado ";" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        #print(ret)
        dc_v()
    else:
        i=i_ant

def lista_par():
    global i,ret,i_ant
    variaveis()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret==':')):
        se='erro na linha {}: esperado ":" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    tipo_var()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    mais_par()

def mais_par():
    global i,ret,i_ant
    if(ret==';'):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        lista_par()
    else:
        i=i_ant

def parametros():
    global i,ret,i_ant
    if(ret=='('):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        lista_par()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret==')')):
            se='erro na linha {}: esperado ")" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
    else:
        i=i_ant

def dc_loc():
    global i,ret,i_ant
    dc_v()

def corpo_p():
    global i,ret,i_ant
    dc_loc()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    print(ret)
    if(not(ret=='begin')):
        se='erro na linha {}: esperado "begin" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    comandos()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret=='end')):
        se='erro na linha {}: esperado "end" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret==';')):
        se='erro na linha {}: esperado ";" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)

def dc_p():
    global i,ret,i_ant
    if(ret=='procedure'):
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret=='ident')):
            se='erro na linha {}: esperado "ident" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        parametros()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        if(not(ret==';')):
            se='erro na linha {}: esperado ";" mas foi obtido "{}"'.format(linha,ret)
            erro.append(se)
        i_ant=i
        i,ret=Analisador_Lexico(i)
        corpo_p()
        i_ant=i
        i,ret=Analisador_Lexico(i)
        dc_p()
    else:
        i=i_ant

def dc():
    global i,ret,i_ant
    if(ret=='var' or ret=='procedure'):
        dc_v()
        dc_p()
    else:
        se='erro na linha {}: esperado "var" ou "procedure" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)

def corpo():
    global i,ret,i_ant
    dc()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret=='begin')):
        se='erro na linha {}: esperado "begin" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    comandos()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret=='end')):
        se='erro na linha {}: esperado "end" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    
def programa():
    global i, ret,i_ant
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret=='program')):
        se='erro na linha {}: esperado "program" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret=='ident')):
        se='erro na linha {}: esperado "ident" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret==';')):
        se='erro na linha {}: esperado ";" mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)
    i_ant=i
    i,ret=Analisador_Lexico(i)
    corpo()
    i_ant=i
    i,ret=Analisador_Lexico(i)
    if(not(ret=='.')):
        se='erro na linha {}: esperado "." mas foi obtido "{}"'.format(linha,ret)
        erro.append(se)

#i_ant=i
#i,ret=Analisador_Lexico(i)
#print(ret)
programa()
print('\nerros: ')
for er in erro:
    print(er)


