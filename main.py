import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
import os
from datetime import datetime

SAVE_FILE = 'saveData.pkl'

def saveData(recommendedDuration, age, name, savedSleepDurations, dates):
    with open(SAVE_FILE, 'wb') as file:
        data = {
            'recommendedDuration': recommendedDuration,
            'age': age,
            'name': name,
            'savedSleepDurations': savedSleepDurations,
            'dates': dates
        }
        pickle.dump(data, file)


def loadData():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'rb') as file:
            return pickle.load(file)
    return None


def setUserProfile():
    existing_data = loadData()
    if existing_data:
        return existing_data['recommendedDuration'], existing_data['age'], existing_data['name'], existing_data[
            'savedSleepDurations'], existing_data['dates']
    else:
        age = simpledialog.askfloat("Âge", "Âge (0/120) ?")
        name = simpledialog.askstring("Nom", "Nom ?")
        ageArray = {
            (0, 0.2): 15,
            (0.3, 0.9): 13,
            (1, 2): 12,
            (3, 5): 11,
            (6, 13): 10,
            (14, 17): 9,
            (18, 64): 8,
            (65, float('inf')): 7
        }
        recommendedDuration = 0
        for (minAge, maxAge), duration in ageArray.items():
            if minAge <= age <= maxAge:
                recommendedDuration = duration
                break
        preferenceMsg = messagebox.askyesno("Préférence",
                                            f"{name}, Une marge peut être mise en place si vous souhaitez avoir un objectif plus haut ou plus bas que la norme pour votre âge. Actuellement l'objectif est de {recommendedDuration}h. Appliquer une marge ?")
        if preferenceMsg:
            preference = simpledialog.askstring("Préférence", "Objectif plus haut ou plus bas ? (h/b)")
            if preference == 'h':
                recommendedDuration += 1
            elif preference == 'b':
                recommendedDuration -= 1
        saveData(recommendedDuration, age, name, [], [])
        return recommendedDuration, age, name, [], []


def setCurrentNightData(savedSleepDurations, dates):
    inBed = simpledialog.askinteger("Heure de coucher", "Heure de coucher (0-23) ?")
    outBed = simpledialog.askinteger("Heure de levée", "Heure de levée (0-23) ?")
    if outBed < inBed:
        currentNightDuration = (24 - inBed) + outBed
    else:
        currentNightDuration = outBed - inBed
    savedSleepDurations.append(currentNightDuration)
    dates.append(datetime.now().strftime("%Y-%m-%d"))
    existing_data = loadData()
    if existing_data:
        recommendedDuration = existing_data['recommendedDuration']
        age = existing_data['age']
        name = existing_data['name']
        saveData(recommendedDuration, age, name, savedSleepDurations, dates)

def calculateSleepDebt(recommendedDuration, savedSleepDurations):
    totalDebt = 0
    lastNightDuration = savedSleepDurations[-1] if savedSleepDurations else 0
    if lastNightDuration < recommendedDuration:
        message = f"{lastNightDuration}h était votre dernière durée de sommeil. Vous n'avez pas atteint l'objectif journalier recommandé ({recommendedDuration}h)."
    else:
        message = f"{lastNightDuration}h était votre dernière durée de sommeil. Vous avez atteint l'objectif recommandé ({recommendedDuration}h)."
    for savedSleepDuration in savedSleepDurations:
        dailyDebt = recommendedDuration - savedSleepDuration
        totalDebt += dailyDebt
    return totalDebt, message

def showNightsCharts(savedSleepDurations, dates, recommendedDuration, age, name):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, savedSleepDurations, label='Durée de sommeil', marker='o')
    ax.plot(dates, [recommendedDuration] * len(dates), label='Objectif recommandé', linestyle='--')
    debt = [recommendedDuration - duration for duration in savedSleepDurations]
    ax.plot(dates, debt, label='Dette de sommeil', linestyle='--', color='red')
    ax.set_xlabel('Date')
    ax.set_ylabel('Heures')
    ax.set_title(f"Données de sommeil pour {name} ({int(age)} ans)")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

class SleepTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sleep Tracker")
        self.recommendedDuration, self.age, self.name, self.savedSleepDurations, self.dates = setUserProfile()
        self.setupUI()

    def setupUI(self):
        self.label = tk.Label(self.root,
                              text=f"Bonjour {self.name}, votre objectif de sommeil est de {self.recommendedDuration} heures par nuit.")
        self.label.pack(pady=10)

        self.addDataButton = tk.Button(self.root, text="Ajouter Données de Sommeil pour aujourd'hui", command=self.addData)
        self.addDataButton.pack(pady=5)

        self.showChartButton = tk.Button(self.root, text="Afficher Graphique", command=self.showChart)
        self.showChartButton.pack(pady=5)

        self.quitButton = tk.Button(self.root, text="Quitter", command=self.root.quit)
        self.quitButton.pack(pady=5)

    def addData(self):
        setCurrentNightData(self.savedSleepDurations, self.dates)
        debtResult, message = calculateSleepDebt(self.recommendedDuration, self.savedSleepDurations)
        messagebox.showinfo("Dette de Sommeil",
                            f"Dette de sommeil à rattraper : {debtResult} heures de sommeil\n{message}")

    def showChart(self):
        fig = showNightsCharts(self.savedSleepDurations, self.dates, self.recommendedDuration, self.age, self.name)
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Graphique de Sommeil")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = SleepTrackerApp(root)
    root.mainloop()
