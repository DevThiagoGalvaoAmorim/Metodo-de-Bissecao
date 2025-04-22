import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# Definição da função f(x)
def f(x):
    return x**3 - 3*x - 18  

# Criar pasta para salvar imagens
os.makedirs("images", exist_ok=True)

# Entrada do usuário
a = float(input("Digite o valor de a: "))
b = float(input("Digite o valor de b: "))
n = int(input("Digite n para tolerância ε < 10^-n: "))
epsilon = 10**(-n)

# Tabela de dados
dataTabela = {"n": [], "an": [], "bn": [], "xn": [], "f(xn)": [], "ε": []}

# Método da Bisseção
if f(a) * f(b) < 0:
    n = 0
    stop = abs(b - a)
    while stop > epsilon:
        xn = (a + b) / 2
        stop = abs(b - a)

        dataTabela["n"].append(n)
        dataTabela["an"].append(round(a, 5))
        dataTabela["bn"].append(round(b, 5))
        dataTabela["xn"].append(round(xn, 5))
        dataTabela["f(xn)"].append(round(f(xn), 5))
        dataTabela["ε"].append(round(stop, 5))

        if f(xn) == 0:
            msg = f"A raiz exata é {round(xn, 7)}"
            break
        elif f(a) * f(xn) < 0:
            b = xn
        else:
            a = xn

        n += 1
        msg = f"A raiz aproximada é {round(xn, 7)}"

    print(msg)
else:
    print("Não há raiz no intervalo.")
    msg = "Nenhuma iteração foi realizada."

# Criar gráfico
x_vals = np.linspace(a - 5, b + 5, 400)
y_vals = f(x_vals)
plt.plot(x_vals, y_vals, label="f(x) = x³ - 3x - 18")
plt.axhline(0, color='red', linewidth=0.5)
plt.axvline(0, color='red', linewidth=0.5)
plt.grid(True)
plt.legend()
plt.savefig("images/grafico.png")

# Verificar se há dados na tabela antes de criar a imagem
df = pd.DataFrame(dataTabela)

if not df.empty:
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.axis('off')
    tabela = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    tabela.scale(2, 1.2)
    plt.savefig("images/tabela.png")

    # Criar imagem final combinada
    output_img = Image.new("RGB", (2000, 1000), color="white")
    grafico = Image.open("images/grafico.png").resize((1000, 1000))
    tabela = Image.open("images/tabela.png").resize((1000, 500))
    output_img.paste(grafico, (0, 0))
    output_img.paste(tabela, (1000, 500))
    draw = ImageDraw.Draw(output_img)
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((1100, 100), "Método da Bisseção", font=font, fill="black")
    draw.text((1100, 300), msg, font=font, fill="black")
    output_img.save("images/output_image.png")
else:
    print("Nenhuma tabela foi gerada, pois não há dados suficientes.")
