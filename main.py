# Made by Korzeremi02

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
    inBed = int(input("Heure de coucher (18-23) ? > "))
    outBed = int(input("Heure de levée (0-12) ? > "))
    if outBed < inBed:
        currentNightDuration = (24 - inBed) + outBed
    else:
        currentNightDuration = outBed - inBed
    print(f"Durée de votre nuit > {currentNightDuration}")
    savedSleepDurations.append(currentNightDuration)

def calculateSleepDebt(recommendedDuration, savedSleepDurations):
    totalDebt = 0
    index = 0
    lastNightDuration = savedSleepDurations[-1] if savedSleepDurations else 0
    if lastNightDuration < recommendedDuration:
        print(f"{lastNightDuration}h était votre dernière durée de sommeil. Vous n'avez pas atteint l'objectif recommandé.")
    else:
        print(f"{lastNightDuration}h était votre dernière durée de sommeil. Vous avez atteint l'objectif recommandé.")
    print(f"Durée de sommeil recommandée > {recommendedDuration}")
    for savedSleepDuration in savedSleepDurations:
        dailyDebt = recommendedDuration - savedSleepDuration
        totalDebt += dailyDebt
        index += 1
        print(f"Calcul de la dette de sommeil sur les nuits 1..{index} > {totalDebt} heures de sommeil à rattraper")
    return totalDebt

recommendedDuration, age = setUserProfile()
setCurrentNightData(savedSleepDurations)
debtResult = calculateSleepDebt(recommendedDuration, savedSleepDurations)
print(f"Dette de sommeil à rattraper : {debtResult} heures de sommeil")
