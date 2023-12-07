import re

class Instrucao:
    def __init__(self, operacao, registrador, se_verdadeiro, se_falso):
        self.operacao = operacao
        self.registrador = self._converter_registrador(registrador)
        self.se_verdadeiro = int(se_verdadeiro)
        self.se_falso = int(se_falso)

    def _converter_registrador(self, reg):
        registro = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        return registro.get(reg, None)

def incrementar(valor):
    return valor + 1

def decrementar(valor):
    return max(0, valor - 1)

def zero(valor):
    return valor == 0

def interpretar_instrucao(linha):

    padrao_operacao = r'[A-Z]{3}'
    operacao = re.search(padrao_operacao, linha).group()

    padrao_registrador = r'[A-Z]{3}([A-Z])'
    registrador = re.search(padrao_registrador, linha).group(1)

    padrao_se_verdadeiro = r'[A-Z](\d+)(?=;|$)'
    se_verdadeiro = re.search(padrao_se_verdadeiro, linha).group(1)

    padrao_se_falso = r';(.*)'
    busca_se_falso = re.search(padrao_se_falso, linha)
    se_falso = busca_se_falso.group(1) if busca_se_falso else 0

    print(operacao, registrador, se_verdadeiro, se_falso)

    return Instrucao(operacao, registrador, se_verdadeiro, se_falso)

def executar_instrucao(instrucao, registradores):
    if instrucao.operacao == "ADD":
        registradores[instrucao.registrador] = incrementar(registradores[instrucao.registrador])
    elif instrucao.operacao == "SUB":
        registradores[instrucao.registrador] = decrementar(registradores[instrucao.registrador])
    elif instrucao.operacao == "ZER":
        if zero(registradores[instrucao.registrador]):
            return instrucao.se_verdadeiro
        return instrucao.se_falso
    return instrucao.se_verdadeiro

def executar_programa(opcao):
    arquivos = {1: 'soma.txt', 2: 'multiplicacao.txt', 3: 'fatorial.txt'}
    nome_arquivo = arquivos.get(opcao)

    valor_a = int(input('Defina o registrador A: '))
    valor_b = int(input('Defina o registrador B: ')) if opcao != 3 else 0
    registradores = [valor_a, valor_b, 0, 0]

    with open(nome_arquivo, 'r') as arquivo:
        instrucoes = arquivo.readlines()

    return instrucoes, registradores

def main():
    print("Bem-vindo ao simulador mqNorma!")
    print("Escolha um programa para executar:")
    opcoes = {1: "Soma", 2: "Multiplicação", 3: "Fatorial", 4: "Sair"}

    while True:
        for chave, valor in opcoes.items():
            print(f"{chave} - {valor}")
        escolha = input("Escolha: ")

        if not escolha.isdigit() or int(escolha) not in opcoes:
            print("Entrada inválida, tente novamente.")
            continue

        if int(escolha) == 4:
            break

        instrucoes, registradores = executar_programa(int(escolha))

        instrucao_atual = 1
        while instrucao_atual:
            inst = interpretar_instrucao(instrucoes[instrucao_atual - 1])
            instrucao_atual = executar_instrucao(inst, registradores)
            print(registradores)

        if int(escolha) == 1:
            print("\nResultado: ", registradores[2])
        elif int(escolha) == 2:
            print("\nResultado: ", registradores[0])
        elif int(escolha) == 3:
            print("\nResultado: ", registradores[3])

if __name__ == '__main__':
    main()
