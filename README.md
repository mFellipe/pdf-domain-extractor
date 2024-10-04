# Do que se trata?
- Este script foi criado com a finalidade de extrair a lista de bloqueio de sites da anatel
- Deve ser um pdf com 3 clunas sendo a terceira que deve conter os endereços para bloquear.

## Como utilizar?
- Utilize os comandos abaixo para realizar a instalação das dependências.

- Crie um venv
```python3 -m venv .venv```

- Ative o venv
```source .venv/bin/activate```

- Instale o pdfplumber
```pip install pdfplumber```

- Adicione todos os arquivos pdf dentro da pasta contendo o main.py e rode o script
```python3 main.py```