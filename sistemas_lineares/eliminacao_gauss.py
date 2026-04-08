from pathlib import Path
from time import perf_counter


def eliminacao_de_gauss(
    A: list[list[float]], # Matriz de coeficientes
    b: list[float] # Vetor de termos independentes
    ) -> list[float]:
    n: int = len(A)

    a: list[list[float]] = [A[i] + [b[i]] for i in range(n)]

    for k in range(n):
        linha_pivo: int = max(range(k, n), key = lambda i: abs(a[i][k]))

        if a[linha_pivo][k] == 0.0:
            raise ValueError("Não possui pivô válido.")

        if linha_pivo != k:
            a[k], a[linha_pivo] = a[linha_pivo], a[k]

        for i in range(k + 1, n):
            m_ik: float = a[i][k] / a[k][k]

            for j in range(k, n + 1):

                a[i][j] = a[i][j] - m_ik * a[k][j]

    x: list[float] = [0.0] * n

    for i in range(n - 1, -1, -1):
        soma: float = 0.0

        for j in range(i + 1, n):
            soma += a[i][j] * x[j]

        x[i] = (a[i][n] - soma) / a[i][i]

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
        solucao: list[float] = eliminacao_de_gauss(A, b)
        tempo_execucao: float = perf_counter() - inicio

        Path("saidas/sistemas_lineares").mkdir(parents=True, exist_ok=True)

        with open("saidas/sistemas_lineares/saida_eliminacao_gauss.txt", "w", encoding="utf-8") as arquivo_saida:
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
