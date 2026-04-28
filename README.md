## Password Generator CLI

Projeto Python de linha de comando para gerar e validar senhas seguras.

### Funcionalidades

- Geracao criptograficamente segura com `secrets`
- Escolha de letras maiusculas, minusculas, numeros e simbolos
- Garantia de pelo menos um caractere de cada grupo selecionado
- Modo automatico ou manual na CLI
- Validacao final da senha gerada ou informada
- Testes automatizados com `pytest`

### Requisitos

- Python 3.10+

### Instalacao

```powershell
python -m pip install -r requirements.txt
```

### Como executar

```powershell
python -m app.cli
```

A aplicacao pergunta no inicio se voce quer:

- gerar uma senha automaticamente
- informar uma senha manualmente

### Exemplos

Geracao automatica:

```powershell
python -m app.cli --mode automatic --length 12 --uppercase --lowercase --numbers --symbols
```

Senha manual:

```powershell
python -m app.cli --mode manual --password MinhaSenha123! --uppercase --lowercase --numbers --symbols
```

### Diagrama

Fluxo principal da aplicacao:

```mermaid
flowchart TD
    A[Inicio] --> B[Executa app/cli.py]
    B --> C{Modo escolhido}
    C -->|Automatico| D[Gerar senha]
    C -->|Manual| E[Informar senha]
    D --> F[app/generator.py]
    F --> G[Seleciona grupos de caracteres]
    G --> H[Valida opcoes]
    H --> I[Gera senha com secrets]
    E --> J[Recebe senha do usuario]
    I --> K[app/validators.py]
    J --> K
    K --> L[Valida regras da senha]
    L --> M[Mostra resultado no terminal]
```

Estrutura dos modulos:

```mermaid
flowchart LR
    A[cli.py] --> B[generator.py]
    A --> C[validators.py]
    B --> C
    D[test_generator.py] --> A
    D --> B
    D --> C
```

### Testes

```powershell
python -m pytest -q
```
