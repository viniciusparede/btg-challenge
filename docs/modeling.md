# Qual é a quantidade de pluviométrica nessa região?
Para cada vértice que compõe o polígono, dispomos da previsão da acumulação diária de precipitação, contudo, a quantidade de chuva estimada para um ponto específico não necessariamente se aplica a todos os outros pontos dentro da abrangência do polígono.

Empregamos a técnica de interpolação de dados. A interpolação de dados é um método utilizado para estimar valores desconhecidos entre pontos conhecidos em um conjunto de dados. Isso envolve a criação de uma função ou modelo matemático que preenche as lacunas entre os pontos existentes, proporcionando uma estimativa contínua e suave dos valores intermediários.

Exemplo:
Suponhamos que a precipitação em um ponto específico (-44,6, -22,2) tenha sido de 18 mm. Qual seria a quantidade de precipitação no ponto (-44,3, -22,1)? Para resolver essa incógnita, utilizaremos a técnica de interpolação fornecida pela biblioteca scipy.interpolate.

```python
# Interpolação
grid_precipitacao = griddata(
    (latitude, longitude), 
    precipitacao, 
    (grid_x, grid_y), 
    method="cubic"
)
```

## Resultado
Para cada dia previsto realizamos a interpolação dos dados para saber qual a precipitação daquela área, conforme a figura.
![Previsão de precipitação Área](/images/interpolacao.png)

Após obtermos esses dados interpolados de previsão de precipitação, surge a necessidade de calcular a integral cumulativa que representa a acumulação desses valores. Isso é especialmente útil para entender a quantidade total de precipitação ocorrida na região de interesse durante o período analisado.

Para realizar esse cálculo, utilizaremos a função **cumulative_trapezoid**. Essa função aplica a técnica dos trapézios acumulativos, que consiste em aproximar a área sob a curva da previsão de precipitação por meio de trapézios individuais em intervalos de tempo discretos. A integral cumulativa resultante nos dará uma estimativa da quantidade total de precipitação acumulada ao longo do período.



