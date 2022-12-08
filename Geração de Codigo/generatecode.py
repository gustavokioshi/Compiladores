import tppsemantic2
import sys 
from sys import argv
from anytree import RenderTree, AsciiStyle
from anytree.exporter import UniqueDotExporter
from llvmlite import ir
from llvmlite import binding as llvm

global func
global builder
global Module
func = None
def geração_de_codigo(tree):
    global func
    global builder
    global Module
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
        if func == None:
            # Variável inteira global
            global a
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

            c = builder.alloca(ir.IntType(32), name=tree.children[1].label)
            # Define o alinhamento
            c.align = 4
            # Cria uma constante pra armazenar o numero 0
            num1 = ir.Constant(ir.IntType(32),0)
            # Armazena o 0 na variavel 
            builder.store(num1, c)

    elif ("atribuicao" in tree.label):
        print(tree.children[1].type)
        if (tree.children[1].type == "VALOR"):
            builder.store(ir.Constant(ir.IntType(32), 2), a)
        if (tree.children[1].type == "ID"):
            a_temp = builder.load(a, "")
            builder.store(a_temp, b)
        # a_temp = builder.load(a, "")
        # b_temp = builder.load(b, "")
        # add_temp = builder.add(a_temp, b_temp, name='temp', flags=())
        # Armazena o temp (a + b) no c
        print("atribuicao")
    elif ("cabecalho" in tree.label):
        print("cabecalho")

    elif ("corpo" in tree.label):
        print("corpo")

    elif ("retorna" in tree.label):
        print("retorna")

    else:
        for filho in tree.children:
            geração_de_codigo(filho)
def main():
    global builder
    global Module
    tree = tppsemantic2.main()    
    print()

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

    geração_de_codigo(tree)
    arquivo = open('vars.ll', 'w')
    arquivo.write(str(Module))
    arquivo.close()
    print(Module)


if __name__ == "__main__":
    main()
