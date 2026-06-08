# Projeto Computacional de Mecânica Clássica

## Oscilações Não Lineares

**Prof. Rodrigo Rocha**  
**Departamento de Física - UFSC**

## Introdução

Neste projeto, você irá estudar numericamente o movimento de um oscilador não linear sujeito a amortecimento e força externa periódica. Diferentemente do oscilador harmônico simples, o sistema estudado possui:

- força restauradora não linear;
- dissipação de energia;
- excitação externa periódica.

Esse modelo aparece em diversos contextos físicos, como:

- vibrações mecânicas;
- circuitos elétricos;
- sistemas estruturais;
- dinâmica molecular;
- sistemas oscilatórios reais.

O objetivo do projeto é investigar como os diferentes parâmetros do sistema afetam o comportamento dinâmico das oscilações.

## Descrição do problema

Considere uma partícula de massa $m$ movendo-se ao longo do eixo $x$, sujeita às seguintes forças:

### 1. Força restauradora não linear

$$
F_r = -kx - \alpha x^3
\tag{1}
$$

onde $k > 0$ é a constante elástica linear e $\alpha$ controla a intensidade da não linearidade.

### 2. Força de amortecimento

$$
F_d = -bv
\tag{2}
$$

onde $b > 0$ é o coeficiente de amortecimento e $v = dx/dt$.

### 3. Força externa periódica

$$
F_{\mathrm{ext}} = F_0 \cos(\omega t)
\tag{3}
$$

onde $F_0$ é a amplitude e $\omega$ a frequência angular da excitação externa.

## Equação de movimento

A equação de movimento do sistema é:

$$
m\frac{d^2x}{dt^2} = -kx - \alpha x^3 - b\frac{dx}{dt} + F_0\cos(\omega t)
\tag{4}
$$

Definindo $v = dx/dt$, obtém-se o sistema de primeira ordem:

$$
\frac{dx}{dt} = v
\tag{5}
$$

$$
\frac{dv}{dt}
= -\frac{k}{m}x - \frac{\alpha}{m}x^3 - \frac{b}{m}v + \frac{F_0}{m}\cos(\omega t)
\tag{6}
$$

## Potencial efetivo

A parte conservativa do sistema pode ser associada ao potencial:

$$
U(x) = \frac{1}{2}kx^2 + \frac{1}{4}\alpha x^4
\tag{7}
$$

A análise deste potencial será importante para interpretar os efeitos da não linearidade.

## Questões

1. Discretize as equações de movimento utilizando o método de Euler com passo temporal $\Delta t$. Apresente explicitamente as expressões para $x_{n+1}$ e $v_{n+1}$.

2. Faça uma análise gráfica do potencial efetivo $U(x)$ para diferentes valores de $\alpha$. Discuta como a não linearidade modifica a forma do potencial.

3. Implemente o método numérico escolhido para a integração das equações de movimento em uma linguagem de programação de sua escolha e obtenha numericamente as soluções $x(t)$ e $v(t)$, bem como o retrato de fase $v \times x$. Discuta o comportamento físico observado.

4. Considere inicialmente o caso sem força externa ($F_0 = 0$). Analise como diferentes valores do coeficiente de amortecimento $b$ influenciam:

   - a amplitude das oscilações;
   - o decaimento temporal;
   - o retrato de fase.

5. Compare os resultados obtidos para:

   - $\alpha = 0$ (oscilador harmônico linear);
   - $\alpha \neq 0$ (oscilador não linear).

   Discuta quais características do movimento são exclusivamente devidas à não linearidade.

6. Defina a energia mecânica do sistema como:

   $$
   E(t) = \frac{1}{2}mv^2 + \frac{1}{2}kx^2 + \frac{1}{4}\alpha x^4
   \tag{8}
   $$

   Para o caso sem força externa ($F_0 = 0$), analise numericamente a evolução temporal da energia para diferentes valores do coeficiente de amortecimento $b$. Discuta:

   - a taxa de dissipação de energia;
   - o papel da não linearidade na dinâmica energética;
   - a relação entre energia e trajetória no espaço de fase.

7. Considere agora o caso com força externa periódica ($F_0 \neq 0$). Analise a resposta do sistema para diferentes valores de $\omega$, discutindo:

   - o comportamento transiente;
   - o regime estacionário;
   - a ocorrência de ressonância.

8. Compare os resultados obtidos para o sistema forçado nos casos:

   - $\alpha = 0$ (oscilador linear forçado);
   - $\alpha \neq 0$ (oscilador não linear forçado).

   Analise como a não linearidade modifica:

   - a amplitude das oscilações;
   - o comportamento temporal;
   - o retrato de fase;
   - a resposta na região de ressonância.

9. Para o caso com força externa periódica ($F_0 \neq 0$), analise a evolução temporal da energia mecânica. Discuta:

   - o balanço entre energia injetada e energia dissipada;
   - a existência de um regime estacionário dinâmico;
   - a dependência desse regime com a frequência $\omega$;
   - a relação entre energia e ressonância.

## Observações

- Não se espera solução analítica fechada; o uso de métodos numéricos é fundamental. Embora o método de Euler seja suficiente para a discretização inicial, os estudantes podem utilizar métodos mais precisos e estáveis, como o método de Runge-Kutta de quarta ordem (RK4), para comparação de resultados.
- O foco principal do projeto é a análise física e computacional do sistema.
- Recomenda-se o uso de gráficos para comparação entre diferentes regimes e parâmetros.
- Para o caso com força externa periódica, a análise energética pode ser enriquecida através do conceito de potência instantânea associada às forças não conservativas do sistema.

A potência fornecida pela força externa (energia injetada no sistema) é dada por:

$$
P_{\mathrm{ext}}(t) = F_0 \cos(\omega t)\, v(t)
\tag{9}
$$

A potência dissipada pelo amortecimento (energia removida do sistema) é:

$$
P_{\mathrm{diss}}(t) = -b v^2(t)
\tag{10}
$$

Essas expressões podem ser utilizadas para uma interpretação qualitativa do balanço energético do sistema, especialmente na análise do regime estacionário e do fenômeno de ressonância.

- A interpretação física dos resultados é parte essencial da avaliação.
- O projeto é individual. O uso de ferramentas externas, incluindo inteligência artificial, deve ser declarado de forma transparente.
- A apresentação dos resultados deve ser clara, organizada e coerente.
- O relatório final deve ser entregue em PDF. Sugere-se o uso de LaTeX, embora outros editores também sejam aceitos.
