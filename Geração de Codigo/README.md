# Projeto de Implementação de um Compilador para a Linguagem TPP: Geração de Codigo (Trabalho – 4ª parte)
#### Gustavo Kioshi Asato
#### Ciencia da Computação – Universidade Tecnológica Federal do Paraná (UTFPR)

## 1 Geração de Codigo
Nessa atividade, discutiremos uma implementação de geração de código. A geração de código é uma técnica utilizada por desenvolvedores para automatizar a criação de código fonte de programas de computador a partir de uma especificação ou de um modelo de alto nível. Isso pode ajudar a economizar tempo e esforço, além de garantir a consistência e a qualidade do código gerado. A implementação de geração de código é baseada em regras de transformação que são aplicadas a um modelo de alto nível, produzindo código fonte em uma linguagem de programação específica. Além disso, a nossa implementação inclui recursos para testar e validar o código gerado, garantindo sua correção e funcionalidade.

### 2 Especificação da Linguagem T++
Com base na arvore gerada no tppparse.py ela é podada de forma que possua somente a parte mais importante das ações realizadas no codigo. Sendo percorrida da direita para a esquerda realizado no gerador_de_codigo.py verifica o nome da arvore e compara o nome para realizar se o nó é do mesmo tipo para realizar a tradução do codigo.
![image](geracao-codigo-testes/gencode-017.tpp.prunned.unique.ast.png)
Codigo a ser testado pelo compilador na parte de geração de codigo.
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

resultado a ser realizado pela maquina que esta utilizando para gerar o executavel sendo lido em codigo da maquina

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
quando rodar o executavel vai pedir dois valores para ser reproduzidos na tela

## 3 Procedimentos
Para rodar o codigo 
cria o codigo .ll
~~~
python3 generatecode.py geracao-codigo-testes/gencode-017.tpp
~~~

~~~
llvm-link vars.ll io.ll -o vars-liked.ll 
~~~
cria um executavel
~~~
clang vars-liked.ll -o vars.exe
~~~
roda o executavel
~~~
./vars.exe 
~~~
mostra o retorno da main
~~~
echo $?
~~~
## 4 llvmlite
llvmlite é uma biblioteca Python que fornece um meio para usar o compilador LLVM em Python. LLVM é uma ferramenta de compilação de código de baixo nível que é usada por muitas linguagens de programação, como C, C++ e Rust, para compilar código em um formato que pode ser facilmente executado pelo processador.

A biblioteca llvmlite fornece uma interface Python para o compilador LLVM que permite aos programadores Python acessar as ferramentas do LLVM de dentro de seus programas Python. Isso é útil para várias tarefas, como a geração dinâmica de código, a otimização de código existente e a geração de código para dispositivos como GPUs.

Para usar llvmlite em seu código Python, basta instalar a biblioteca usando o gerenciador de pacotes Python pip:

~~~
pip install llvmlite
~~~
## 5 Referencias

https://github.com/rogerioag/llvm-gencode-samples
https://pypi.org/project/llvmlite
https://llvmlite.readthedocs.io/en/latest

