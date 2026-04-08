from pathlib import Path
from time import perf_counter


def gauss_jordan(A: list[list[float]]) -> list[list[float]]:
    n: int = len(A)
    M: list[list[float]] = []

    for i in range(n):
        linha: list[float] = A[i][:]

        for j in range(n):
            if i == j:
                linha.append(1)
            else:
                linha.append(0)

        M.append(linha)

    for k in range(n):
        linha_pivo: int = max(range(k, n), key = lambda i: abs(M[i][k]))

        if M[linha_pivo][k] == 0.0:
            raise ValueError("Não possui pivô válido.")

        if linha_pivo != k:
            M[k], M[linha_pivo] = M[linha_pivo], M[k]

        pivo: float = M[k][k]

        for j in range(2 * n):
            M[k][j] = M[k][j] / pivo

        for i in range(n):
            if i != k:
                fator: float = M[i][k]

                for j in range(2 * n):
                    M[i][j] = M[i][j] - fator * M[k][j]

    inversa: list[list[float]] = []

    for i in range(n):
        inversa.append(M[i][n:])

    return inversa


def condicao(A: list[list[float]]) -> float:
    inversa: list[list[float]] = gauss_jordan(A)
    norma_A: float = max(sum(abs(x) for x in linha) for linha in A)
    norma_inversa: float = max(sum(abs(x) for x in linha) for linha in inversa)

    return norma_A * norma_inversa


def processar_arquivo(caminho: str) -> None:
    with open(caminho, "r", encoding="utf-8") as arquivo_entrada:
        linhas: list[str] = [linha.strip() for linha in arquivo_entrada if linha.strip()]

    try:
        if len(linhas) < 2:
            raise ValueError("Arquivo de entrada inválido.")

        n: int = int(linhas[0])
        matriz_entrada: list[list[float]] = [list(map(float, linha.split())) for linha in linhas[1:1+n]]

        if len(matriz_entrada) != n or any(len(linha) < n for linha in matriz_entrada):
            raise ValueError("Use: n na primeira linha e depois n linhas com ao menos n valores.")

        A: list[list[float]] = [linha[:n] for linha in matriz_entrada]

        inicio: float = perf_counter()
        numero_condicao: float = condicao(A)
        tempo_execucao: float = perf_counter() - inicio

        Path("saidas/condicionamento").mkdir(parents=True, exist_ok=True)

        with open("saidas/condicionamento/saida_condicionamento.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(f"Condição: {numero_condicao:.10f}\n")
            arquivo_saida.write(f"Tempo de Execução (s): {tempo_execucao:.10f}\n")

    except ValueError as e:
        print(f"Erro: {e}")


def main(args: list[str] | None = None) -> None:
    caminho_padrao: str = "entradas/entrada_condicionamento.txt"
    processar_arquivo(args[0] if args else caminho_padrao)


if __name__ == "__main__":
    main()
