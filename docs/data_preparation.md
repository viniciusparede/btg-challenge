# Compreensão dos dados
Um dos problemas do desafio consiste na integração dos dados de precipitação e os pontos das áreas. O dados de previsão disponibilizados 

Podemos perceber que a medida que se arredonda os dados de latitude e longitude com um número menor de casas decimais o mapa perde resolução. Infelizmente os dados de do modelo de precisão contém 2 casas decimais de resolução, portando teremos que aproximar a maior quantidade de pontos possíveis do mapa da bacia com os dados de precipitação. Para resolver esse problema, utilizando a biblioteca geopandas, que trabalha com dataframes