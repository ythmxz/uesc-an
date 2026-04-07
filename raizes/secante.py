from pathlib import Path
from typing import Callable
import numpy
from sympy import symbols, sympify, lambdify


def gerar_funcao(expressao: str) -> Callable[[float], float]:
    return lambdify(symbols('x'), sympify(expressao), modules=["numpy"])


def secante(
    f: Callable[[float], float], # Função
    x0: float, # Chute inicial 1
    x1: float, # Chute inicial 2
    tolerancia: float = 1e-6, # Tolerância para a convergência
    d_min: float = 1e-12, # Valor mínimo para o denominador
    i_max: int = 100, # Número máximo de iterações
    ) -> tuple[float, int]:
    for i in range(1, i_max + 1):
        if abs(f(x1) - f(x0)) < d_min:
            raise ValueError("Denominador muito pequeno.")

        x2: float = (f(x1) * x0 - f(x0) * x1) / (f(x1) - f(x0))

        if abs(f(x2)) <= tolerancia or abs(x2 - x1) <= tolerancia:
            return x2, i

        x0 = x1
        x1 = x2

    raise ValueError("Não convergiu dentro do número máximo de iterações.")


def processar_arquivo(caminho: str) -> None:
    with open(caminho, "r", encoding="utf-8") as arquivo_entrada:
        linhas: list[str] = [linha.strip() for linha in arquivo_entrada if linha.strip()]

    if len(linhas) < 6:
        raise ValueError("Linhas insuficientes no arquivo de entrada.")

    expressao: str = linhas[0]
    x0: float = float(linhas[1])
    x1: float = float(linhas[2])
    tolerancia: float = float(linhas[3])
    d_min: float = float(linhas[4])
    i_max: int = int(linhas[5])

    f: Callable[[float], float] = gerar_funcao(expressao)

    try:
        raiz, iteracoes = secante(f, x0, x1, tolerancia, d_min, i_max)

        Path("saidas").mkdir(parents=True, exist_ok=True)

        with open("saidas/saida_secante.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(f"Raiz: {raiz:.10f}\n")
            arquivo_saida.write(f"Iterações: {iteracoes}\n")

    except ValueError as e:
        print(f"Erro: {e}")


def main(args: list[str] | None = None) -> None:
    caminho_padrao: str = "entradas/entrada_raizes.txt"
    processar_arquivo(args[0] if args else caminho_padrao)


if __name__ == "__main__":
    main()
