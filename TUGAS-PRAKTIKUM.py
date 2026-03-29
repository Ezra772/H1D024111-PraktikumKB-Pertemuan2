import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Menyiapkan Variabel Ruang Lingkup (Universe)
# Suhu (0-40), Kelembapan (0-100), Kipas (0-100)
suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')
kipas = ctrl.Consequent(np.arange(0, 101, 1), 'kipas')

# 2. Membuat Minimal 3 Himpunan Fuzzy untuk Setiap Variabel (Membership Functions)

# Himpunan untuk Variabel Suhu: Dingin, Sedang, Panas
suhu['Dingin'] = fuzz.trimf(suhu.universe, [0, 0, 20])
suhu['Sedang'] = fuzz.trimf(suhu.universe, [10, 20, 30])
suhu['Panas'] = fuzz.trimf(suhu.universe, [20, 40, 40])

# Himpunan untuk Variabel Kelembapan: Kering, Normal, Basah
kelembapan['Kering'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['Normal'] = fuzz.trimf(kelembapan.universe, [25, 50, 75])
kelembapan['Basah'] = fuzz.trimf(kelembapan.universe, [50, 100, 100])

# Himpunan untuk Variabel Kipas: Pelan, Sedang, Cepat
kipas['Pelan'] = fuzz.trimf(kipas.universe, [0, 0, 50])
kipas['Sedang'] = fuzz.trimf(kipas.universe, [25, 50, 75])
kipas['Cepat'] = fuzz.trimf(kipas.universe, [50, 100, 100])

# 3. Membuat Minimal 3 Aturan Fuzzy (Fuzzy Rules)
# Aturan 1: JIKA suhu dingin DAN kelembapan basah, MAKA kipas pelan (karena cuaca sudah sangat lembap sejuk)
aturan1 = ctrl.Rule(suhu['Dingin'] & kelembapan['Basah'], kipas['Pelan'])

# Aturan 2: JIKA suhu sedang, MAKA kipas sedang (untuk mempertahankan kondisi ruangan)
aturan2 = ctrl.Rule(suhu['Sedang'], kipas['Sedang'])

# Aturan 3: JIKA suhu panas ATAU kelembapan kering, MAKA kipas cepat (agar ruangan cepat sejuk / udara tersirkulasi)
aturan3 = ctrl.Rule(suhu['Panas'] | kelembapan['Kering'], kipas['Cepat'])

# 4. Membangun Control System dan Engine Simulasi
mesin_fuzzy = ctrl.ControlSystem([aturan1, aturan2, aturan3])
sistem_kipas = ctrl.ControlSystemSimulation(mesin_fuzzy)

# 5. Menguji Input (Contoh: Suhu di 32°C dan Kelembapan ruangan 40%)
sistem_kipas.input['suhu'] = 32
sistem_kipas.input['kelembapan'] = 40

# Memerintahkan sistem untuk menghitung hasilnya
sistem_kipas.compute()

# 6. Menampilkan Hasil Output di Terminal dan Grafik
hasil_kipas = sistem_kipas.output['kipas']
print(f"Berdasarkan Suhu (32) dan Kelembapan (40), kecepatan putaran kipas adalah: {hasil_kipas:.2f}")

# Menampilkan grafik arsiran hasil keputusan dari kipas
kipas.view(sim=sistem_kipas)
input("TEKAN ENTER untuk menutup grafik dan melanjutkan...")
