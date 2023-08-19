# Preparação dos dados
Uma das dificuldades encontradas no desafio está relacionada à integração dos dados provenientes do modelo de precipitação com os pontos que delimitam a extensão da Bacia do Rio Grande. Para realizar essa junção, utiliza-se como base a função apply_contour. Ao examinar os arquivos, torna-se evidente que os dados fornecidos pelo modelo de precipitação contêm informações de precipitação associadas a diferentes pontos. No entanto, nota-se que a resolução desses dados é menor em comparação com os atributos presentes no arquivo de contorno da bacia.

Vamos considerar a seguinte situação com dois conjuntos de dados de latitudes como exemplo: um ponto com apenas uma casa decimal (por exemplo, 37.7) e outro com quatro casas decimais (por exemplo, 37.7123). A discrepância na resolução desses dados pode acarretar em implicações significativas durante a condução de análises geoespaciais.

```python
# Exemplo de latitudes com diferentes formatos
latitude1 = 37.7
latitude2 = 37.7123
```

A integração de dados geoespaciais com resoluções discrepantes pode apresentar desafios significativos. Ao tentar combinar conjuntos de dados, a ausência de padronização pode resultar em conclusões imprecisas e tornar mais complexa a elaboração de análises abrangentes. No nosso caso, não será viável a utilização das coordenadas geográficas como chave primária para a junção dos conjuntos de dados.

## Resolução de coordenadas geográficas
Para estabelecer uma condição de contorno, primeiramente iremos utilizar a biblioteca **geopandas**.

O GeoPandas é um projeto de código aberto que visa facilitar o trabalho com dados geoespaciais em Python. O GeoPandas estende os tipos de dados utilizados pelo pandas para permitir operações espaciais em tipos geométricos.

A função **apply_contour** desempenha um papel crucial ao realizar uma rotina de pré-processamento especializada, na qual ocorre a conversão eficiente de DataFrames convencionais em GeoDataFrames enriquecidos. Essa rotina abrange diversas etapas que vão desde a junção baseada na proximidade geográfica até ajustes essenciais nas colunas dos dados.

A etapa de junção por proximidade produz nossa condição de contorno ao problema. Ao aplicar essa técnica, a função reúne elementos que estão em estreita proximidade geográfica, possibilitando a criação de conexões significativas entre os dados. Essa junção é especialmente vantajosa em cenários nos quais a relação espacial entre os dados é crucial para interpolação dos dados

Para transformar um conjunto de dados do tipo Pandas em GeoPandas necessitamos criar uma coluna do tipo 'geometry' para ser nossa chave primária. A figura representa como os dados da latitude e longitude de determinado ponto são repassados.

![Coluna do tipo 'geometry'](/images/geometry.webp)

A partir dessa coluna podemos realizar a operação de 'join' com base na coluna 'geometry'. Essa operação visa a junção espacial de dois GeoDataFrames com base na distância entre suas geometrias.

Os resultados incluirão vários registros de saída para um único registro de entrada onde há vários vizinhos equidistantes mais próximos ou com interseção.

```python
# Realizar a junção usando o método sjoin_nearest com base na coluna geometry
result = gpd.sjoin_nearest(
    left_df=gcontour_df,
    right_df=gforecast_df,
    how="left",
    distance_col="distance",
    max_distance=sys.maxsize,
)
```

Como resultado final:
| lat_referencia 	| long_referencia 	| lat_aproximacao 	| long_aproximacao 	| data_value 	| distance 	| data_previsao 	|
|----------------	|-----------------	|-----------------	|------------------	|------------	|----------	|---------------	|
| -44.569716     	| -22.239244      	| -44.6           	| -22.2            	| 18.0       	| 0.04957  	| 10/12/2021    	|
| -44.408722     	| -22.202038      	| -44.6           	| -22.2            	| 1.0        	| 0.191289 	| 02/12/2021    	|
| -44.305087     	| -22.136691      	| -44.2           	| -22.2            	| 29.7       	| 0.122683 	| 08/12/2021    	|

## Análise do contorno criado
Após aplicar o préprocessamento dos dados o seguinte polígono foi criado
![Contorno de aproximação](/images/contorno.png)

Nota-se que o polígono de delimitação aproximada, construído por meio da manipulação dos dados, abrange uma extensão adequada para viabilizar a previsão de precipitação. É importante ressaltar que alcançar uma delimitação perfeita é inviável devido às limitações de resolução dos dados. No entanto, para fins práticos, a delimitação atual se alinha de maneira consistente com as características da Bacia do Rio Grande.

No contexto deste desafio, adotaremos os seguintes vértices:

```python
[
    (-44.6, -22.2),
    (-44.6, -21.8),
    (-44.6, -21.4),
    (-44.2, -21.4),
    (-43.8, -21.4),
    (-43.8, -21.8),
    (-44.2, -21.8),
    (-44.2, -22.2),
]
```
