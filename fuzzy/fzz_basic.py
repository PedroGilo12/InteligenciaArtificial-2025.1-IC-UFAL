import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definição das variáveis
temperatura = ctrl.Antecedent(np.arange(0, 101, 1), 'temperatura')
fluxo = ctrl.Antecedent(np.arange(0, 21, 1), 'fluxo')
abertura = ctrl.Consequent(np.arange(0, 101, 1), 'abertura')

# Funções de pertinência
temperatura['baixa'] = fuzz.trimf(temperatura.universe, [0, 0, 50])
temperatura['media'] = fuzz.trimf(temperatura.universe, [25, 50, 75])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [50, 100, 100])

fluxo['baixo'] = fuzz.trimf(fluxo.universe, [0, 0, 10])
fluxo['medio'] = fuzz.trimf(fluxo.universe, [5, 10, 15])
fluxo['alto'] = fuzz.trimf(fluxo.universe, [10, 20, 20])

abertura['pequena'] = fuzz.trimf(abertura.universe, [0, 0, 50])
abertura['moderada'] = fuzz.trimf(abertura.universe, [25, 50, 75])
abertura['grande'] = fuzz.trimf(abertura.universe, [50, 100, 100])

# Regras
regra1 = ctrl.Rule(temperatura['baixa'] & fluxo['alto'], abertura['grande'])
regra2 = ctrl.Rule(temperatura['baixa'] & fluxo['medio'], abertura['moderada'])
regra3 = ctrl.Rule(temperatura['media'] & fluxo['alto'], abertura['moderada'])
regra4 = ctrl.Rule(temperatura['media'] & fluxo['baixo'], abertura['pequena'])
regra5 = ctrl.Rule(temperatura['alta'] & fluxo['baixo'], abertura['pequena'])
regra6 = ctrl.Rule(temperatura['alta'] & fluxo['alto'], abertura['moderada'])

# Sistema de Controle
sistema_abertura = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
simulador = ctrl.ControlSystemSimulation(sistema_abertura)

# ==============================================================
# Simulação ao longo do tempo

# Criar vetores de temperatura e fluxo variando
tempo = np.linspace(0, 10, 100)  # 100 instantes de tempo de 0 a 10s

temperaturas = 30 + 10 * np.sin(0.5 * tempo)  # Temperatura variando com o tempo (tipo senoidal)
fluxos = 10 + 5 * np.cos(0.3 * tempo)          # Fluxo variando com o tempo (também senoidal)

aberturas = []  # Para armazenar a saída (abertura) em cada instante

for temp, flu in zip(temperaturas, fluxos):
    simulador.input['temperatura'] = temp
    simulador.input['fluxo'] = flu
    simulador.compute()
    aberturas.append(simulador.output['abertura'])

# ==============================================================
# Gráficos

plt.figure(figsize=(14, 8))

# Plotar temperatura
plt.subplot(3, 1, 1)
plt.plot(tempo, temperaturas, 'r-', label='Temperatura (°C)')
plt.ylabel('Temperatura (°C)')
plt.grid(True)
plt.legend()

# Plotar fluxo
plt.subplot(3, 1, 2)
plt.plot(tempo, fluxos, 'b-', label='Fluxo (L/min)')
plt.ylabel('Fluxo (L/min)')
plt.grid(True)
plt.legend()

# Plotar abertura
plt.subplot(3, 1, 3)
plt.plot(tempo, aberturas, 'g-', label='Abertura da Válvula (%)')
plt.xlabel('Tempo (s)')
plt.ylabel('Abertura (%)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
# ==============================================================
# Gráficos de pertinência - Temperatura
plt.figure(figsize=(10, 5))
plt.title('Funções de Pertinência - Temperatura')
plt.plot(temperatura.universe, temperatura['baixa'].mf, label='Baixa')
plt.plot(temperatura.universe, temperatura['media'].mf, label='Média')
plt.plot(temperatura.universe, temperatura['alta'].mf, label='Alta')
plt.xlabel('Temperatura (°C)')
plt.ylabel('Pertinência')
plt.legend()
plt.grid(True)
plt.show()

# Gráficos de pertinência - Fluxo
plt.figure(figsize=(10, 5))
plt.title('Funções de Pertinência - Fluxo de Água')
plt.plot(fluxo.universe, fluxo['baixo'].mf, label='Baixo')
plt.plot(fluxo.universe, fluxo['medio'].mf, label='Médio')
plt.plot(fluxo.universe, fluxo['alto'].mf, label='Alto')
plt.xlabel('Fluxo (L/min)')
plt.ylabel('Pertinência')
plt.legend()
plt.grid(True)
plt.show()
# ==============================================================

