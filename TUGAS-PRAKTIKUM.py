import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kipas = ctrl.Consequent(np.arange(0, 101, 1), 'kipas')

suhu['Dingin'] = fuzz.trimf(suhu.universe, [0, 0, 20])
suhu['Sedang'] = fuzz.trimf(suhu.universe, [10, 20, 30])
suhu['Panas'] = fuzz.trimf(suhu.universe, [20, 40, 40])

kelembapan['Kering'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['Normal'] = fuzz.trimf(kelembapan.universe, [25, 50, 75])
kelembapan['Basah'] = fuzz.trimf(kelembapan.universe, [50, 100, 100])

kipas['Pelan'] = fuzz.trimf(kipas.universe, [0, 0, 50])
kipas['Sedang'] = fuzz.trimf(kipas.universe, [25, 50, 75])
kipas['Cepat'] = fuzz.trimf(kipas.universe, [50, 100, 100])

aturan1 = ctrl.Rule(suhu['Dingin'] & kelembapan['Basah'], kipas['Pelan'])
aturan2 = ctrl.Rule(suhu['Sedang'], kipas['Sedang'])
aturan3 = ctrl.Rule(suhu['Panas'] | kelembapan['Kering'], kipas['Cepat'])

engine = ctrl.ControlSystem([aturan1, aturan2, aturan3])
system = ctrl.ControlSystemSimulation(engine)

system.input['suhu'] = 32
system.input['kelembapan'] = 40
system.compute()
hasil_kipas = system.output['kipas']
print(f"Kecepatan Putaran Kipas Adalah: {hasil_kipas:.2f}")
kipas.view(sim=system)
input("TEKAN ENTER untuk melanjutkan")
