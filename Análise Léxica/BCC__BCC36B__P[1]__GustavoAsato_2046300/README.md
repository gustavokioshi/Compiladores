# Projeto de Implementação de um Compilador para a Linguagem TPP: Análise Léxica (Trabalho – 1ª parte)
#### Gustavo Kioshi Asato
#### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
## 1 Análisador Léxico
Nessa atividade desenvolvida durante a disciplina de Compiladores tem em foco desenvolver um analisador léxico que funcina como um sistema de varedura no codigo a ser compilado, separando os tokens. Os tokens são definidos no compilador sendo palavras reservadas ou símbolos. Cada token pode receber os proximos caracteres de acordo com a sua implementação de forma com que cada token possa ter uma entrada necessaria para retornar para oque foi designada.
### 2 Linguagem T++
A linguagem T++ possui os seguintes tipos suportados interio e flutuante podendo ser armazenados em arrays unidimensional ou bidimensional. O tipo de aquivo para ser reconhecido como .tpp no final do arquivo.
### 2.1 Tokens
Os tokens são pré-definidos na criação do compilador. Sendo chamada toda vez que aparece no codigo a ser compilado, cada token possui uma ação especifica podendo tomar diversas descisões com determinados parametros que foram submetidos.
### 2.2 Operadores 
|token          |simbolo|
|---------------|------|
| MAIS          | +    |
| MENOS         | -    |
| MULTIPLICACAO | *    |
| DIVISAO       | /    |
| E_LOGICO      | &&   |
| OU_LOGICO     | \|\| |
| DIFERENCA     | <>   |
| MENOR_IGUAL   | <=   |
| MAIOR_IGUAL   | >=   |
| MENOR         | <    |
| MAIOR         | >    |
| IGUAL         | =    |
| NEGACAO       | !    |


|token          |simbolo|
|---------------|------|
| ABRE_PARENTESE| (    |
| FECHA_PARENTESE| )    |
| ABRE_COLCHETE | [    |
| FECHA_COLCHETE|  ]   |
| VIRGULA      | ,   |
| DOIS_PONTOS    | :  |
| ATRIBUICAO     | :=  |
## 3 Linguagens de programação para a implementação
### 3.1 Python
O Python é uma linguagem de programação de alto nível utilizada em diferentes tipos de aplicações, em Machine Learning, no desenvolvimento de jogos. Sendo necessario para utilizar para poder compilar os codigos.
### 3.2 PLY
O PLY é uma biblioteca para python que permite desenvolver um compilador sendo necessario durante todo o desenvolvimento do projeto 
## 4 Testes
