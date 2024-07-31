import requests
import re

class CalculadoraRest:
    def __init__(self, base_url):
        self.base_url = base_url

    def operacao(self, op, param1, param2):
        url = f"{self.base_url}/{op}/{param1}/{param2}"
        response = requests.post(url)
        if response.status_code == 200:
            return response.json().get('result')
        else:
            return f"Erro: {response.status_code}, {response.text}"

    def soma(self, param1, param2):
        return self.operacao("soma", param1, param2)

    def subtracao(self, param1, param2):
        return self.operacao("subtracao", param1, param2)

    def multiplicacao(self, param1, param2):
        return self.operacao("multiplicacao", param1, param2)

    def divisao(self, param1, param2):
        return self.operacao("divisao", param1, param2)


## if __name__ == "__main__":
##    calculadora = CalculadoraRest("https://calculadora-fxpc.onrender.com/operation")

    # Exemplo de uso:
##    print("Soma: 10 + 5 =", calculadora.soma(10, 5))

import tkinter as tk
from tkinter import messagebox

def click(event):
    global expression
    expression += event.widget.cget("text")
    equation.set(expression)

def clear():
    global expression
    expression = ""
    equation.set(expression)

def separate_operators_numbers(expression):
    # Use regex to find all numbers and operators
    tokens = re.findall(r'\d+\.\d+|\d+|[+-/*//()]', expression)
    return tokens

def find_indices(lst, value):
    return [i for i, x in enumerate(lst) if x == value]

def evaluate():
    global expression

    calculadora = CalculadoraRest("https://calculadora-fxpc.onrender.com/operation")
    try:
        # 2 * 6 + 99 / 8 * 6 - 4
        tokens = separate_operators_numbers(expression)

        # Multiplicação e Divisão
        idx = 0
        for i in tokens:
            if i == '*':
                tokens[idx+1] = calculadora.multiplicacao(float(tokens[idx-1]), float(tokens[idx+1]))
                tokens[idx] = None
                tokens[idx-1] = None

            if i == '/':
                tokens[idx+1] = calculadora.divisao(float(tokens[idx-1]), float(tokens[idx+1]))
                tokens[idx] = None
                tokens[idx-1] = None

            idx += 1

        tokens = list(filter(lambda x: x is not None, tokens))

        # Soma e Subtração
        idx = 0
        for i in tokens:
            if i == '+':
                tokens[idx+1] = calculadora.soma(float(tokens[idx-1]), float(tokens[idx+1]))
                tokens[idx] = None
                tokens[idx-1] = None

            if i == '-':
                tokens[idx+1] = calculadora.subtracao(float(tokens[idx-1]), float(tokens[idx+1]))
                tokens[idx] = None
                tokens[idx-1] = None

            idx += 1

        tokens = list(filter(lambda x: x is not None, tokens))

        # result = str(eval(expression))
        result = str(tokens[0])
        equation.set(result)
        expression = result
    except Exception as e:
        messagebox.showerror("Error", "Invalid Input")
        expression = ""

# Criar janela
root = tk.Tk()
root.title("Calculator")

# Variaveis para guardar entrada e saida
equation = tk.StringVar()
expression = ""

# Visor para mostrar a opeção atual
input_field = tk.Entry(root, textvariable=equation, font=('arial', 20, 'bold'), bd=10, insertwidth=4, width=14, borderwidth=4)
input_field.grid(row=0, column=0, columnspan=4)

# cria botões
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

# Adiciona botões a janela
row_val = 1
col_val = 0
for button in buttons:
    if button == 'C':
        btn = tk.Button(root, text=button, padx=20, pady=20, font=('arial', 20, 'bold'), command=clear)
    elif button == '=':
        btn = tk.Button(root, text=button, padx=20, pady=20, font=('arial', 20, 'bold'), command=evaluate)
    else:
        btn = tk.Button(root, text=button, padx=20, pady=20, font=('arial', 20, 'bold'))
        btn.bind("<Button-1>", click)

    btn.grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

if __name__ == "__main__":
    # Pegar operações
    response = requests.get("https://calculadora-fxpc.onrender.com/operations")
    print(response.json())

    # Roda o loop principal
    root.mainloop()