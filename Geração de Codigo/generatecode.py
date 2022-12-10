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
        exitBasicBlock = main.append_basic_block('exit')

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
        print(val_ende)
        if (tree.children[1].type == "VALOR"):
            for i in range(len(val)):
                if val[i]== tree.children[0].label:
                    builder.store(ir.Constant(ir.IntType(32), int(tree.children[1].label) ), val_ende[i])

        if (tree.children[1].type == "ID"):
            for i in range(len(val)):
                if val[i]== tree.children[0].label:
                    temp_a = builder.load(val_ende[i])
            builder.store(temp_a, val_ende[i])
        print("atribuicao")

    elif ("cabecalho" in tree.label):
        print("cabecalho")

    elif ("corpo" in tree.label):
        print("corpo")

    elif ("retorna" in tree.label):
        # Cria um salto para o bloco de saída
        builder.branch(exitBasicBlock)

        # Adiciona o bloco de saida
        builder.position_at_end(exitBasicBlock)
        
        for i in range(len(val)):
            if val[i]== tree.children[0].label:
                builder.ret(builder.load(val_ende[i], ""))
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
