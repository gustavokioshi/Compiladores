import tppparser
import sys
from prettytable import PrettyTable
from sys import argv
from anytree import RenderTree, AsciiStyle
from anytree.exporter import UniqueDotExporter

global flag
flag = 0
global parametro
parametro = ''
def find_token(tree):
    global flag
    token = None
    for filho in tree.children:
        if flag == 1:
            break
        elif "ID" == filho.label:
            flag =1
            return filho.label
        elif "id" == filho.label:
            flag =1
            return filho.label
        else:
            token = find_token(filho)
    return token

def find_lexema(tree):
    global flag
    lexema =''
    for filho in tree.children:
        if flag == 1:
            break
        elif "ID" == filho.label:
            flag = 1
            return filho.children[0].label
        else:
            lexema = find_lexema(filho)
    return lexema

def find_tipo(tree):
    global flag 
    for filho in tree.children:
        if "tipo" == filho.label:
            return filho.children[0].children[0].label
        else:
            return find_tipo(filho)
dim = 0
def find_dim(tree,count):
    global dim
    for filho in tree.children:
        if "corpo" == filho.label:
            break
        elif "indice" == filho.label:
            count = count + 1
            return count
        dim = find_dim(filho,count)
    return dim
tam_dim1 = 0
def find_tam_dim1(tree):
    global tam_dim1
    for filho in tree.children:
        if "corpo" == filho.label:
            break
        elif "indice" == filho.label:
            return filho.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
        tam_dim1 = find_tam_dim1(filho)
    return tam_dim1

# def find_tam_dim2(tree)
def find_escopo(tree):
    if tree.parent == None:
        return "global"
    if "cabecalho" == tree.label:
        return tree.children[0].children[0].label
    return find_escopo(tree.parent)

def find_init(tree):
    if "declaracao_funcao" in tree.label:
        return "N"
    elif "declaracao_variaveis" in tree.label:
        return "N"
    elif "parametro" in tree.label:
        return "N"
    elif "atribuicao" in tree.label:
        return "S"
    elif "chamada_funcao" in tree.label:
        return "S"

def find_linha(tree):
    flag = 0
    linha =''
    for i in tree.label:
        if(i==":"):
            flag = 1
        elif(flag == 1):
            linha =linha+i
    return linha

def find_funcao(tree):
    for filho in tree.children:
        if "declaracao_funcao" in filho.label:
            return filho.children[1].children[0].children[0].label

def find_parametros(tree):
    global parametro
    for filho in tree.children:
        if "parametro:" in filho.label:
            parametro = parametro +"|"+find_tipo(filho)+"="+filho.children[2].children[0].label
            return parametro
        elif "numero" in filho.label:
            parametro = parametro +"|"+ filho.children[0].children[0].label
            return parametro
        elif "corpo" in filho.label:
            return parametro
        find_parametros(filho)
    return parametro
            
def find_valor(tree):
    # if "atribuicao" in tree.label:
        # for 
    return "fix"
def monta_tabela_simbolos(tree):
    global flag
    global dim
    global tam_dim1
    global parametro
    for filho in tree.children:
        if ("declaracao_funcao" in filho.label) or ("chamada_funcao" in filho.label):
            flag = 0
            token = find_token(filho)
            init = find_init(filho)
            escopo = find_escopo(filho)
            flag = 0
            lexema = find_lexema(filho)
            tipo = find_tipo(filho)
            dim = find_dim(filho,0)
            tam_dim1 = find_tam_dim1(filho)
            tam_dim2 = "0"
            linha = find_linha(filho)
            funcao =find_funcao(filho)
            parametros = find_parametros(filho)
            valor = find_valor(filho)
            Table.add_row([token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor])
        elif ("atribuicao" in filho.label) or ("declaracao_variaveis" in filho.label):
            flag = 0
            token = find_token(filho)
            init = find_init(filho)
            escopo = find_escopo(filho)
            flag = 0
            lexema = find_lexema(filho)
            tipo = find_tipo(filho)
            dim = find_dim(filho,0)
            tam_dim1 = find_tam_dim1(filho)
            tam_dim2 = "0"
            linha = find_linha(filho)
            funcao =find_funcao(filho)
            parametros = None
            valor = find_valor(filho)
            Table.add_row([token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor])
        elif "parametro:" in filho.label:
            flag = 0
            token = find_token(filho)
            init = find_init(filho)
            escopo = find_escopo(filho)
            flag = 0
            lexema = filho.children[2].children[0].label
            tipo = find_tipo(filho)
            dim = find_dim(filho,0)
            tam_dim1 = find_tam_dim1(filho)
            tam_dim2 = "0"
            linha = find_linha(filho)
            funcao =find_funcao(filho)
            parametros = None
            valor = find_valor(filho)
            Table.add_row([token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor])
        dim = 0
        tam_dim1 = 0
        parametro = ""
        monta_tabela_simbolos(filho)

def main():
    tree = tppparser.main()
    global Table
    Table = PrettyTable( ['Token', 'Lexema', 'Tipo', 'dim', 'tam_dim1', 'tam_dim2', 'escopo', 'init', 'linha','funcao', 'parametros', 'valor'])
    # print(RenderTree(tree, style=AsciiStyle()).by_attr())
    # findall(tree, filter_=lambda node: node.name in ("a"))
    
    monta_tabela_simbolos(tree)
    print(Table)
    # verifica_regras_semanticas(Table)

    # Nós que tem o valor de linhas nos nomes
    verificar_nos = ['retorna', 'corpo', 'leia', 'escreva', 'se', 'repita', 'até']

    # Nós que serão retirados na poda
    remover_nos = ['ID', 'var', 'lista_variaveis', 'dois_pontos', 'tipo',
                    'INTEIRO',  'NUM_INTEIRO','lista_declaracoes', 'declaracao', 'indice',
                    'numero', 'fator','abre_colchete', 'fecha_colchete', 'menos', 'menor_igual',
                    'maior_igual','expressao', 'expressao_logica',  'ABRE_PARENTESE', 'FECHA_PARENTESE', 
                    'MAIS', 'chamada_funcao', 'MENOS','expressao_simples', 'expressao_aditiva', 'expressao_multiplicativa',
                    'expressao_unaria', 'inicializacao_variaveis', 'ATRIBUICAO','NUM_NOTACAO_CIENTIFICA', 'LEIA', 
                    'abre_parentese', 'fecha_parentese', 'atribuicao', 'fator', 'cabecalho', 'FIM','operador_soma',
                    'mais', 'chamada_funcao', 'lista_argumentos', 'VIRGULA','virgula', 'lista_parametros', 'vazio',
                    '(', ')', ':', ',', 'FLUTUANTE', 'NUM_PONTO_FLUTUANTE', 'RETORNA', 'ESCREVA', 'SE', 'ENTAO', 'SENAO',
                    'maior','menor', 'REPITA', 'igual', 'menos', 'menor_igual', 'maior_igual', 'operador_logico',
                    'operador_multiplicacao', 'vezes','id', 'declaracao_variaveis', 'atribuicao', 'operador_relacional', 'MAIOR']

    # Verificar retorno (nenhum filho)
    # print()

    # Gera imagem da árvore podada
    UniqueDotExporter(tree).to_picture(f"{sys.argv[1]}.prunned.unique.ast.png")
    print(f"Árvore Sintática Abstrata foi gerada. \nArquivo de Saída: {sys.argv[1]}.prunned.unique.ast.png")


if __name__ == "__main__":
    main()
