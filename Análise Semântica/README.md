# Projeto de Implementação de um Compilador para a Linguagem TPP: Análise Semantica (Trabalho – 3ª parte)
#### Gustavo Kioshi Asato
#### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
## 1 Análise Semantica
Nessa atividade desenvolvida durante a disciplina de Compiladores tem em foco desenvolver um analisador semantico que funcina como um sistema de varedura no codigo a ser compilado, separando os tokens. Os tokens são definidos no compilador sendo palavras reservadas ou símbolos dispinilizados em formato de arvore pelo analise sintatica. Cada token pode receber os proximos caracteres de acordo com a sua implementação de forma com que cada token possa ter uma entrada necessaria para retornar para oque foi designada.
O teste a ser analizado 'sema005.tpp'.
### 2 Tabela de Simbolos
Durante a analise Semantica ha dois objetivos que devem ser completados, sendo eles a construcao da tabela de simbolos, e a identificacao de erros e avisos, assim como os erros e avisos esperados no conjunto de testes especificamente para analise semantica, e por fim, podar a arvore Sintatica, o que resultara em uma arvore sintatica abstrata. A criacao da tabela de simbolos neste caso for felta durante a propria analise Semantica, mais especificamente, antes de verificar as regras semanticas, ja que ela sera utilizada para realizar este passo. A tabela gerada ao fim e semelhante a tabela abaixo.

| Token |   Lexema  |   Tipo  | dim | tam_dim1 | tam_dim2 |   escopo  | init | linha | funcao |      parametros      |        valor         | retorno |
|-------|-----------|---------|-----|----------|----------|-----------|------|-------|--------|----------------------|----------------------|---------|
|   ID  |    func   | inteiro |  0  |    0     |    0     |   global  |  N   |   4   |   S    | |inteiro=x|inteiro=y | |inteiro=x|inteiro=y |    S    |
|   id  |     x     | inteiro |  0  |    0     |    0     |    func   |  N   |   4   |   N    |         None         |                      |  vazio  |
|   id  |     y     | inteiro |  0  |    0     |    0     |    func   |  N   |   4   |   N    |         None         |                      |  vazio  |
|   ID  |     x     |   None  |  0  |    0     |    0     |    func   |  N   |   5   |   N    |         None         |         None         |  vazio  |
|   ID  |     y     |   None  |  0  |    0     |    0     |    func   |  N   |   5   |   N    |         None         |         None         |  vazio  |
|   ID  | principal | inteiro |  0  |    0     |    0     |   global  |  N   |   8   |   S    |                      |                      |  vazio  |
|   ID  |     a     | inteiro |  0  |    0     |    0     | principal |  N   |   9   |   N    |         None         |                      |  vazio  |
|   ID  |     a     |   None  |  0  |    0     |    0     | principal |  S   |   10  |   N    |         None         |                      |  vazio  |
|   ID  |    func   |   None  |  0  |    0     |    0     | principal |  N   |   10  |   N    |         None         |         None         |  vazio  |
|   ID  |    func   |   None  |  0  |    0     |    0     | principal |  S   |   10  |   S    |         |10          |         |10          |  vazio  |

A Tabela de Simbolos contem de acordo com a necessidade de elementos nas colunas. A coluna 'Token' representa o token da variavel ou funcao que faz parte da tabela de simbolos, a coluna 'Lexema' contem o nome das variaveis declaradas ou utilizadas, assim como o nome das funcoes declaradas ou chamada, a coluna 'Tipo' contem o tipo das variaveis ou funcoes declaradas, a colunas 'dim' contera '0' caso seja , e caso ela contenha mais de uma dimensao, os valores dessas dimensoes nas colunas'tam-diml' que representa o tamanho da primeira dimensao e 'tam-dim2', a qual representa o tamanho da segunda dimensao.'init' representa se uma funcao ou variavel foi declarada ou nao, dizendo na coluna 'linha' em que linha do codigo esta. A coluna funcao permite saber se é declarado em que funcao. Os parametros são oque passa pela funcao tanto na hora de criar quanto na hora de ler.O valor é oque foi atribuido para a variavel. E por utimo o retorno permite saber se a funcao retorna algum valor.


## 3 Regras Semânticas
Para que seja possivel criar a Arvore Sintatica Abstrata, e necessario tem um maior conhecimento sobre as regras semanticas aplicada a linguagem. Neste caso a regra semantica foi oferecida pelo professor no documento de especificacao do desenvolvimento desta analise, podendo entao ser observada a seguir.



- Aviso: Variável 'func' não declarada
- Erro: Função 'principal' deveria retornar 'inteiro', mas retorna vazio
- Erro: Chamada a função 'func' que não foi declarada

## 3.1 Procedimentos
- Verificacao se existe uma funcao principal no codigo que serve como funcao de inicializacao
- Verificar se o tipo retornado da funcao principal e o mesmo do tipo da funcao principal
- Verificar se a quantidade de parametros de uma chamada de funcao e igual a quantidade de parametros formais de sua definicao
- Verificar para todas as funcoes se o tipo do valor retornado e compativel com o tipo de retorno declarado
- Verificar se as funcoes sao declaradas antes de ser chamadas
- Uma funcao qualquer nao pode chamar a funcao principal
- É possivel declarar uma funcao e nao utiliza la

## 4 Poda arvore
Nessa parte realiza a poda da arvore que permite deixar as principais operações que ocorre na arvore sendo as atribuicoes realizadas no codigo os nós são separados para aqueles que serão cortados e os que serão mantidos sendo os matidos 'retorna', 'corpo', 'cabecalho', 'atribuicao', 'chamada_funcao', 'declaracao_variaveis' e os que seão apagados 'ID', 'var', 'dois_pontos', 'tipo', 'leia', 'escreva','se', 'repita', 'até', 'INTEIRO',  'NUM_INTEIRO', 'declaracao', 'indice', 'lista_declaracoes', 'numero', 'fator','abre_colchete', 'fecha_colchete', 'menos', 'menor_igual', 'maior_igual','expressao', 'expressao_logica',  'ABRE_PARENTESE', 'FECHA_PARENTESE', 'MAIS', 'MENOS','expressao_simples', 'expressao_multiplicativa', 'vazio','fim', 'expressao_unaria', 'inicializacao_variaveis', 'ATRIBUICAO','NUM_NOTACAO_CIENTIFICA', 'LEIA', 'abre_parentese', 'fecha_parentese', 'fator', 'FIM','operador_soma', 'expressao_aditiva', 'mais', 'lista_argumentos', 'VIRGULA','virgula', 'lista_parametros', ',', 'FLUTUANTE', 'NUM_PONTO_FLUTUANTE', 'RETORNA', 'ESCREVA', 'SE', 'ENTAO', 'SENAO', 'maior','menor', 'REPITA', 'operador_logico', 'lista_variaveis','acao', 'operador_multiplicacao', 'vezes','id', 'operador_relacional', 'MAIOR', sendo esses os tokens utilizados no codigo.
                    

## 5 Referencias

https://anytree.readthedocs.io/en/latest/

