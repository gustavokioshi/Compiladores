# Projeto de Implementação de um Compilador para a Linguagem TPP: Análisador Sintática (Trabalho – 2ª parte)
#### Gustavo Kioshi Asato
#### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
## 1 Introdução
correção de gramatica
O Analisador Sintático é uma parte do compilador que visa a partir os tokens do analisador léxico gerar uma árvore sintática. Onde cada nó da árvore representa uma expressão regular e as folhas sendo cada token. Serve para detecção de erros no código, pois o analisador sintático.
### 2 Objetivo
Nessa atividade foi desenvolvido um analisador sintático para a linguagem TPP, com detecção de erros sendo disponibilizado um código base pelo professor, sendo oferecido casos de testes para ter melhor conhecimento sobre a atividade. Sendo desenvolvida em python com as seguintes bibliotecas PLY servindo para iniciar o compilador, anytree mostrar a árvore que ao teste gera, graphviz mostrar em .png as árvores geradas no windows.
### 3 Descrição da gramática
A gramática da linguagem TPP as regras são definidas pelo padrão BNF(Backus Naur Form) às regras estão disponibilizados na tabela de tokens.
|token|token|token|token|token|token|token|token|tokens|
|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|
|programa ::= |lista_declaracoes|
|lista_declaracoes ::= |lista_declaracoes declaracao|declaracao|
|declaracao ::=|declaracao_variaveis| inicializacao_variaveis| declaracao_funcao|
|declaracao_variaveis ::=|tipo DOIS_PONTOS lista_variaveis|
|inicializacao_variaveis ::=|atribuicao|
|lista_variaveis ::=|lista_variaveis VIRGULA var | var|
|var ::=|ID| ID indice|
|indice ::=|indice ABRE_COLCHETE expressao FECHA_COLCHETE | ABRE_COLCHETE expressao FECHA_COLCHETE|
|tipo ::=|INTEIRO|FLUTUANTE|
|declaracao_funcao ::=|tipo cabecalho|cabecalho|
|cabecalho ::=|ID ABRE_PARENTESE lista_parametros |FECHA_PARENTESE corpo FIM|
|lista_parametros ::=|lista_parametros VIRGULA parametro| parametro| vazio|
|parametro ::=|tipo DOIS_PONTOS ID|  parametro|ABRE_COLCHETE FECHA_COLCHETE|
|corpo ::=|corpo acao | vazio |
|acao ::=|expressao| declaracao_variaveis| se| repita| leia| escreva| retorna| erro|
|se ::=|SE expressao ENTAO corpo FIM| SE expressao ENTAO|corpo SENAO corpo FIM|
|repita ::=|REPITA corpo ATE expressao|
|atribuicao ::=|var ATRIBUICAO expressao|
|leia ::=|LEIA ABRE_PARENTESE var FECHA_PARENTESE|
|escreva ::=|ESCREVA ABRE_PARENTESE expressao|FECHA_PARENTESE|
|retorna ::=|RETORNA ABRE_PARENTESE expressao|FECHA_PARENTESE|
|expressao ::=|expressao_logica| atribuicao|
|expressao_logica ::=|expressao_simples| expressao_logica operador_logico expressao_simples|
|expressao_simples ::=|expressao_aditiva| expressao_simples|operador_relacional expressao_aditiva|
|expressao_aditiva ::=|expressao_multiplicativa|expressao_aditiva operador_soma expressao_multiplicativa|
|expressao_multiplicativa ::=|expressao_unaria| expressao_multiplicativa operador_multiplicacao|expressao_unaria|
|expressao_unaria ::=|fator| operador_soma fator| operador_negacao fator|
|operador_relacional ::=|MENOR| MAIOR | IGUAL | DIFERENTE | MENOR_IGUAL | MAIOR_IGUAL|
|operador_soma ::=|MAIS| MENOS|
|operador_logico ::=|E| OU|
|operador_negacao ::=|NAO|
|operador_multiplicacao ::=|VEZES| DIVIDE|
|fator ::=|ABRE_PARENTESE expressao FECHA_PARENTESE|var|chamada_funcao|numero|
|numero ::=|NUM_INTEIRO|NUM_PONTO_FLUTUANTE|NUM_NOTACAO_CIENTIFICA|
|chamada_funcao ::=|ID ABRE_PARENTESE lista_argumentos|FECHA_PARENTESE|
|lista_argumentos  ::=|lista_argumentos VIRGULA expressao|expressao|vazio|

Na figura abaixo utilizou o token tipo para demostrar como ele realizava a chama de outros tokens na tabela de tokens, diagrama de definição de tipo. Sendo possível selecionar um desses tokens inteiro, flutuante.

<img src="tipo.png" style="height: 100px; width:200px;"/>

Na figura abaixo utilizou o token definição de variáveis para demostrar como ele realizava a chama de outros tokens na tabela de tokens, diagrama de definição de variável. Sendo possível selecionar um desses tokens ID, ABRE_COLCHETE, expressão, FECHA_COLCHETE.

<img src="defini_variavel.png" style="height: 100px; width:600px;"/>

Na figura abaixo utilizou o token ação para demostrar como ele realizava a chama de outros tokens na tabela de tokens, diagrama de definição de corpo. Sendo possível selecionar um desses tokens expressão, declaracao_variaveis, se, repita, leia, escreva, retorna, erro.

<img src="acao.png" style="height: 300px; width:200px;"/>

### 4 Formato da Analise Sintática 
Considerando que o objetivo do analisador sintático é validar se o código fornecido possui erros de gramática podendo ser construída em um formato de árvore.

Para gerar a árvore sintática é necessário ter as seguintes bibliotecas do graphviz, para gerar o png e a árvore no terminal.
Na figura abaixo demostra a árvore gerada pelo bublesort.

<img src="bubble_sort.tpp.unique.ast.png"/>


Sendo cada no da árvore um token um nó na árvore sendo possível aplicar um token erro que só ocorre quando não for possível chegar a um nó folha valido. Figura abaixo representa um token error do índice em código.

```
def p_indice_error(p):
    """indice : ABRE_COLCHETE error FECHA_COLCHETE
                | indice ABRE_COLCHETE error FECHA_COLCHETE
    """

    print("Erro na definicao do indice. Expressao ou indice.")

    print("Erro:p[0]:{p0}, p[1]:{p1}, p[2]:{p2}, p[3]:{p3}".format(
        p0=p[0], p1=p[1], p2=p[2], p3=p[3]))
    error_line = p.lineno(2)
    father = MyNode(name='ERROR::{}'.format(error_line), type='ERROR')
    logging.error(
        "Syntax error parsing index rule at line {}".format(error_line))
    parser.errok()
    p[0] = father
```
### 5 Detalhes da implementação
Durante a execução do tppparse.py ele recebe um codigo que permite identificar a qual token vai ser endereçado o determinados conjuntos de caracteres. O input necessia de um codigo .tpp para utilizar o ttpparse.py sendo retornado uma arvore com todas as palavras nos nós folhas 

### 6 YACC(Yet Another Compiler Compiler)
O YACC (Yet Another Compiler Compiler)é utilizado para gerar o analizador sintatico, parte do compilador responsável por fornecer sentido sintático a um determinado código fonte, baseado LALR(1). 
O metodo utilizado pelo YACC é LALR(1) que possui um caracterizador mais forte que a analise SLR(1), e mais simples que a analise LR(1) sendo gerada tabelas sintaticas menor.

