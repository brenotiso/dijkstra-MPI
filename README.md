# Dijkstra MPI
Implementação do algoritmo de Dijkstra de forma paralela utilizando MPI.
Trabalho desenvolvido para a disciplina Programação Paralela e Concorrente - 2019/1


**Alunos:**
- Breno Henrique Tiso Tana
- Frederico Alves Gomes
-  Heuller Soares Vilela Silva
- Pedro Henrique Costa da Silva Moreira


## Intalação dos Requisitos
É necessário ter instalado o python3. Então execute:
```
$ pip install -r requirements.txt
```

## Execução
Para a execução de uma entrada qualquer utilize os seguintes comandos:

#### Para o código sequencial
```
$ python3 dijkstra_seq.py <nome-arquivo> <origem> <destino>

```

#### Para o código paralelo
```
$ mpiexec -n <numero-processadores> dijkstra_paralelo.py <nome-arquivo> 0 <destino>
```

## Dados de teste
Alguns dados de teste estão disponíveis na pasta datasets.
Outros podem ser obtidos em: https://toreopsahl.com/datasets/

