from pathlib import Path
import sys

import bisseccao
import newton_raphson
import posicao_falsa
import secante


def executar_todos(caminho_entrada: str) -> None:
	metodos = [
		("Bissecção", bisseccao.processar_arquivo),
		("Posição Falsa", posicao_falsa.processar_arquivo),
		("Newton-Raphson", newton_raphson.processar_arquivo),
		("Secante", secante.processar_arquivo),
	]

	for nome, funcao in metodos:
		try:
			funcao(caminho_entrada)
			print(f"[OK] {nome}")
		except Exception as erro:
			print(f"[ERRO] {nome}: {erro}")


def main(args: list[str] | None = None) -> None:
	argumentos = args if args is not None else sys.argv[1:]
	caminho_padrao = Path("entradas") / "entrada_raizes.txt"
	caminho_entrada = argumentos[0] if argumentos else str(caminho_padrao)

	executar_todos(caminho_entrada)


if __name__ == "__main__":
	main()
