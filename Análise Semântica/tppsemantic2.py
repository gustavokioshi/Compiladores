import tppparser
import sys
from prettytable import PrettyTable
from sys import argv
from anytree import RenderTree, AsciiStyle
from anytree.exporter import UniqueDotExporter

# def find_token(tree):
#     for filho in tree.children:
#         # print("log1:"+filho.label)
#         if "declaracao" == filho.label:
#             flag = 0
#             linha =''
#             print("linha:", end="")
#             for i in filho.children[0].label:
#                 if(i==":"):
#                     flag = 1
#                 elif(flag == 1):
#                     linha =linha+i
#                     print(i, end="")
#             print()
#             if "cabecalho" == filho.children[0].children[1].label:
#                 print("lexema:"+ filho.children[0].children[1].children[0].children[0].label)
#                 lexema = filho.children[0].children[1].children[0].children[0].label
#                 print("token:"+ filho.children[0].children[1].children[0].label)
#                 token = filho.children[0].children[1].children[0].label
#             else:
#                 print("lexema:"+ filho.children[0].children[2].children[0].children[0].children[0].label)
#                 lexema = filho.children[0].children[2].children[0].children[0].children[0].label
#                 print("token:"+ filho.children[0].children[2].children[0].children[0].label)
#                 token = filho.children[0].children[2].children[0].children[0].label
#             print("tipo:"+ filho.children[0].children[0].children[0].children[0].label)
#             tipo = filho.children[0].children[0].children[0].children[0].label
#             Table.add_row([token,lexema,tipo,"dim","tam_dim1","tam_dim2","global","N",linha])
#         if ("indice" == filho.label):
#             print("dim:1")
#             dim = 1
#             print("tam_dim1:"+ filho.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label)
#             tam_dim1 = filho.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
        
#         find_token(filho)
def find_token(tree):
    token =""
    for filho in tree.children:
        print("log-ID:" + filho.label)
        if "ID" == filho.label:
            print("log-ID")
            return filho.label
        token = find_token(filho)
    return token

def find_lexema(tree):
    lexema=''
    for filho in tree.children:
        if "ID" == filho.label:
            return filho.children[0].label
        lexema = find_lexema(filho)
    return lexema
def find_tipo(tree):
    for filho in tree.children:
        if "tipo" == filho.label:
            return filho.children[0].children[0].label
        return find_tipo(filho)
def find_dim(tree,count):
    dim = 0
    for filho in tree.children:
        if "indice" == filho.label:
            count = count + 1
            return count
        dim = find_dim(filho,count)
    return dim
def find_tam_dim1(tree):
    tam_dim1 = 0
    for filho in tree.children:
        if "indice" == filho.label:
            return filho.children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0].label
        tam_dim1 = find_tam_dim1(filho)
    return tam_dim1
# def find_tam_dim2(tree)
# def find_escopo(tree)
# def find_init(tree)
def find_linha(tree):
    flag = 0
    linha =''
    for i in tree.children[0].label:
        if(i==":"):
            flag = 1
        elif(flag == 1):
            linha =linha+i
    return linha

def monta_tabela_simbolos(tree):
    for filho in tree.children:
        if "declaracao" == filho.label:
            token = find_token(filho)
            init = "N"
            escopo = "global"
            lexema = find_lexema(filho)
            tipo = find_tipo(filho)
            dim = find_dim(filho,0)
            tam_dim1 = find_tam_dim1(filho)
            tam_dim2 = "0"
            linha = find_linha(filho)
            Table.add_row([token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha])
        if "ATRIBUICAO" == filho.label:
            token = find_token(filho.parent.parent)
            init = "S"
            escopo = filho.parent.parent.parent.parent.parent.children[0].children[0].label
            lexema = find_lexema(filho.parent)
            tipo = find_tipo(filho.parent.parent)
            dim = find_dim(filho.parent.parent,0)
            tam_dim1 = find_tam_dim1(filho.parent.parent)
            tam_dim2 = "0"
            linha = find_linha(filho.parent.parent)
            Table.add_row([token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha])
        monta_tabela_simbolos(filho)

def main():
    tree = tppparser.main()
    global Table
    Table = PrettyTable( ['Token', 'Lexema', 'Tipo', 'dim', 'tam_dim1', 'tam_dim2', 'escopo', 'init', 'linha'])
    print(RenderTree(tree, style=AsciiStyle()).by_attr())
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
