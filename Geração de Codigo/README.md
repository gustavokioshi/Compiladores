# Projeto de Implementação de um Compilador para a Linguagem TPP: Geração de Codigo (Trabalho – 4ª parte)
#### Gustavo Kioshi Asato
#### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)

## 1 Geração de Codigo
Nessa atividade, discutiremos uma implementação de geração de código. A geração de código é uma técnica utilizada por desenvolvedores para automatizar a criação de código fonte de programas de computador a partir de uma especificação ou de um modelo de alto nível. Isso pode ajudar a economizar tempo e esforço, além de garantir a consistência e a qualidade do código gerado. A implementação de geração de código é baseada em regras de transformação que são aplicadas a um modelo de alto nível, produzindo código fonte em uma linguagem de programação específica. Além disso, a nossa implementação inclui recursos para testar e validar o código gerado, garantindo sua correção e funcionalidade.

### 2 Especificação da Linguagem T++
Com base na arvore gerada no tppparse.py ela é podada de forma que possua somente a parte mais importante das ações realizadas no codigo. Sendo percorrida da direita para a esquerda 
![image](geracao-codigo-testes/gencode-017.tpp.prunned.unique.ast.png)

~~~TPP
inteiro principal()	
	inteiro: x
	flutuante: y
	
	x := 0
	y := 0.0
	
	leia(x)
	leia(y)
	escreva(x)
	escreva(y)
	
    retorna(0)
fim
~~~


~~~TPP
; ModuleID = "modulo.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

define i32 @"main"()
{
"principal:entry":
  %".2" = alloca i32
  store i32 0, i32* %".2"
  %"x" = alloca i32, align 4
  store i32 0, i32* %"x"
  %"y" = alloca i32, align 4
  store i32 0, i32* %"y"
  store i32 0, i32* %"x"
  store i32 0, i32* %"y"
  %".8" = load i32, i32* %"x", align 4
  %".9" = call i32 @"leiaInteiro"()
  store i32 %".9", i32* %"x", align 4
  %".11" = load i32, i32* %"y", align 4
  %".12" = call i32 @"leiaInteiro"()
  store i32 %".12", i32* %"y", align 4
  %".14" = load i32, i32* %"x"
  call void @"escrevaInteiro"(i32 %".14")
  %".16" = load i32, i32* %"y"
  call void @"escrevaInteiro"(i32 %".16")
  br label %"exit"
exit:
  ret i32 0
}
~~~

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

![image](semantica-testes/sema-005.tpp.prunned.unique.ast.png)
                    
antes da poda
![image](semantica-testes/sema-005.tpp.unique.ast.png)
## 5 Referencias

https://anytree.readthedocs.io/en/latest/

