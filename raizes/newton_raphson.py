from pathlib import Path
from typing import Callable
import numpy
from sympy import symbols, sympify, lambdify


def gerar_funcao(expressao: str) -> Callable[[float], float]:
    return lambdify(symbols('x'), sympify(expressao), modules=["numpy"])

def derivada(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)


def newton_raphson(
    f: Callable[[float], float], # Função
    df: Callable[[Callable[[float], float], float, float], float], # Derivada
    x0: float, # Chute inicial
    tolerancia: float = 1e-6, # Tolerância para a convergência
    df_min: float = 1e-12, # Valor mínimo para a derivada
    i_max: int = 100, # Número máximo de iterações
    h: float = 1e-6, # Passo para a derivada numérica
    ) -> tuple[float, int]:
    for i in range(1, i_max + 1):

        if abs(f(x0)) <= tolerancia:
            return x0, i

        if abs(df(f, x0, h)) < df_min:
            raise ValueError("Derivada muito próxima de zero.")

        x1: float = x0 - f(x0) / df(f, x0, h)

        if abs(x1 - x0) <= tolerancia:
            return x1, i

        x0 = x1

    raise ValueError("Não convergiu dentro do número máximo de iterações.")


def processar_arquivo(caminho: str) -> None:
    with open(caminho, "r", encoding="utf-8") as arquivo_entrada:
        linhas: list[str] = [linha.strip() for linha in arquivo_entrada if linha.strip()]

    if len(linhas) < 7:
        raise ValueError("Linhas insuficientes no arquivo de entrada.")

    expressao: str = linhas[0]
    x0: float = (float(linhas[1]) + float(linhas[2])) / 2.0
    tolerancia: float = float(linhas[3])
    df_min: float = float(linhas[4])
    i_max: int = int(linhas[5])
    h: float = float(linhas[6])


    f: Callable[[float], float] = gerar_funcao(expressao)

    try:
        raiz, iteracoes = newton_raphson(f, derivada, x0, tolerancia, df_min, i_max, h)

        Path("saidas").mkdir(parents=True, exist_ok=True)

        with open("saidas/saida_newton_raphson.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(f"Raiz: {raiz:.10f}\n")
            arquivo_saida.write(f"Iterações: {iteracoes}\n")

    except ValueError as e:
        print(f"Erro: {e}")


def main(args: list[str] | None = None) -> None:
    caminho_padrao: str = "entradas/entrada_raizes.txt"
    processar_arquivo(args[0] if args else caminho_padrao)


if __name__ == "__main__":
    main()
