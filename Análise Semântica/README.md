# Projeto de Implementação de um Compilador para a Linguagem TPP: Análise Semantica (Trabalho – 3ª parte)
#### Gustavo Kioshi Asato
#### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)
## 1 Análise Semantica
Nessa atividade desenvolvida durante a disciplina de Compiladores tem em foco desenvolver um analisador semantico que funcina como um sistema de varedura no codigo a ser compilado, separando os tokens. Os tokens são definidos no compilador sendo palavras reservadas ou símbolos dispinilizados em formato de arvore pelo analise sintatica. Cada token pode receber os proximos caracteres de acordo com a sua implementação de forma com que cada token possa ter uma entrada necessaria para retornar para oque foi designada.

### 2 Tabela de Simbolos
Durante a analise Semantica ha dois objetivos que devem ser completados, sendo eles a construcao da tabela de simbolos, e a identificacao de erros e avisos, assim como os erros e avisos esperados no conjunto de testes especificamente para analise semantica, e por fim, podar a arvore Sintatica, o que resultara em uma arvore sintatica abstrata. A criacao da tabela de simbolos neste caso for felta durante a propria analise Semantica, mais especificamente, antes de verificar as regras semanticas, ja que ela sera utilizada para realizar este passo. A tabela gerada ao fim e semelhante a tabela abaixo.


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

E possivel perceber que a Tabela de Simbolos contem de acordo com a necessidade de elementos nas colunas, e agora veremos o que cada uma delas significa. A coluna 'Token' representa o token da variavel ou funcao que faz parte da tabela de simbolos, a coluna 'Lexema' contem o nome das variaveis declaradas ou utilizadas, assim como o nome das funcoes declaradas ou chamada, a coluna 'Tipo' contem o tipo das variaveis ou funcoes declaradas, a colunas 'dim' contera '0' caso seja , e caso ela contenha mais de uma dimensao, os valores dessas dimensoes serao armazenadas nas colunas'tam-diml' que representa o tamanho da primeira dimensao e 'tam-dim2', a qual representa o tamanho da segunda dimensao. Ja a coluna 'init' representa se uma funcao ou variavel foi declarada ou nao, dizendo na coluna 'linha' onde ela foi encontrada. Por fim podemos observar as colunas adicionada principalmente para armazenar alguns dados das funcoes, sendo elas 'funcao' que indica se o lexema identificado e uma funcao ou nao, e caso seja, na coluna e armazena os parametros passados. Para encerrar temos a coluna valor , que como o proprio nome diz, guarda os valores e tipos das atribuicoes feitas.


## 3 Regras Semânticas
Para que seja possivel criar a Arvore Sintatica Abstrata, e necessario tem um maior conhecimento sobre as regras semanticas aplicada a linguagem. Neste caso a regra semantica foi oferecida pelo professor no documento de especificacao do desenvolvimento desta analise, podendo entao ser observada a seguir.


![alt text](fatorial1.png)
## 3.1 Funcoes e Procedimentos
- Verificacao se existe uma funcao principal no codigo que serve como funcao de inicializacao
- Verificar se o tipo retornado da funcao principal e o mesmo do tipo da funcao principal
- Verificar se a quantidade de parametros de uma chamada de funcao e igual a quantidade de parametros formais de sua definicao
- Verificar para todas as funcoes se o tipo do valor retornado e compativel com o tipo de retorno declarado
- Verificar se as funcoes sao declaradas antes de ser chamadas
- Uma funcao qualquer nao pode chamar a funcao principal
- É possivel declarar uma funcao e nao utiliza la


![alt text](testes.png)
## 5 Referencias

https://anytree.readthedocs.io/en/latest/

