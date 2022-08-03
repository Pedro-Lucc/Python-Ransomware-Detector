# IMPORTS
from os import name, system


# FUNÇÕES PARA AUXILIAR
# Função para limpar a tela
def clearScreen():
    # Windows NT
    if name == "nt":
        system("cls")
    # Mac/Linux
    else:
        system("clear")
