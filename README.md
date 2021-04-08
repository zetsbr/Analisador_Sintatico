# Título: Analisador Sintatico

## Autor: 

- João Porto RA170291 (jvaporto@gmail.com)

## Resumo:

Implementação de um analisador sintático funcional para a linguagem Lalgol para a matéria de Compiladores II 

## Organização dos arquivos:

```
├── Analisador_Sintatico.py: O analisador sintatico propriamente dito.
├── README.md: Instrucoes sobre a ferramenta.
├── Automatos.pdf: Arquvio contendo as ilustrações dos autômatos implementados dentro do analisador sintático.
├── Automatos.pdf: Arquivo com as intruções da linguagem Lalgol e códigos de exemplo.
└── txt.txt: Arquivo contendo os comandos da lingaugem Lalgol que serão consumidos pelo analisador léxico.
```

## Dependências:

Para a execução do código é necessário ter python 3.7.6 ou superior (https://www.python.org/downloads/)

Para os usuários de windows é necessário adicionar o python as variáveis de ambiente durante a instalação

## Execução:

Para ler um código com para teste coloque ele dentro do arquivo txt.txt, Os erros identificados serão mostrados ao fim da execução indicando qual o tipo e a linha que se encontra.

Para o teste foram utilizados os codigos de exemplo assim como foram mostrados e algumas versões com erros forçados para teste das funções.

No caso da execução no windows é iteressante utilizar o idle pois este não fechará após a execução e será possível visualizar os possíveis erros e mensagens do código.