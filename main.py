#!/usr/bin/env python

import pdfplumber
from pathlib import Path
import concurrent.futures
import sys
import validators


def extract_data_from_pdf(pdf_path, col_extract):
    """
    Extrai dados da coluna especificada de tabelas com pelo menos o número de colunas definido em um PDF específico.

    Args:
        pdf_path (Path): Caminho para o arquivo PDF.
        col_extract (int): Índice da coluna a ser extraída (0-based).

    Returns:
        tuple: (list de linhas válidas, list de linhas com erros)
    """
    output_lines = []
    output_lines_erro = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Itera sobre todas as páginas do PDF
            for i, page in enumerate(pdf.pages, start=1):
                # Extrai todas as tabelas da página
                tables = page.extract_tables()

                # Verifica se existem tabelas na página
                if tables:
                    for table_index, table in enumerate(tables, start=1):
                        # Itera sobre as linhas da tabela
                        for row_index, row in enumerate(table, start=1):
                            # Verifica se a linha tem pelo menos col_extract+1 colunas e pula a primeira linha (cabeçalho)
                            if len(row) > col_extract and row_index > 1:
                                dado_da_coluna = row[col_extract].strip()

                                # Formata a linha para o arquivo de output
                                formatted_line = (
                                    f'local-zone: "{dado_da_coluna}" always_nxdomain\n'
                                )

                                # Já descarto colunas vazias e endereços IP
                                if (
                                    dado_da_coluna
                                    and not validators.ipv4(dado_da_coluna)
                                    and not validators.ipv6(dado_da_coluna)
                                ):
                                    # Valida se é um dominio valido... se não for, adiciona no output de erros
                                    if validators.domain(dado_da_coluna):
                                        output_lines.append(formatted_line)
                                        # Imprime a mensagem de log
                                        print(
                                            f"[SUCESSO] - Arquivo: {pdf_path.name} | Página {i}, Tabela {table_index}, Linha {row_index}: '{dado_da_coluna}' adicionada no output"
                                        )
                                    else:
                                        output_lines_erro.append(formatted_line)
                                        print(
                                            f"[ERROR] - Arquivo: {pdf_path.name} | Página {i}, Tabela {table_index}, Linha {row_index}: '{dado_da_coluna}' adicionada no output de erros"
                                        )
                else:
                    # Indica que a página não possui tabelas
                    print(f"Arquivo: {pdf_path.name} | Página {i}: Não possui tabelas.")
    except Exception as e:
        print(f"Erro ao processar o arquivo {pdf_path.name}: {e}")

    return output_lines, output_lines_erro


def main():
    # Solicita ao usuário qual a coluna que ele quer extrair
    try:
        col_extract = (
            int(input("Digite o número da coluna que deseja extrair (1,2,3...): ")) - 1
        )
        if col_extract < 0:
            raise ValueError("O número da coluna deve ser positivo.")
    except ValueError as ve:
        print(f"Entrada inválida: {ve}")
        return

    # Define o diretório atual onde o script está localizado
    if getattr(sys, "frozen", False):
        current_dir = Path(sys.argv[0]).parent
    else:
        current_dir = Path(__file__).parent

    print(f"Diretório atual: {current_dir}")

    # Define os arquivos de saída
    output_file_path = current_dir / "output.txt"
    error_output_file_path = current_dir / "output_errors.txt"

    print(f"Arquivo de saída: {output_file_path}")
    print(f"Arquivo de erros: {error_output_file_path}")

    # Encontra todos os arquivos PDF na pasta atual
    pdf_files = list(current_dir.glob("*.pdf"))

    if not pdf_files:
        print("Nenhum arquivo PDF encontrado na pasta atual.")
        return

    all_output_lines = []
    all_error_lines = []

    # Utiliza ProcessPoolExecutor para processar PDFs em paralelo
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Mapeia a função extract_data_from_pdf para cada PDF encontrado
        # Isso retorna um gerador de futuros
        futures = {
            executor.submit(extract_data_from_pdf, pdf_path, col_extract): pdf_path
            for pdf_path in pdf_files
        }

        for future in concurrent.futures.as_completed(futures):
            pdf_path = futures[future]
            try:
                data, errors = future.result()
                all_output_lines.extend(data)
                all_error_lines.extend(errors)
                print(f"Concluída a extração do arquivo: {pdf_path.name}\n")
            except Exception as e:
                print(f"Erro ao processar o arquivo {pdf_path.name}: {e}")

    # Escreve todas as linhas válidas no arquivo de saída
    try:
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.writelines(all_output_lines)
        print(
            f"Extração concluída. Os dados válidos foram salvos em '{output_file_path}'."
        )
    except Exception as e:
        print(f"Erro ao escrever no arquivo de saída: {e}")

    # Escreve todas as linhas com erros no arquivo de erros
    if all_error_lines:
        try:
            with open(
                error_output_file_path, "w", encoding="utf-8"
            ) as error_output_file:
                error_output_file.writelines(all_error_lines)
            print(
                f"Alguns dados apresentaram erros e foram salvos em '{error_output_file_path}'."
            )
        except Exception as e:
            print(f"Erro ao escrever no arquivo de erros: {e}")
    else:
        print("Nenhum erro encontrado durante a extração.")


if __name__ == "__main__":
    main()
