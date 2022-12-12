import tppsemantic2
import sys 
from sys import argv
from anytree import RenderTree, AsciiStyle
from anytree.exporter import UniqueDotExporter
from llvmlite import ir
from llvmlite import binding as llvm

# Código de Inicialização.
llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# Cria o módulo.
Module = ir.Module('modulo.bc')
Module.triple = llvm.get_process_triple()
target = llvm.Target.from_triple(Module.triple)
target_machine = target.create_target_machine()
Module.data_layout = target_machine.target_data


global func
global builder
global val
global val_ende
global main
val = []
val_ende = []
func = None
def geração_de_codigo(tree):
    global func
    global builder
    global Module
    global val
    global val_ende
    global exitBasicBlock
    global main
    if ("declaracao_funcao" in tree.label):
        func = tree.children[1].label
        print(func)
        # Define o retorno da função main
        Zero32 = ir.Constant(ir.IntType(32), 0)
        # Cria função main
        t_func_main = ir.FunctionType(ir.IntType(32), ())
        # Declara função main
        main = ir.Function(Module, t_func_main, name=tree.children[1].label)
        # Declara os blocos de entrada e saída da função.
        entryBlock = main.append_basic_block('entry')

        # Adiciona o bloco de entrada.
        builder = ir.IRBuilder(entryBlock)

        # Cria o valor de retorno e inicializa com zero
        returnVal = builder.alloca(ir.IntType(32), name='retorno')
        builder.store(Zero32, returnVal)
        
        for filho in tree.children:
            geração_de_codigo(filho)
        func = None
    elif ("chamada_funcao" in tree.label):
        print("chamada_funcao")
        
    elif ("declaracao_variaveis" in tree.label):
        print("declaracao_variaveis")
        
        if func == None:
            # Variável inteira global
            a = ir.GlobalVariable(Module, ir.IntType(32),tree.children[1].label)
            # Inicializa a variavel
            a.initializer = ir.Constant(ir.IntType(32), 0)
            # Linkage = common
            a.linkage = "common"
            # Define o alinhamento em 4
            a.align = 4
        else:
            # Variável inteira 
            # Aloca na memória variável a do tipo inteiro 
            a = builder.alloca(ir.IntType(32), name=tree.children[1].label)
            # Define o alinhamento
            a.align = 4
            # Cria uma constante pra armazenar o numero 0
            num1 = ir.Constant(ir.IntType(32),0)
            # Armazena o 0 na variavel 
            builder.store(num1, a)
        val.append(tree.children[1].label)
        val_ende.append(a)

    elif ("atribuicao" in tree.label):
        if len(tree.children) == 2:
            # tipo numero x=1
            if (tree.children[1].type == "VALOR"):
                for i in range(len(val)):
                    if val[i]== tree.children[0].label:
                        builder.store(ir.Constant(ir.IntType(32), int(tree.children[1].label) ), val_ende[i])
            # tipo letra x=y
            if (tree.children[1].type == "ID"):
                for i in range(len(val)):
                    if val[i]== tree.children[0].label:
                        temp_a = builder.load(val_ende[i])
                builder.store(temp_a, val_ende[i])
        elif len(tree.children) == 4:

            if (tree.children[1].type == "VALOR"):
                for i in range(len(val)):
                    if val[i]== tree.children[1].label:
                        x_temp = ir.Constant(ir.IntType(32), int(tree.children[1].label))
            # tipo letra x=y
            if (tree.children[1].type == "ID"):
                for i in range(len(val)):
                    if val[i]== tree.children[1].label:
                        x_temp = builder.load(val_ende[i])
            if (tree.children[3].type == "VALOR"):
                for i in range(len(val)):
                    if val[i]== tree.children[3].label:
                        y_temp = ir.Constant(ir.IntType(32), int(tree.children[3].label))
            # tipo letra x=y
            if (tree.children[3].type == "ID"):
                for i in range(len(val)):
                    if val[i]== tree.children[3].label:
                        y_temp = builder.load(val_ende[i])
            if tree.children[2].label == '+':
                builder.add(x_temp, y_temp)
            elif tree.children[2].label == '-':
                builder.sub(x_temp, y_temp)
            elif tree.children[2].label == '*':
                builder.mul(x_temp, y_temp)
            elif tree.children[2].label == '/':      
                builder.sdiv(x_temp, y_temp)
            elif tree.children[2].label == '%':
                builder.srem(x_temp, y_temp)
        print("atribuicao")
        
    elif ("cabecalho" in tree.label):
        print("cabecalho")

    elif ("se" in tree.label):
        print("se")
        # Declara os blocos básicos para o primeiro if.
        #	if(a < b) {
        #		c = 5; 
        #	}
        #	else {
        #		c = 6;
        #	}
        iftrue_1 = main.append_basic_block('iftrue_1')
        iffalse_1 = main.append_basic_block('iffalse_1')
        ifend_1 = main.append_basic_block('ifend_1')

        # Carrega as variáveis a e b para comparação.
        # IRBuilder.load(ptr, name='', align=None)
        for i in range(len(val)):
            if val[i]== tree.children[1].label:
                temp_a = val_ende[i]
                a_cmp = builder.load(temp_a, 'a_cmp', align=4)
            if val[i]== tree.children[3].label:
                temp_c = tree.children[3].label
                c_cmp = builder.load(temp_c, 'b_cmp', align=4)
            else:
                c_cmp = ir.Constant(ir.IntType(32), val_ende[i])


        #  IRBuilder.icmp_signed(cmpop, lhs, rhs, name='')
        print(tree.children[2].label, a_cmp, c_cmp)
        If_1 = builder.icmp_signed(tree.children[2].label, a_cmp, c_cmp)
        builder.cbranch(If_1, iftrue_1, iffalse_1)

        builder.position_at_end(iftrue_1)
        for filho in tree.children[5].children:
            geração_de_codigo(filho)
        builder.branch(ifend_1)

        builder.position_at_end(iffalse_1)
        for filho in tree.children[7].children:
            geração_de_codigo(filho)
        builder.branch(ifend_1)
        builder.position_at_end(ifend_1)

    elif ("repita" in tree.label):
        print("repita")
        loop = builder.append_basic_block('loop')
        loop_val = builder.append_basic_block('loop_val')
        loop_end = builder.append_basic_block('loop_end')

        # Pula para o laço do loop
        builder.branch(loop)

        # Posiciona no inicio do bloco do loop
        builder.position_at_end(loop)

        for filho in range(len(tree.children)):
            if filho == 0:
                filho = 0
            else:
                geração_de_codigo(tree.children[filho])

        # Pula para o laço de validação
        builder.branch(loop_val)

        # Posiciona no inicio do bloco de validação
        builder.position_at_end(loop_val)

        # Valor de comparação
        comperValue = ir.Constant(ir.IntType(32), int(tree.children[5].label)) 
        for i in range(len(val)):
            if val[i]== tree.children[3].label:
                temp_a = val_ende[i]
                a_cmp = builder.load(temp_a, 'a_cmp', align=4)
        # Gera a expressão de comparação

        # transformação para que alinguagem possa compreender o operador de comparação
        if tree.children[4].label == "=":
            operator = "=="
        sumExpression = builder.icmp_signed(operator, a_cmp, comperValue)

        # Compara se a expressão é verdadeira ou não, caso for pula para o bloco do loop end, caso contrário pula para o bloco do loop
        builder.cbranch(sumExpression, loop_end, loop)

        # Posiciona no inicio do bloco do fim do loop (saída do laço) e define o que o será executado após o fim (o resto do programa)  
        builder.position_at_end(loop_end)
    elif ("escreva" in tree.label):
        print("escreva")
    elif ("retorna" in tree.label):
        # Cria um salto para o bloco de saída

        exitBasicBlock = main.append_basic_block('exit')
        builder.branch(exitBasicBlock)

        # Adiciona o bloco de saida
        builder.position_at_end(exitBasicBlock)
        
        # variavel de retorno para letra
        flag = 0
        for i in range(len(val)):
            if val[i] == tree.children[1].label:
                builder.ret(builder.load(val_ende[i]))
                flag = 1
        if flag == 0:
            builder.ret(ir.Constant(ir.IntType(32), int(tree.children[1].label)))
        print("retorna")

    else:
        for filho in tree.children:
            geração_de_codigo(filho)
def main():
    tree = tppsemantic2.main()    
    print()

    # UniqueDotExporter(tree).to_picture(f"{sys.argv[1]}.prunned.unique.ast.png")
    # print(f"Árvore Sintática Abstrata foi gerada. \nArquivo de Saída: {sys.argv[1]}.prunned.unique.ast.png")


    geração_de_codigo(tree)
    arquivo = open('vars.ll', 'w')
    arquivo.write(str(Module))
    arquivo.close()
    print(Module)


if __name__ == "__main__":
    main()
