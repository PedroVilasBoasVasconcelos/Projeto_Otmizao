# Projeto de Otimização Linear

Aplicação web desenvolvida em Python com Flask para resolução de problemas de Programação Linear. O sistema permite montar a função objetivo, inserir restrições, escolher entre maximização ou minimização, calcular a solução ótima, visualizar o preço sombra e realizar análise de sensibilidade.

## Funcionalidades

- Cadastro da quantidade de variáveis
- Cadastro da quantidade de restrições
- Escolha entre maximizar ou minimizar
- Montagem da função objetivo
- Inserção dos coeficientes das restrições
- Escolha dos operadores das restrições
- Cálculo da solução ótima
- Exibição dos valores das variáveis
- Cálculo do valor da função objetivo
- Cálculo do preço sombra
- Análise de sensibilidade
- Alteração das restrições mantendo os dados já preenchidos
- Reset completo do problema
- Interface web moderna e responsiva

## Tecnologias utilizadas

- Python
- Flask
- SciPy
- HTML
- CSS
- JavaScript

## Estrutura do projeto

```text
Projeto-de-otimizacao/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── particles.js
│   ├── templates/
│   │   ├── form.html
│   │   ├── result.html
│   │   └── post_optimization.html
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── form_utils.py
│   │   ├── post_optimization_utils.py
│   │   └── shadow_price_process.py
│   ├── __init__.py
│   └── routes.py
├── .gitignore
├── config.py
├── README.md
├── requirements.txt
└── run.py
```

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Greed2003/Projeto-de-otimizacao.git
```

```bash
cd Projeto-de-otimizacao
```

### 2. Criar o ambiente virtual

É recomendado utilizar o Python 3.11.

```bash
py -3.11 -m venv venv
```

### 3. Ativar o ambiente virtual

No Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Caso apareça erro de permissão, execute:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois ative novamente:

```bash
.\venv\Scripts\Activate.ps1
```

### 4. Atualizar o pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 5. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

Caso ocorra erro na instalação do NumPy ou SciPy, instale os pacotes binários primeiro:

```bash
python -m pip install numpy scipy --only-binary=:all:
```

Depois execute novamente:

```bash
python -m pip install -r requirements.txt
```

### 6. Executar o projeto

```bash
python run.py
```

Depois acesse no navegador:

```text
http://127.0.0.1:5000
```

## Como usar o sistema

1. Escolha a quantidade de variáveis.
2. Escolha a quantidade de restrições.
3. Clique em **Montar modelo**.
4. Escolha o tipo de otimização: **Maximizar** ou **Minimizar**.
5. Preencha os coeficientes da função objetivo.
6. Preencha os coeficientes das restrições.
7. Escolha o operador de cada restrição.
8. Informe o lado direito de cada restrição.
9. Clique em **Otimizar modelo**.
10. Veja o valor ótimo da função objetivo.
11. Veja os valores encontrados para cada variável.
12. Veja o preço sombra de cada restrição.
13. Use a análise de sensibilidade para testar alterações no lado direito das restrições.
14. Caso necessário, clique em **Alterar restrições** para voltar ao formulário mantendo os dados preenchidos.
15. Clique em **Resetar tudo** para limpar os dados e iniciar um novo problema.

## Exemplos de teste

### Exemplo de maximização

Função objetivo:

```text
Max Z = 40A + 30B
```

Preenchimento da função objetivo:

```text
A = 40
B = 30
```

Restrições:

```text
A + B ≤ 100
2A + B ≤ 140
A + 3B ≤ 180
```

Preenchimento das restrições:

```text
Restrição 1:
A = 1
B = 1
Operador = ≤
Lado direito = 100

Restrição 2:
A = 2
B = 1
Operador = ≤
Lado direito = 140

Restrição 3:
A = 1
B = 3
Operador = ≤
Lado direito = 180
```

Resultado esperado aproximado:

```text
A = 48
B = 44
Z = 3240
```

### Exemplo de minimização

Função objetivo:

```text
Min Z = 8A + 6B
```

Preenchimento da função objetivo:

```text
A = 8
B = 6
```

Restrições:

```text
2A + B ≥ 10
A + 3B ≥ 12
```

Preenchimento das restrições:

```text
Restrição 1:
A = 2
B = 1
Operador = ≥
Lado direito = 10

Restrição 2:
A = 1
B = 3
Operador = ≥
Lado direito = 12
```

Resultado esperado aproximado:

```text
A = 3.6
B = 2.8
Z = 45.6
```

## Telas do sistema

O projeto possui três telas principais:

### Tela inicial

Tela utilizada para escolher a quantidade de variáveis e restrições do problema.

### Tela de montagem do modelo

Tela utilizada para:

- Escolher entre maximização ou minimização
- Preencher a função objetivo
- Preencher as restrições
- Escolher os operadores
- Informar os lados direitos das restrições

### Tela de resultado

Tela que exibe:

- Tipo de otimização escolhido
- Valor da função objetivo
- Valores das variáveis
- Preço sombra
- Campos para análise de sensibilidade

### Tela de pós-otimização

Tela que exibe o novo resultado após alterações feitas na análise de sensibilidade.

## Observações

- O projeto utiliza o método Simplex por meio da biblioteca SciPy.
- O sistema permite resolver problemas de maximização e minimização em Programação Linear.
- As variáveis são representadas automaticamente por letras, como A, B, C e D.
- O botão **Alterar restrições** permite voltar ao formulário sem apagar os dados já preenchidos.
- O botão **Resetar tudo** limpa a sessão e retorna para a tela inicial.
- Para problemas de maximização, o sistema converte internamente a função objetivo para o formato utilizado pelo método de otimização.
- Para problemas de minimização, o sistema utiliza os coeficientes informados diretamente na função objetivo.

## Comandos Git úteis

Verificar alterações:

```bash
git status
```

Adicionar arquivos modificados:

```bash
git add .
```

Criar commit:

```bash
git commit -m "Atualiza projeto"
```

Enviar alterações para o GitHub:

```bash
git push
```

## Autor

Desenvolvido por Igor Olivio / Pedro Vasconcelos.
