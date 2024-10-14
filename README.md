# Do que se trata?
- Este script foi criado com a finalidade de extrair a lista de bloqueio de sites da anatel
- Deve ser um pdf com 3 clunas sendo a terceira que deve conter os endereços para bloquear.

## Como instalar?
- Baixe o binário em releases coloque na mesma pasta dos arquivos .pdf que deseja extrair e rode o comando.
```chmod +x pdf-extractor* && sudo mv ./pdf-extractor* /usr/bin/pdf-extractor```


## Como utilizar o codigo fonte?
- Utilize os comandos abaixo para realizar a instalação das dependências.


- [1] Clone o repositório em qualquer pasta
```git clone https://github.com/mFellipe/pdf-domain-extractor.git && cd pdf-domain-extractor```

- [2] Crie um venv
```python3 -m venv .venv```

- [3] Ative o venv
```source .venv/bin/activate```

- [4] Instale o pdfplumber
```pip install pdfplumber```

- [5] Adicione todos os arquivos pdf dentro da pasta contendo o main.py e rode o script
```python3 main.py```

- Obs: após fazer os passos uma primeira vez, para utilizar o programa novamente utilize apenas os comandos 3 e 5 na pasta do projeto.
