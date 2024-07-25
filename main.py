# Made by Korzeremi02
import matplotlib.pyplot as plt

savedSleepDurations = [8, 2, 5, 6, 10]

def setUserProfile():
    age = float(input("Âge (0/120) ? > "))
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
    for (minAge, maxAge), recommendedDuration in ageArray.items():
        if minAge <= age <= maxAge:
            return recommendedDuration, age
    return 0, age

def setCurrentNightData(savedSleepDurations):
    inBed = int(input("Heure de coucher (0-23) ? > "))
    outBed = int(input("Heure de levée (0-23) ? > "))
    if outBed < inBed:
        currentNightDuration = (24 - inBed) + outBed
    else:
        currentNightDuration = outBed - inBed
    savedSleepDurations.append(currentNightDuration)

def calculateSleepDebt(recommendedDuration, savedSleepDurations):
    totalDebt = 0
    index = 0
    lastNightDuration = savedSleepDurations[-1] if savedSleepDurations else 0
    if lastNightDuration < recommendedDuration:
        print(f"{lastNightDuration}h était votre dernière durée de sommeil. Vous n'avez pas atteint l'objectif recommandé ({recommendedDuration}h).")
    else:
        print(f"{lastNightDuration}h était votre dernière durée de sommeil. Vous avez atteint l'objectif recommandé ({recommendedDuration}h).")
    for savedSleepDuration in savedSleepDurations:
        dailyDebt = recommendedDuration - savedSleepDuration
        totalDebt += dailyDebt
        index += 1
    return totalDebt

def plotSleepData(savedSleepDurations, recommendedDuration):
    nights = list(range(1, len(savedSleepDurations) + 1))
    debt = [recommendedDuration - duration for duration in savedSleepDurations]

    plt.figure(figsize=(10, 5))
    plt.plot(nights, savedSleepDurations, label='Durée de sommeil')
    plt.plot(nights, [recommendedDuration] * len(nights), label='Objectif recommandé', linestyle='--')
    plt.plot(nights, [d for d in debt], label='Dette de sommeil')
    plt.xlabel('Nuit')
    plt.ylabel('Heures')
    plt.title('Données de sommeil et Dette de sommeil')
    plt.legend()
    plt.show()

recommendedDuration, age = setUserProfile()
setCurrentNightData(savedSleepDurations)
debtResult = calculateSleepDebt(recommendedDuration, savedSleepDurations)
plotSleepData(savedSleepDurations, recommendedDuration)
print(f"Dette de sommeil à rattraper : {debtResult} heures de sommeil")
