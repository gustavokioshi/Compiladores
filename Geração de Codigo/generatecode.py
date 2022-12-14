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

_escrevaI = ir.FunctionType(ir.VoidType(), [ir.IntType(32)])
escrevaI = ir.Function(Module, _escrevaI, "escrevaInteiro")

_escrevaF = ir.FunctionType(ir.VoidType(), [ir.FloatType()])
escrevaF = ir.Function(Module, _escrevaF, "escrevaFlutuante")

_leiaI = ir.FunctionType(ir.IntType(32), [])
leiaI = ir.Function(Module, _leiaI, "leiaInteiro")

_leiaF = ir.FunctionType(ir.FloatType(), [])
leiaF = ir.Function(Module, _leiaF, "leiaFlutuante")


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
    global escrevaI
    global escrevaF
    global leiaI
    global leiaF
    if ("declaracao_funcao" in tree.label):
        func = (tree.children[1].label)
        print(func)
        #tem parametro
        if tree.children[1].label == 'soma':
            # Cria o cabeçalho da função soma
            t_soma = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
            soma = ir.Function(Module, t_soma, 'soma')
            soma.args[0].name = 'a'
            soma.args[1].name = 'b'
        # Define o retorno da função main
        Zero32 = ir.Constant(ir.IntType(32), 0)
        # Cria função main
        t_func_main = ir.FunctionType(ir.IntType(32), ())
        # Declara função main
        if tree.children[1].label == 'principal':
            main = ir.Function(Module, t_func_main, name = 'main' )
        else:
            main = ir.Function(Module, t_func_main, name = tree.children[1].label )
        # Declara os blocos de entrada e saída da função.
        entryBlock = main.append_basic_block(tree.children[1].label+':entry')

        # Adiciona o bloco de entrada.
        builder = ir.IRBuilder(entryBlock)

        # Cria o valor de retorno e inicializa com zero
        returnVal = builder.alloca(ir.IntType(32))
        builder.store(Zero32, returnVal)
        
        for filho in tree.children:
            geração_de_codigo(filho)
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
        print(val)
        # atribuicao de um unico valor
        if len(tree.children) == 2:
            # tipo numero x=1
            if (tree.children[1].type == "VALOR"):
                for i in range(len(val)):
                    if val[i]== tree.children[0].label:
                        builder.store(ir.Constant(ir.IntType(32), int(tree.children[1].label) ), val_ende[i])
            # tipo letra x=y
            if (tree.children[1].type == "ID"):
                for i in range(len(val)):
                    if val[i] == tree.children[1].label:
                        temp_a = builder.load(val_ende[i])
                for i in range(len(val)):
                    if val[i] == tree.children[0].label:
                        builder.store(temp_a, val_ende[i])
        # atribuicao com alguma operacao
        elif len(tree.children) == 4:
            #x = 1 + _
            if (tree.children[1].type == "VALOR"):
                x_temp = ir.Constant(ir.IntType(32), int(tree.children[1].label))
            #x = y + _
            if (tree.children[1].type == "ID"):
                for i in range(len(val)):
                    if val[i]== tree.children[1].label:
                        x_temp = builder.load(val_ende[i])
            #x = _ + 1
            if (tree.children[3].type == "VALOR"):
                y_temp = ir.Constant(ir.IntType(32), int(tree.children[3].label))
            #x = _ + y
            if (tree.children[3].type == "ID"):
                for i in range(len(val)):
                    if val[i]== tree.children[3].label:
                        y_temp = builder.load(val_ende[i])
            for i in range(len(val)):
                if val[i]== tree.children[0].label:
                    r_temp = val_ende[i]
            # operacoes 
            if tree.children[2].label == '+':
                a_temp = builder.add(x_temp, y_temp)
            elif tree.children[2].label == '-':
                a_temp = builder.sub(x_temp, y_temp)
            elif tree.children[2].label == '*':
                a_temp = builder.mul(x_temp, y_temp)
            elif tree.children[2].label == '/':      
                a_temp = builder.sdiv(x_temp, y_temp)

            builder.store(a_temp ,r_temp )
            
        print("atribuicao")
        
    elif ("cabecalho" in tree.label):
        print("cabecalho")



    elif ("se" in tree.label):
        print("se")
        iftrue_1 = main.append_basic_block('iftrue_1')
        iffalse_1 = main.append_basic_block('iffalse_1')
        ifend_1 = main.append_basic_block('ifend_1')

        # Carrega as variáveis a e b para comparação.
        print(val_ende)
        for i in range(len(val)):
            if val[i]== tree.children[1].label:
                temp_a = val_ende[i]
                a_cmp = builder.load(temp_a, align=4)
        for i in range(len(val)):
            if val[i]== tree.children[3].label:
                temp_c = tree.children[3].label
                c_cmp = builder.load(temp_c, align=4)
                break
            else:
                c_cmp = ir.Constant(ir.IntType(32), int(tree.children[3].label))


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
        if (tree.children[5].type == "VALOR"):
            comperValue = ir.Constant(ir.IntType(32), int(tree.children[5].label)) 
        elif (tree.children[5].type == "ID"):
            comperValue = builder.load (tree.children[5].label)
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
        # Invoca a função 'escrevaI', carregando o valor da variável 'a'
        # e o passando como argumento
        for i in range(len(val)):
            if val[i] == tree.children[1].label:
                builder.call(escrevaI, args=[builder.load(val_ende[i])])
        print("escreva")
    elif ("leia" in tree.label):
        # Invoca a função 'leiaI', carregando o valor da variável 'a'
        # Aloca variável 'a'
        for i in range(len(val)):
            if val[i] == tree.children[1].label:
                builder.load(val_ende[i], align=4)
                break
        # Invoca a função 'leiaI' e salva o resultado no ponteiro
        # que representa a variável 'a'
        resultado_leia = builder.call(leiaI, args=[])
        builder.store(resultado_leia, val_ende[i], align=4)
        print("leia")
    elif ("retorna" in tree.label):
        # Cria um salto para o bloco de saída

        exitBasicBlock = main.append_basic_block('exit')
        builder.branch(exitBasicBlock)

        # Adiciona o bloco de saida
        builder.position_at_end(exitBasicBlock)
        
        # variavel de retorno para letra
        flag = 0
        if len(tree.children) == 2:
            for i in range(len(val)):
                if val[i] == tree.children[1].label:
                    builder.ret(builder.load(val_ende[i]))
                    flag = 1
            if flag == 0:
                builder.ret(ir.Constant(ir.IntType(32), int(tree.children[1].label)))
        elif len(tree.children) == 4:
            #x = 1 + _
            if (tree.children[1].type == "VALOR"):
                x_temp = ir.Constant(ir.IntType(32), int(tree.children[1].label))
            #x = y + _
            if (tree.children[1].type == "ID"):
                for i in range(len(val)):
                    if val[i]== tree.children[1].label:
                        x_temp = builder.load(val_ende[i])
            #x = _ + 1
            if (tree.children[3].type == "VALOR"):
                y_temp = ir.Constant(ir.IntType(32), int(tree.children[3].label))
            #x = _ + y
            if (tree.children[3].type == "ID"):
                for i in range(len(val)):
                    if val[i]== tree.children[3].label:
                        y_temp = builder.load(val_ende[i])
            # operacoes 
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
        func= None
        print("retorna")

    else:
        for filho in tree.children:
            geração_de_codigo(filho)
def main():
    tree = tppsemantic2.main()    
    print()

    # UniqueDotExporter(tree).to_picture(f"{sys.argv[1]}.prunned.unique.ast.png")
    # print(f"Árvore Sintática Abstrata foi gerada. \nArquivo de Saída: {sys.argv[1]}.prunned.unique.ast.png")
    # llvm-link vars.ll io.ll -o vars-liked.ll 
    # clang vars-liked.ll -o vars.exe
    # ./vars.exe 
    # echo $?
    geração_de_codigo(tree)
    arquivo = open('vars.ll', 'w')
    arquivo.write(str(Module))
    arquivo.close()
    print(Module)


if __name__ == "__main__":
    main()
