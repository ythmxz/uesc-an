from pathlib import Path
from time import perf_counter


def fatoracao_LU(
    A: list[list[float]], # Matriz de coeficientes
    b: list[float] # Vetor de termos independentes
    ) -> tuple[list[float], list[list[float]], list[list[float]]]:
    n = len(A)

    L: list[list[float]] = [[0.0] * n for _ in range(n)]
    U: list[list[float]] = [linha[:] for linha in A]
    b_permutado: list[float] = b[:]

    for i in range(n):
        L[i][i] = 1.0

    for k in range(n):
        linha_pivo: int = max(range(k, n), key = lambda i: abs(U[i][k]))

        if U[linha_pivo][k] == 0.0:
            raise ValueError("Não possui pivô válido.")

        if linha_pivo != k:
            U[k], U[linha_pivo] = U[linha_pivo], U[k]
            b_permutado[k], b_permutado[linha_pivo] = b_permutado[linha_pivo], b_permutado[k]

            for j in range(k):
                L[k][j], L[linha_pivo][j] = L[linha_pivo][j], L[k][j]

        for i in range(k + 1, n):
            m_ik: float = U[i][k] / U[k][k]

            L[i][k] = m_ik

            for j in range(k, n):
                U[i][j] = U[i][j] - m_ik * U[k][j]

    y: list[float] = [0.0] * n

    for i in range(n):
        soma: float = 0.0

        for j in range(i):
            soma += L[i][j] * y[j]

        y[i] = b_permutado[i] - soma

    x: list[float] = [0.0] * n

    for i in range(n - 1, -1, -1):
        soma: float = 0.0

        for j in range(i+1, n):
            soma += U[i][j] * x[j]

        x[i] = (y[i] - soma) / U[i][i]

    return x, L, U


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
        x, L, U = fatoracao_LU(A, b)
        tempo_execucao: float = perf_counter() - inicio

        Path("saidas/sistemas_lineares").mkdir(parents=True, exist_ok=True)

        with open("saidas/sistemas_lineares/saida_fatoracao_lu.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write("Solução:\n")
            for i, valor in enumerate(x, start=1):
                arquivo_saida.write(f"x{i}: {valor:.10f}\n")

            arquivo_saida.write("\nMatriz L:\n")
            for linha in L:
                arquivo_saida.write(" ".join(f"{valor:.10f}" for valor in linha) + "\n")

            arquivo_saida.write("\nMatriz U:\n")
            for linha in U:
                arquivo_saida.write(" ".join(f"{valor:.10f}" for valor in linha) + "\n")

            arquivo_saida.write(f"\nTempo de Execução (s): {tempo_execucao:.10f}\n")

    except ValueError as e:
        print(f"Erro: {e}")


def main(args: list[str] | None = None) -> None:
    caminho_padrao: str = "entradas/entrada_sistemas_lineares.txt"
    processar_arquivo(args[0] if args else caminho_padrao)


if __name__ == "__main__":
    main()
