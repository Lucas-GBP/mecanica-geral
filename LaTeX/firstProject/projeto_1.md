# Projeto Computacional de Mecânica Clássica

## Queda Vertical em Meio Estratificado com Arrasto Assimétrico

**Prof. Rodrigo Rocha**
**Departamento de Física - UFSC**

## Introdução

Neste projeto, você irá estudar o movimento de um corpo sob a ação da gravidade em um meio resistivo não homogêneo. Diferentemente de modelos usuais, o arrasto dependerá:

- da velocidade (termos linear e quadrático),
- da posição (meio estratificado),
- e do sentido do movimento (assimetria entre subida e descida).

Esse modelo é mais próximo de situações reais, como movimento em fluidos com densidade variável ou objetos com geometria assimétrica. A assimetria nos coeficientes de arrasto modela objetos cuja interação com o fluido depende do sentido do movimento, como corpos deformáveis, estruturas aerodinâmicas não simétricas ou partículas que mudam sua orientação ao inverter a direção do movimento.

## Descrição do problema

Considere uma partícula de massa $m$ lançada verticalmente para cima a partir da posição $x = 0$, com velocidade inicial $v_0 > 0$.

Adote o eixo vertical orientado para cima.

As forças atuando sobre o sistema são:

### 1. Gravidade

$$
F_g = -mg
\tag{1}
$$

### 2. Força de arrasto

A força de arrasto depende do sentido da velocidade:

$$
F_d =
\begin{cases}
-\beta_\uparrow(x) v - \gamma_\uparrow(x) v^2, & v > 0 \quad \text{(subida)} \\
-\beta_\downarrow(x) v + \gamma_\downarrow(x) v^2, & v < 0 \quad \text{(descida)}
\end{cases}
\tag{2}
$$

### 3. Estratificação do meio

Os coeficientes de arrasto dependem da altura segundo:

$$
\beta_\uparrow(x) = \beta_0 e^{-x/H}, \qquad
\gamma_\uparrow(x) = \gamma_0 e^{-x/H}
\tag{3}
$$

onde:

- $\beta_0, \gamma_0 > 0$ são constantes,
- $H$ é uma escala característica de altura do meio.

A assimetria entre subida e descida é parametrizada por:

$$
\beta_\downarrow(x) = r_\beta \beta_\uparrow(x), \qquad
\gamma_\downarrow(x) = r_\gamma \gamma_\uparrow(x)
\tag{4}
$$

## Equação de movimento

A equação de movimento é dada por:

$$
m\frac{dv}{dt} = F_g + F_d
\tag{5}
$$

ou explicitamente:

$$
m\frac{dv}{dt} =
\begin{cases}
-mg - \beta_\uparrow(x) v - \gamma_\uparrow(x) v^2, & v > 0 \\
-mg - \beta_\downarrow(x) v + \gamma_\downarrow(x) v^2, & v < 0
\end{cases}
\tag{6}
$$

com:

$$
\frac{dx}{dt} = v
\tag{7}
$$

## Questões

1. Discretize as equações de movimento (Eqs. 6 e 7) utilizando o método de Euler com passo $\Delta t$. Apresente explicitamente as expressões para $x_{n+1}$ e $v_{n+1}$ em termos de $x_n$, $v_n$ e demais parâmetros do modelo.

2. Faça uma análise gráfica do comportamento dos parâmetros $\beta_\uparrow$ e $\gamma_\uparrow$ com relação a $x$, para diferentes valores dos parâmetros $\beta_0$, $\gamma_0$ e $H$. Discuta como as variações nesses parâmetros influenciam as curvas obtidas.

3. Faça uma análise gráfica do comportamento dos parâmetros $\beta_\downarrow$ e $\gamma_\downarrow$ em função de $x$, considerando diferentes cenários para os parâmetros, tais como $r_\beta > 0$, $r_\beta < 0$, $r_\gamma > 0$ e $r_\gamma < 0$. Discuta como essas diferentes condições influenciam as curvas obtidas.

4. Apresente um pseudocódigo contendo as estruturas principais para a integração numérica das equações de movimento da partícula. Seu pseudocódigo deve incluir: inicialização das variáveis, definição dos parâmetros, laço temporal e atualização de $x$ e $v$ a cada passo de tempo.

5. Implemente o algoritmo em uma linguagem de programação de sua escolha e resolva numericamente as equações de movimento para um conjunto de parâmetros fixos ($\beta_0$, $\gamma_0$, $r_\beta$, $r_\gamma$, $H$, etc.). Apresente os resultados obtidos ($x(t)$ e $v(t)$) e discuta o comportamento da solução.

   **Nota:** a integração numérica deve ser realizada em duas etapas distintas: uma correspondente à subida da partícula e outra à descida.

6. A partir da solução numérica obtida, determine:

   - a altura máxima atingida pela partícula ($x^\ast$);
   - a velocidade de impacto na descida ($v^\ast$) em $x = 0$;
   - compare os tempos de subida ($\tau_\uparrow$) e descida ($\tau_\downarrow$).

7. Realize uma exploração paramétrica do sistema. O objetivo é determinar a dependência de $x^\ast$, $v^\ast$, $\tau_\uparrow$ e $\tau_\downarrow$ em função dos parâmetros $\beta_0$, $\gamma_0$, $r_\beta$, $r_\gamma$ e $H$. Escolha apenas um único parâmetro para variar, mantendo os demais fixos. Apresente os gráficos de $x^\ast$, $v^\ast$, $\tau_\uparrow$ e $\tau_\downarrow$ em função do parâmetro escolhido.

   **Exemplo:** caso a escolha seja $r_\beta$, construa os gráficos de $x^\ast$, $v^\ast$, $\tau_\uparrow$ e $\tau_\downarrow$ em função de $r_\beta$. Discuta como variações nesses parâmetros influenciam as curvas obtidas.

## Observações

- Não se espera que seja obtida uma solução analítica fechada; o uso de métodos numéricos é fundamental.
- A análise física dos resultados é parte essencial do projeto e deve ser apresentada com clareza.
- O projeto é individual; caso sejam utilizadas ferramentas externas, como softwares ou inteligência artificial, seu uso deve ser declarado de forma transparente.
- A apresentação dos resultados (gráficos, tabelas e discussões) deve ser organizada e coerente, facilitando a interpretação dos dados obtidos.
- A versão final do relatório deve ser entregue em PDF. Sugere-se o uso de LaTeX, mas Word também será aceito.
