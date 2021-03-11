#autor: João Vitor de Andrade Porto
#para usar favor tenhar um arquivo chamado txt.txt contendo o código em lalgol
num=['1','2','3','4','5','6','7','8','9','0','.']
ch=['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
alfabeto=ch+num
operador=['+','-','*','/']
cmd=['read','write','if','then','else','while','do','begin','end','.','procedure','program','real','integer','var']
separador=[' ','(',')',',',';',':=',':','\n','{','}']
relacao=['=','<>','>=','<=','>','<']
reservado=operador+cmd+separador+relacao
linha=1
erro=[]
token=""
txt=open('txt.txt')
texto=txt.read()
texto=texto+'\n'
i=0
retorno=''
while(i<len(texto)):
    if(texto[i]=='\n'):
        linha=linha+1
    elif(texto[i]=='{'):
        while(texto[i]!='}'):
            i=i+1
    elif(texto[i] != ' '):
        if(not(texto[i] in alfabeto) and not(texto[i] in reservado)):
            se='erro na linha {}: caracter invalido em {}'.format(linha,texto[i])
            erro.append(se)
            print(texto[i] + ' - ' + 'erro')
        else:
            token=token+texto[i]
            if((texto[i+1] in separador) or (texto[i+1] in operador) or (texto[i] in separador) or (texto[i] in relacao) or (texto[i] in operador) or (texto[i+1]+texto[i+2] in separador) or (texto[i+1]+texto[i+2] in relacao) or (texto[i+1] in relacao) or (not(texto[i+1] in alfabeto) and not(texto[i+1] in reservado))):
                if(token in reservado):
                    if((token in relacao) and (texto[i+1] in relacao)):
                        i=i+1
                        token=token+texto[i]
                    print(token + ' - ' + token)
                    retorno=token
                elif(token=='end.'):
                    print('end - end')
                    print('. - .')
                elif(list(filter(token.startswith,num))!= []):
                    if(not(any(l in [c for c in token] for l in ch))):
                        if('.' in token):
                            if(not(token.endswith('.'))):
                                print(token + ' - ' + 'real')
                                retorno='numero_real'
                            else:
                                se='erro na linha {}: numero real incompleto em {}'.format(linha,token)
                                erro.append(se)
                                print(token + ' - ' + 'erro')
                        else:
                            print(token + ' - ' + 'inteiro')
                            retorno='numero_int'
                    else:
                        se='erro na linha {}: numero mal formado em {}'.format(linha,token)
                        erro.append(se)
                        print(token + ' - ' + 'erro')
                else:
                    if(not('.' in token)):
                        print(token + ' - ' + 'identificador')
                        retorno='ident'
                    else:
                        se='erro na linha {}:identificador mal formado em {}'.format(linha,token)
                        erro.append(se)
                        print(token + ' - ' + 'erro')
            
                token=''
    i=i+1
print('\nerros: ')
print(erro)

