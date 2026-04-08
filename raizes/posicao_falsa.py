from pathlib import Path
from time import perf_counter
from typing import Callable
import numpy
from sympy import symbols, sympify, lambdify


def gerar_funcao(expressao: str) -> Callable[[float], float]:
    return lambdify(symbols('x'), sympify(expressao), modules=["numpy"])


def posicao_falsa(
    f: Callable[[float], float], # Função
    a: float, # Limite inferior
    b: float, # Limite superior
    tolerancia: float = 1e-6, # Tolerância para a convergência
    d_min: float = 1e-12, # Diferença mínima entre f(b) e f(a)
    ) -> tuple[float, float, int]:
    if f(a) * f(b) >= 0.0:
        raise ValueError("A função deve ter sinais diferentes em a e b.")

    err: float = 0.0
    i: int = 0

    while True:
        i += 1

        if f(b) - f(a) < d_min:
            raise ValueError("A diferença entre f(b) e f(a) é muito pequena.")

        c: float = (a * f(b) - b * f(a)) / (f(b) - f(a))
        err = abs(b - a)

        if abs(f(c)) <= tolerancia:
            return c, err, i

        if f(a) * f(c) < 0.0:
            b = c

        else:
            a = c


def processar_arquivo(caminho: str) -> None:
    with open(caminho, "r", encoding="utf-8") as arquivo_entrada:
        linhas: list[str] = [linha.strip() for linha in arquivo_entrada if linha.strip()]

    if len(linhas) < 5:
        raise ValueError("Linhas insuficientes no arquivo de entrada.")

    expressao: str = linhas[0]
    a: float = float(linhas[1])
    b: float = float(linhas[2])
    tolerancia: float = float(linhas[3])
    d_min: float = float(linhas[4])

    f: Callable[[float], float] = gerar_funcao(expressao)

    try:
        inicio: float = perf_counter()
        raiz, erro_absoluto, iteracoes = posicao_falsa(f, a, b, tolerancia, d_min)
        tempo_execucao: float = perf_counter() - inicio

        Path("saidas/raizes").mkdir(parents=True, exist_ok=True)

        with open("saidas/raizes/saida_posicao_falsa.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(f"Raiz: {raiz:.10f}\n")
            arquivo_saida.write(f"Erro Absoluto: {erro_absoluto:.10e}\n")
            arquivo_saida.write(f"Iterações: {iteracoes}\n")
            arquivo_saida.write(f"Tempo de Execução (s): {tempo_execucao:.10f}\n")

    except ValueError as e:
        print(f"Erro: {e}")


def main(args: list[str] | None = None) -> None:
    caminho_padrao: str = "entradas/entrada_raizes.txt"
    processar_arquivo(args[0] if args else caminho_padrao)


if __name__ == "__main__":
    main()
