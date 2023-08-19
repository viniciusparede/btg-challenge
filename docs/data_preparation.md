# Compreensão dos dados
Um dos problemas do desafio consiste na integração dos dados de precipitação e os pontos que determinam a área da Bacia do Rio Grande.

## Arquivo de coordenadas geogŕaficas (Bacia do Rio Grande)
```python
read_contour_file(file_path: str)
```
### Visualização dos dados
| lat        	| long       	|
|------------	|------------	|
| -44.617282 	| -22.288938 	|
| -44.613593 	| -22.287491 	|
| -44.608377 	| -22.282603 	|

Os dados obtidos através do arquivo PSATCMG_CAMARGOS.bln representam as coordenadas geográficas da Bacia do Rio Grande. A figura abaixo representa uma visualização mais efetiva da região.

![Contorno Bacia Rio do Grande](/data/bacia_rio_grande.png)

## Arquivos de previsão de precipitação
O nome dos arquivos seguem o seguinte padrão: ETA40_p**ddmmyy**a**ddmmyy**.dat

A primeira data é referente a quando foi feita a previsão e a segunda data diz respeito qual data está sendo prevista.

Os arquivos disponibilizados estão em formato .dat e a função de leitura dos mesmos foi previamente cedida pela função

```python
read_dat_file_to_dataframe(file_path: str)
```

Percebe-se apenas olhando o nome dos arquivos que todos são referentes a data 01/12/2021 e a última data de previsão disponível é do dia 11/12/2021.

Para sabermos a previsão de precipitação acumulada dada pelo modelo do dia 01/12/2021 até o dia 11/12/2021 deveremos realizar a leitura de todos os arquivos disponibilizados.

### Visualização dos dados
| lat   | long | data_value |
|-------|------|------------|
| -30.2 | 3.4  | 4.7        |
| -30.2 | 3.8  | 3.8        |
| -30.2 | 4.2  | 0.0        |

Após abrir o arquivo nota-se três atributos. Os atributos lat e long representam latitude e longitude de um determinado ponto, portanto a coordenada geográfica e, a terceira variável nomeada como data_value demonstra precipitação diária acumulada naquele dia.

OBS: A resolução dos pontos de predição são menores comparados ao arquivo de coordenadas geográfica da Bacia do Rio Grande.

