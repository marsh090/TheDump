# 🌟 Labirinto Mágico em Python 🌟

Bem-vindo ao Labirinto Mágico, uma aventura emocionante escrita em Python! Este projeto não é apenas um labirinto comum; ele oferece uma série de funcionalidades incríveis que vão desde a geração de labirintos aleatórios até a resolução automática deles. 🎉

## 📋 Índice

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Executar](#como-executar)
- [Funcionalidades](# 🌈 Funcionalidades)
- [Contribuição](#contribuição)

## 🛠 Requisitos

- Python 3.x 🐍
- NumPy 🧮

## 📥 Instalação

1. Clone este repositório ou baixe o código-fonte.
2. Instale o NumPy usando pip:

    ```bash
    pip install numpy
    ```

## 🚀 Como Executar

Para embarcar nesta aventura, abra o terminal e execute:

```bash
python nome_do_arquivo.py
```

## 🌈 Funcionalidades

### 🎲 `geraLabirinto()`

Gera um labirinto aleatório para você explorar. Não requer nenhum argumento.

```python
labirinto.geraLabirinto()
```

### 💾 `salvaLabirinto(nome)`

Salva o labirinto atual em um arquivo para que você possa retomar sua aventura mais tarde.

```python
labirinto.salvaLabirinto("meu_labirinto_incrivel")
```

### 📂 `carregaLabirinto(nome)`

Carrega um labirinto previamente salvo para que você possa continuar de onde parou.

```python
labirinto.carregaLabirinto("meu_labirinto_incrivel")
```

### 🖨 `imprimeLabirinto()`

Imprime o labirinto atual no terminal. Ótimo para uma rápida espiada!

```python
labirinto.imprimeLabirinto()
```

### 🏆 `resolveLabirinto()`

Resolve o labirinto para você e mostra o caminho da vitória.

```python
labirinto.resolveLabirinto()
```

### 🔄 `realeatorizaLabirinto()`

Quer um novo desafio sem mudar o ponto de partida e chegada? Esta função realeatoriza o labirinto para você!

```python
labirinto.realeatorizaLabirinto()
```

### 🎮 Tela Inicial Interativa

Escolha o tamanho do seu labirinto antes de começar a aventura! Opções de "Pequeno", "Médio" e "Grande" disponíveis.
