# Projeto de Implementação de um Compilador para a Linguagem TPP: Análisador Sintática (Trabalho – 2ª parte)
#### Gustavo Kioshi Asato
#### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
## 1 Introdução
correção de gramatica
O Análisador Sintático é uma parte do compilador que visa a partir os tokens do analizador lexico gerar uma arvore sintatica. Onde cada nó da arvore representa uma expressão regular e as folhas sendo cada token. Serve  para detecção de erros no codigo pois o analisador sintatico 
### 2 Objetivo
Nessa atividade foi desenvolvido um analizador sintatico para alinguagem TPP, com detecção de erros sendo disponibilizado um codigo base pelo professor, sendo oferecido casos de testes para ter melhor conhecimento sobre a atividade. sendo desenvolvoda em python com as seguintes bibliotecas PLY servindo para iniciar o compilador, anytree mostrar a arvore que a o teste gera, graphviz mostrar em .png as arvores geradas no windows.
### 3 Descrição da gramática
A gramatica da linguagem TPP as regras são definidas pelo padrão BNF(Backus Naur Form) ás regras estão disponibilizados na tabela de tokens.
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

Na figura abaixo utilizou o token tipo para demostrar como ele realizava a chama de outros tokens na tabela de tokens, diagrama de definição de tipo. Sendo possivel selecionar um desses tokens inteiro, flutuante.

<img src="tipo.png" style="height: 100px; width:200px;"/>

Na figura abaixo utilizou o token definição de variaveis para demostrar como ele realizava a chama de outros tokens na tabela de tokens, diagrama de definição de variavel. Sendo possivel selecionar um desses tokens ID, ABRE_COLCHETE, expressao, FECHA_COLCHETE.

<img src="defini_variavel.png" style="height: 100px; width:600px;"/>

Na figura abaixo utilizou o token acao para demostrar como ele realizava a chama de outros tokens na tabela de tokens, diagrama de definição de corpo. Sendo possivel selecionar um desses tokens expressao, declaracao_variaveis, se, repita, leia, escreva, retorna, erro.

<img src="acao.png" style="height: 300px; width:200px;"/>

### 4 Formato da Analise Sintática

Para gerar a arvore sintatica é necessario ter as seguintes bibliotecas do graphviz, para gerar o png e a arvore no terminal.
Na figura abaixo demostra a arvore gerada pelo bublesort.

<img src="bubble_sort.tpp.unique.ast.png"/>

### 5 Implementação
### 6 Resultados
