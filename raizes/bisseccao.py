from pathlib import Path
from typing import Callable
import numpy
from sympy import symbols, sympify, lambdify


def gerar_funcao(expressao: str) -> Callable[[float], float]:
    return lambdify(symbols('x'), sympify(expressao), modules=["numpy"])


def bisseccao(
    f: Callable[[float], float], # Função
    a: float, # Limite inferior
    b: float, # Limite superior
    tolerancia: float = 1e-6 # Tolerância para a convergência
    ) -> tuple[float, float, int]:
    if f(a) * f(b) >= 0.0:
        raise ValueError("A função deve ter sinais diferentes em a e b.")

    err: float = 0.0
    i: int = 0

    while ((b - a) / 2.0) > tolerancia:
        i += 1
        c: float = (a + b) / 2.0
        err = abs(b - a)

        if f(c) == 0.0:
            return c, err, i

        elif f(a) * f(c) < 0.0:
            b = c

        else:
            a = c

    return (a + b) / 2.0, err, i


def processar_arquivo(caminho: str) -> None:
    with open(caminho, "r", encoding="utf-8") as arquivo_entrada:
        linhas: list[str] = [linha.strip() for linha in arquivo_entrada if linha.strip()]

    if len(linhas) < 4:
        raise ValueError("Linhas insuficientes no arquivo de entrada.")

    expressao: str = linhas[0]
    a: float = float(linhas[1])
    b: float = float(linhas[2])
    tolerancia: float = float(linhas[3])

    f: Callable[[float], float] = gerar_funcao(expressao)

    try:
        raiz, erro_absoluto, iteracoes = bisseccao(f, a, b, tolerancia)

        Path("saidas").mkdir(parents=True, exist_ok=True)

        with open("saidas/saida_bisseccao.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(f"Raiz: {raiz:.10f}\n")
            arquivo_saida.write(f"Erro Absoluto: {erro_absoluto:.10e}\n")
            arquivo_saida.write(f"Iterações: {iteracoes}\n")

    except ValueError as e:
        print(f"Erro: {e}")


def main(args: list[str] | None = None) -> None:
    caminho_padrao: str = "entradas/entrada_raizes.txt"
    processar_arquivo(args[0] if args else caminho_padrao)


if __name__ == "__main__":
    main()
