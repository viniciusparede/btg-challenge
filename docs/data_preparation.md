# Preparação dos dados
Um dos problemas do desafio consiste na integração dos dados do modelo de precipitação e os pontos que determinam a área da Bacia do Rio Grande. Iremos utilizar a função **apply_contour** como base para essa junção. Percebe-se após abrir os arquivos que os dados do modelo de precipitação disponibilizados contém precipitações em diferentes pontos, mas com uma resolução menor que os atributos contidos no arquivo de contorno da bacia.

Tomemos como exemplo dois conjuntos de dados de latitude: um expresso com apenas uma casa decimal (por exemplo, 37.7) e outro com quatro casas decimais (por exemplo, 37.7123). A disparidade na resolução desses dados pode resultar em consequências significativas durante análises geoespaciais.

```python
# Exemplo de latitudes com diferentes formatos
latitude1 = 37.7
latitude2 = 37.7123
```

A integração de dados geoespaciais com resoluções discrepantes pode ser problemática. Na tentativa de combinar conjuntos de dados, a falta de padronização pode levar a resultados imprecisos e dificultar a criação de análises abrangentes. No nosso caso não iremos conseguir combinar conjuntos de dados utilizando como chave primária as coordenadas geográficas.

## Resolução de coordenadas geográficas
Para estabelecer uma condição de contorno, primeiramente iremos utilizar a biblioteca **geopandas**.

O GeoPandas é um projeto de código aberto que visa facilitar o trabalho com dados geoespaciais em Python. O GeoPandas estende os tipos de dados utilizados pelo pandas para permitir operações espaciais em tipos geométricos.

A função **apply_contour** desempenha um papel crucial ao realizar uma rotina de pré-processamento especializada, na qual ocorre a conversão eficiente de DataFrames convencionais em GeoDataFrames enriquecidos. Essa rotina abrange diversas etapas que vão desde a junção baseada na proximidade geográfica até ajustes essenciais nas colunas dos dados.

Além disso, a etapa de junção por proximidade desempenha um papel fundamental. Ao aplicar essa técnica, a função reúne elementos que estão em estreita proximidade geográfica, possibilitando a criação de conexões significativas entre os dados. Essa junção é especialmente vantajosa em cenários nos quais a relação espacial entre os dados é crucial para a interpretação dos resultados.
