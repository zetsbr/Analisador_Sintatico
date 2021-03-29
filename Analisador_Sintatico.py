#autor: João Vitor de Andrade Porto
#para usar favor tenhar um arquivo chamado txt.txt contendo o código em lalgol
num=['1','2','3','4','5','6','7','8','9','0','.']
ch=['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','ç']
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
linha_ant=linha
def Analisador_Lexico(i):
    global texto, erro, linha, reservado, relacional, separador, cmd, operador, alfabeto, linha_ant
    achou=False
    token=''
    retorno=''
    linha_ant=linha
    while(i<len(texto) and not(achou)):
        if((texto[i]=='\n')):
            linha=linha+1
        elif(texto[i]=='{'):
            while(texto[i]!='}'):
                i=i+1
        elif(texto[i] != ' '):
            if(not(texto[i] in alfabeto) and not(texto[i] in reservado)):
                se='erro na linha {}: caracter invalido em {}'.format(linha,texto[i])
                erro.append(se)
                retorno='erro_lexico'
            else:
                token=token+texto[i]
                if((texto[i+1] in separador) or (texto[i+1] in operador) or (texto[i] in separador) or (texto[i] in relacional) or (texto[i] in operador) or (texto[i+1]+texto[i+2] in separador) or (texto[i+1]+texto[i+2] in relacional) or (texto[i+1] in relacional) or (not(texto[i+1] in alfabeto) and not(texto[i+1] in reservado))):
                    if((token in reservado) or (token=='end.') or (token=='.')):
                        if(token=='end.'):
                            i=i-1
                            token=token[:-1]
                        if((token in relacional) and (texto[i+1] in relacional) or (token+texto[i+1] in separador)):
                            i=i+1
                            token=token+texto[i]
                        retorno=token
                    elif(list(filter(token.startswith,num))!= []):
                        if(not(any(l in [c for c in token] for l in ch))):
                            if('.' in token):
                                if(not(token.endswith('.'))):
                                    retorno='real'
                                else:
                                    se='erro na linha {}: numero real incompleto em {}'.format(linha,token)
                                    erro.append(se)
                                    retorno='erro_lexico'
                            else:
                                print(token + ' - ' + 'inteiro')
                                retorno='integer'
                        else:
                            se='erro na linha {}: numero mal formado em {}'.format(linha,token)
                            erro.append(se)
                            retorno='erro_lexico'
                    else:
                        if(not('.' in token)):
                            retorno='ident'
                        else:
                            se='erro na linha {}:identificador mal formado em {}'.format(linha,token)
                            erro.append(se)
                            retorno='erro_lexico'
                    achou=True
                    token=''
        i=i+1
    return(i,retorno)


def consome_simbolo():
    global i,ret,i_ant
    i_ant=i
    i,ret=Analisador_Lexico(i)
    while(ret=='erro_lexico'):
        i_ant=i
        i,ret=Analisador_Lexico(i)

def insere_erro(se):
    global i,ret,i_ant,linha
    se='erro na linha {}: esperado {} mas foi obtido "{}"'.format(linha,se,ret)
    erro.append(se)
    i=i_ant
    if(linha_ant!=linha):
        linha=linha-1

def fator():
    global i,ret,i_ant,linha
    if(ret=='(' or ret=='ident' or ret=='integer' or ret=='real'):
        if(ret=='('):
            consome_simbolo()
            expressao()
            consome_simbolo()
            if(not(ret==')')):
                insere_erro('")"')
    else:
        insere_erro('"(" ou "ident" ou "integer" ou "real"')

def op_mul():
    if(not(ret=='*' or ret=='/')):
        insere_erro('"*" ou "/"')

def mais_fatores():
    global i,linha
    if(ret=='*' or ret=='/'):
        op_mul()
        consome_simbolo()
        fator()
        consome_simbolo()
        mais_fatores()
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def termo():
    op_un()
    consome_simbolo()
    fator()
    consome_simbolo()
    mais_fatores()

def op_ad():
    if(not(ret=='+' or ret=='-')):
        insere_erro('"+" ou "-"')     

def outros_termos():
    global i,linha
    if(ret=='+' or ret=='-'):
        op_ad()
        consome_simbolo()
        termo()
        consome_simbolo()
        outros_termos()
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def op_un():
    global i,linha
    if(not(ret=='+' or ret=='-')):
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def expressao():
    termo()
    consome_simbolo()
    outros_termos()

def relacao():
    if(not(ret=='=' or ret=='<>' or ret=='>=' or ret=='<=' or ret=='>' or ret=='<')):
        insere_erro('"=" ou "<>" ou ">=" ou "<=" ou ">" ou "<"')

def condicao():
    expressao()
    consome_simbolo()
    relacao()
    consome_simbolo()
    expressao()

def comandos():
    global i,linha
    if(ret=='read' or ret=='write' or ret=='while' or ret=='if' or ret=='ident' or ret=='begin'):
        cmd()
        consome_simbolo()
        if(not(ret==';')):
            insere_erro('";"')
        consome_simbolo()
        comandos()
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1
        
def cmd():
    global i,linha
    if(ret=='read'):
        consome_simbolo()
        if(not(ret=='(')):
            insere_erro('"("')
        consome_simbolo()
        variaveis()
        consome_simbolo()
        if(not(ret==')')):
            insere_erro('")"')
    elif(ret=='write'):
        consome_simbolo()
        if(not(ret=='(')):
            insere_erro('"("')
        consome_simbolo()
        variaveis()
        consome_simbolo()
        if(not(ret==')')):
            insere_erro('")"')
    elif(ret=='while'):
        consome_simbolo()
        condicao()
        consome_simbolo()
        if(not(ret=='do')):
            insere_erro('"do"')
        consome_simbolo()
        cmd()
    elif(ret=='if'):
        consome_simbolo()
        condicao()
        consome_simbolo()
        if(not(ret=='then')):
            insere_erro('"then"')
        consome_simbolo()
        cmd()
        consome_simbolo()
        pfalsa()
    elif(ret=='ident'):
        consome_simbolo()
        if(ret==':='):
            consome_simbolo()
            expressao()
        elif(ret=='('):
            lista_arg()
        else:
            insere_erro('":=" ou "("')
            while(ret!=';'):
                consome_simbolo()
            i=i_ant
            if(linha_ant!=linha):
                linha=linha-1
    elif(ret=='begin'):
        consome_simbolo()
        comandos()
        consome_simbolo()
        if(not(ret=='end')):
            insere_erro('"end"')
    
def lista_arg():
    global i,linha
    if(ret=='('):
        consome_simbolo()
        argumentos()
        consome_simbolo()
        if(not(ret==')')):
            insere_erro('")"')
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def mais_ident():
    global i,linha
    if(ret==';'):
        consome_simbolo()
        argumentos()
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def pfalsa():
    global i,linha
    if(ret=='else'):
        consome_simbolo()
        cmd()
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def argumentos():
    if(not(ret=='ident')):
        insere_erro('"ident"')
    consome_simbolo()
    mais_ident()

def tipo_var():
    if(not(ret=='integer' or ret=='real')):
        insere_erro('"integer" ou "real"')

def mais_var():
    global i,linha
    if(ret==','):
        consome_simbolo()
        variaveis()
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1
        
def variaveis():
    if(not(ret=='ident')):
        insere_erro('"ident"')
    consome_simbolo()
    mais_var()

def dc_v():
    global i,linha
    if(ret=='var'):
        consome_simbolo()
        variaveis()
        consome_simbolo()
        if(not(ret==':')):
            insere_erro('":"')
        consome_simbolo()
        tipo_var()
        consome_simbolo()
        if(not(ret==';')):
            insere_erro('";"')
        consome_simbolo()
        dc_v()
    elif(not(ret=='procedure')):
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def lista_par():
    variaveis()
    consome_simbolo()
    if(not(ret==':')):
        insere_erro('":"')
    consome_simbolo()
    tipo_var()
    consome_simbolo()
    mais_par()

def mais_par():
    global i,linha
    if(ret==';'):
        consome_simbolo()
        lista_par()
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def parametros():
    global i,linha
    if(ret=='('):
        consome_simbolo()
        lista_par()
        consome_simbolo()
        if(not(ret==')')):
            insere_erro('")"')
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def dc_loc():
    dc_v()

def corpo_p():
    dc_loc()
    consome_simbolo()
    if(not(ret=='begin')):
        insere_erro('"begin"')
    consome_simbolo()
    comandos()
    consome_simbolo()
    if(not(ret=='end')):
        insere_erro('"end"')
    consome_simbolo()
    if(not(ret==';')):
        insere_erro('";"')
        
def dc_p():
    global i,linha
    if(ret=='procedure'):
        consome_simbolo()
        if(not(ret=='ident')):
            insere_erro('"ident"')
        consome_simbolo()
        parametros()
        consome_simbolo()
        if(not(ret==';')):
            insere_erro('";"')
        consome_simbolo()
        corpo_p()
        consome_simbolo()
        dc_p()
    else:
        i=i_ant
        if(linha_ant!=linha):
            linha=linha-1

def dc():
    global i,ret,i_ant,linha
    if(ret=='var' or ret=='procedure'):
        dc_v()
        dc_p()
    else:
        insere_erro('""var" ou "procedure""')

def corpo():
    dc()
    consome_simbolo()
    if(not(ret=='begin')):
        insere_erro('"begin"')
    consome_simbolo()
    comandos()
    consome_simbolo()
    if(not(ret=='end')):
        insere_erro('"end"')
    
def programa():
    print('Processo de análise sintática sendo realizado, por favor aguarde')
    consome_simbolo()
    if(not(ret=='program')):
        insere_erro('"program"')
    consome_simbolo()
    if(not(ret=='ident')):
        insere_erro('"ident"')
    consome_simbolo()
    if(not(ret==';')):
        insere_erro('";"')
    consome_simbolo()
    corpo()
    consome_simbolo()
    if(not(ret=='.')):
        insere_erro('"."')
    print('Processo de análise sintática finalizada, imprimindo lista de erros')

programa()
print(linha)
print('\nerros: ')
for er in erro:
    print(er)


