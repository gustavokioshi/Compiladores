import tppparser
import sys
from prettytable import PrettyTable
from sys import argv
from anytree import RenderTree, AsciiStyle
from anytree.exporter import UniqueDotExporter

global flag
flag = 0
tam_dim1 = 0
dim = 0
global parametro
parametro = ''
global token_list
red = ""
class Token():
    def __init__(self):
        self.list = []
        
    def add(self,token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor, retorno):
        self.list.append([token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor, retorno])
        return self.list

token_list = Token()

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
    red = "N"
    if "chamada_funcao" in tree.label:
        return "S"
    for filho in tree.children:
        if "cabecalho" in filho.label:
            return "S"
        if "expressao" in filho.label:
            return "N"
        if red == "N":
            red = find_funcao(filho)
    return red
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
def allleaf(tree):
    global red
    for filho in tree.children:
        if filho.label == "ID":
            red = red + filho.children[0].label
        allleaf(filho)
    return red

def find_valor(tree):
    global red
    for filho in tree.children:
        if "expressao:" in filho.label:
            red = red + allleaf(filho)
    return parametro
def find_retorno(tree):
    red = "vazio"
    for filho in tree.children:
        if "retorna" in filho.label:
            return "S"
        if red == "vazio":
            red = find_retorno(filho)
    return red
def find_ID(tree,escopo,linha):
    global token_list
    for filho in tree.children:
        if filho.label == "ID":
            Table.add_row([filho.label,filho.children[0].label,None,0,0,0,escopo,"N",linha,"N", None, None, "vazio"])
            token_list.add(filho.label,filho.children[0].label,None,0,0,0,escopo,"N",linha,"N", None, None, "vazio")
        find_ID(filho,escopo,linha)
def monta_tabela_simbolos(tree):
    global flag
    global dim
    global tam_dim1
    global parametro
    global token_list
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
            retorno = find_retorno(filho)
            Table.add_row([token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor, retorno])
            token_list.add(token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor, retorno)
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
            retorno = find_retorno(filho)
            Table.add_row([token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor, retorno])
            token_list.add(token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor, retorno)
            if ("atribuicao" in filho.label):
                for filhoi in filho.children:
                    if filhoi.label == "expressao":
                        find_ID(filhoi,escopo,linha)



            
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
            retorno = find_retorno(filho)
            Table.add_row([token,lexema,tipo,dim,tam_dim1,tam_dim2, escopo, init, linha,funcao, parametros, valor, retorno])
            token_list.add(token,lexema,tipo,dim,tam_dim1,tam_dim2,escopo,init,linha,funcao, parametros, valor, retorno)
        if ("retorna:" in filho.label):
            escopo = find_escopo(filho)
            linha = find_linha(filho)
            for filhoi in filho.children:
                if filhoi.label == "expressao":
                    find_ID(filhoi,escopo,linha)
        dim = 0
        tam_dim1 = 0
        parametro = ""
        monta_tabela_simbolos(filho)




def declaracao_funcao_principal():
    flag = 0
    global token_list
    for token in token_list.list:
        if token[1] == "principal":
            flag = 1
            if token[2] == None:
                flag = 2
                break
    if flag == 0:
        print("Erro: Função principal não declarada")
    if flag == 2:
        print("Erro: Chamada para a função principal não permitida")

def erro_de_array():
    global token_list
    for token in token_list.list:
        if '0' != token[3]:
            if '.' in str(token[4]):
                if None == token[2]:
                    print("Erro: índice de array '"+ token[1] +"' não inteiro")


def funcao_nao_inicializada():
    global token_list
    for token_a in token_list.list:
        repete_token = 0
        flag = 0
        for token_b in token_list.list:
            if token_b[1] != "principal":
                if token_a[1] == token_b[1] :
                    repete_token = repete_token + 1
                    if (token_b[7] == "N") and (token_b[2] != None):
                        flag = 1
                    if (token_b[7] == "S") and (flag == 1):
                        flag = 0
                    if (token_b[2] != None) and (token_a[2] != None):
                        temp = int(token_b[8]) - int(token_a[8])
                        if temp <0:
                            flag =2
                            break
                if token_b[1] == token_a[6] :
                    flag = 0
                if (token_a[8] == token_b[8]) and (token_a[7] == "N") and (token_b[7] == "S"):
                    valida1 = "asd"
                    valida2 = "ewq"
                    for token_c in token_list.list:
                        if token_c[1] == token_a[1]:
                            valida1 = token_c[2]
                        if token_c[1] == token_b[1]:
                            valida2 = token_c[2]
                    if (valida1 == valida2):
                        flag = 3
                        break

                    
        if flag == 1:
            print("Aviso: Variável '"+ token_a[1] +"' declarada e não utilizada")
        elif flag == 2:
            print("Aviso: Variável '"+ token_a[1] +"' já declarada anteriormente")
        elif repete_token == 1:
            print("Aviso: Variável '"+ token_a[1] +"' não declarada")
        elif flag == 3:
            print("Aviso: Coerção implícita do valor de '"+ token_a[1] +"'")

def retorna():
    global token_list
    for token in token_list.list:
        if token[9] == "S":
            if token[2] == None:
                print("Erro: Chamada a função '"+token[1]+"' que não foi declarada")
            elif token[12] == "vazio":
                print("Erro: Função '"+ token[1]+"' deveria retornar '"+str(token[2])+"', mas retorna "+token[12])            

def verifica_regras_semanticas():
    declaracao_funcao_principal()
    erro_de_array()
    funcao_nao_inicializada()
    retorna()

def retira_no(no_remove):
    global remover_nos
    global verificar_nos
    aux_tree = []
    no_pai = no_remove.parent

    if no_remove.label in remover_nos:
        for filho in range(len(no_pai.children)):
            if no_pai.children[filho].label ==  no_remove.label:
                aux_tree += no_remove.children
            else:
                aux_tree.append(no_pai.children[filho])
        no_pai.children = aux_tree

    if (no_remove.label in verificar_nos):
        for filho in range(len(no_pai.children)):
            if no_pai.children[filho].label ==  no_remove.label:
                aux_tree += no_remove.children
            else:
                aux_tree.append(no_pai.children[filho])
        no_pai.children = aux_tree
        
def poda_arvore(tree):
    for filho in tree.children:
        poda_arvore(filho)
    retira_no(tree)

def main():
    global remover_nos
    global verificar_nos
    global Table
    tree = tppparser.main()
    Table = PrettyTable( ['Token', 'Lexema', 'Tipo', 'dim', 'tam_dim1', 'tam_dim2', 'escopo', 'init', 'linha','funcao', 'parametros', 'valor', 'retorno'])
    
    monta_tabela_simbolos(tree)
    print(Table)
    # verifica_regras_semanticas()

    # Nós que serao mantidos
    verificar_nos = ['retorna', 'corpo', 'cabecalho', 'atribuicao', 'chamada_funcao', 'declaracao_variaveis']

    # Nós que serão removidos na poda
    remover_nos = ['ID', 'var', 'dois_pontos', 'tipo', 'leia', 'escreva','se', 'repita', 'até',
                    'INTEIRO',  'NUM_INTEIRO', 'declaracao', 'indice', 'lista_declaracoes',
                    'numero', 'fator','abre_colchete', 'fecha_colchete', 'menos', 'menor_igual',
                    'maior_igual','expressao', 'expressao_logica',  'ABRE_PARENTESE', 'FECHA_PARENTESE', 
                    'MAIS', 'MENOS','expressao_simples', 'expressao_multiplicativa', 'vazio','fim',
                    'expressao_unaria', 'inicializacao_variaveis', 'ATRIBUICAO','NUM_NOTACAO_CIENTIFICA', 'LEIA', 
                    'abre_parentese', 'fecha_parentese', 'fator', 'FIM','operador_soma', 'expressao_aditiva',
                    'mais', 'lista_argumentos', 'VIRGULA','virgula', 'lista_parametros', ',',
                     'FLUTUANTE', 'NUM_PONTO_FLUTUANTE', 'RETORNA', 'ESCREVA', 'SE', 'ENTAO', 'SENAO',
                    'maior','menor', 'REPITA', 'operador_logico', 'lista_variaveis','acao',
                    'operador_multiplicacao', 'vezes','id', 'operador_relacional', 'MAIOR',')','(',':',':=']

    poda_arvore(tree)
    print()

    UniqueDotExporter(tree).to_picture(f"{sys.argv[1]}.prunned.unique.ast.png")
    print(f"Árvore Sintática Abstrata foi gerada. \nArquivo de Saída: {sys.argv[1]}.prunned.unique.ast.png")
    return tree

if __name__ == "__main__":
    main()
