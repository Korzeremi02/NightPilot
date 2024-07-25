import matplotlib.pyplot as plt
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

def setUserProfile(existing_data=None):
    if existing_data:
        age = existing_data['age']
        name = existing_data['name']
        recommendedDuration = existing_data['recommendedDuration']
        savedSleepDurations = existing_data['savedSleepDurations']
        dates = existing_data['dates']
        print(f"Les données existantes : \nNom : {name}\nÂge : {age}\nObjectif recommandé : {recommendedDuration}h")
        return recommendedDuration, age, name, savedSleepDurations, dates
    else:
        print('\n' * 1000)
        age = float(input("Âge (0/120) ? > "))
        name = input("Nom ? > ")
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
        print('\n' * 1000)
        preferenceMsg = input(f"{name}, Une marge peut être mise en place si vous souhaitez avoir un objectif plus haut ou plus bas que la norme pour votre âge. Actuellement l'objectif est de {recommendedDuration}h. Appliquer une marge ? (o/n) > ")
        if preferenceMsg == 'n':
            saveData(recommendedDuration, age, name, [], [])
            return recommendedDuration, age, name, [], []
        preference = input("Objectif plus haut ou plus bas ? (h/b) > ")
        if preference == 'h':
            recommendedDuration += 1
            print(f"Objectif augmenté à {recommendedDuration}h.")
        elif preference == 'b':
            recommendedDuration -= 1
            print(f"Objectif diminué à {recommendedDuration}h.")
        saveData(recommendedDuration, age, name, [], [])
        return recommendedDuration, age, name, [], []

def setCurrentNightData(savedSleepDurations, dates):
    print('\n' * 1000)
    inBed = int(input("Heure de coucher (0-23) ? > "))
    outBed = int(input("Heure de levée (0-23) ? > "))
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
    print('\n' * 1000)
    totalDebt = 0
    lastNightDuration = savedSleepDurations[-1] if savedSleepDurations else 0
    if lastNightDuration < recommendedDuration:
        print(f"{lastNightDuration}h était votre dernière durée de sommeil. Vous n'avez pas atteint l'objectif journalier recommandé ({recommendedDuration}h). Veillez à être plus régulier dans vos nuits.")
    else:
        print(f"{lastNightDuration}h était votre dernière durée de sommeil. Vous avez atteint l'objectif recommandé ({recommendedDuration}h). Continuez à être régulier dans vos nuits !")
    for savedSleepDuration in savedSleepDurations:
        dailyDebt = recommendedDuration - savedSleepDuration
        totalDebt += dailyDebt
    return totalDebt

def showNightsCharts(savedSleepDurations, dates, recommendedDuration, age, name):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, savedSleepDurations, label='Durée de sommeil', marker='o')
    plt.plot(dates, [recommendedDuration] * len(dates), label='Objectif recommandé', linestyle='--')
    debt = [recommendedDuration - duration for duration in savedSleepDurations]
    plt.plot(dates, debt, label='Dette de sommeil', linestyle='--', color='red')
    plt.xlabel('Date')
    plt.ylabel('Heures')
    plt.title(f"Données de sommeil pour {name} ({int(age)} ans)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

existing_data = loadData()
recommendedDuration, age, name, savedSleepDurations, dates = setUserProfile(existing_data)
setCurrentNightData(savedSleepDurations, dates)
debtResult = calculateSleepDebt(recommendedDuration, savedSleepDurations)
showNightsCharts(savedSleepDurations, dates, recommendedDuration, age, name)
print(f"Dette de sommeil à rattraper : {debtResult} heures de sommeil\n(La dette de sommeil est un indicateur et ne doit pas être appliquée. Il est important de dormir suffisamment pour être en forme et de respecter les recommandations médicales.)")
