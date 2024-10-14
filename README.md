# Do que se trata?
- Este script foi criado com a finalidade de extrair a lista de bloqueio de sites da anatel
- Deve ser um pdf com 3 clunas sendo a terceira que deve conter os endereços para bloquear.

## Como utilizar?
- Utilize os comandos abaixo para realizar a instalação das dependências.


- [1] Clone o repositório em qualquer pasta
```git clone https://github.com/mFellipe/pdf-domain-extrator.git && cd pdf-domain-extrator```

- [2] Crie um venv
```python3 -m venv .venv```

- [3] Ative o venv
```source .venv/bin/activate```

- [4] Instale o pdfplumber
```pip install pdfplumber```

- [5] Adicione todos os arquivos pdf dentro da pasta contendo o main.py e rode o script
```python3 main.py```

- Obs: após fazer os passos uma primeira vez, para utilizar o programa novamente utilize apenas os comandos 3 e 5 na pasta do projeto.
