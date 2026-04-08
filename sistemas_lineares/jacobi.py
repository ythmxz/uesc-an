from pathlib import Path
from time import perf_counter


def jacobi(
    A: list[list[float]], # Matriz de coeficientes
    b: list[float], # Vetor de termos independentes
    x0: list[float] | None = None, # Chute inicial
    tolerancia: float = 1e-6, # Critério de convergência
    i_max: int = 100 # Número máximo de iterações
    ) -> list[float]:
    n: int = len(A)

    if x0 is None:
        x: list[float] = [0.0] * n
    else:
        x: list[float] = x0[:]

    x_novo: list[float] = [0.0] * n

    for _ in range(i_max):
        for i in range(n):
            soma: float = 0.0

            for j in range(n):
                if j != i:
                    soma += A[i][j] * x[j]

            x_novo[i] = (b[i] - soma) / A[i][i]

        erro: float = 0.0

        for i in range(n):
            erro = max(erro, abs(x_novo[i] - x[i]))

        x: list[float] = x_novo[:]

        if erro < tolerancia:
            break

    return x


def processar_arquivo(caminho: str) -> None:
    with open(caminho, "r", encoding="utf-8") as arquivo_entrada:
        linhas: list[str] = [linha.strip() for linha in arquivo_entrada if linha.strip()]

    try:
        if len(linhas) < 2:
            raise ValueError("Arquivo de entrada inválido.")

        n: int = int(linhas[0])
        sistema: list[list[float]] = [list(map(float, linha.split())) for linha in linhas[1:1+n]]

        if len(sistema) != n or any(len(linha) != n + 1 for linha in sistema):
            raise ValueError("Use: n na primeira linha e depois n linhas com n+1 valores.")

        A: list[list[float]] = [linha[:-1] for linha in sistema]
        b: list[float] = [linha[-1] for linha in sistema]

        inicio: float = perf_counter()
        solucao: list[float] = jacobi(A, b)
        tempo_execucao: float = perf_counter() - inicio

        Path("saidas/sistemas_lineares").mkdir(parents=True, exist_ok=True)

        with open("saidas/sistemas_lineares/saida_jacobi.txt", "w", encoding="utf-8") as arquivo_saida:
            for i, valor in enumerate(solucao, start=1):
                arquivo_saida.write(f"x{i}: {valor:.10f}\n")
            arquivo_saida.write(f"Tempo de Execução (s): {tempo_execucao:.10f}\n")

    except ValueError as e:
        print(f"Erro: {e}")


def main(args: list[str] | None = None) -> None:
    caminho_padrao: str = "entradas/entrada_sistemas_lineares.txt"
    processar_arquivo(args[0] if args else caminho_padrao)


if __name__ == "__main__":
    main()
