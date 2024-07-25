function Is-PyInstallerInstalled {
    try {
        # Vérifier si la commande pyinstaller est disponible
        $pyInstallerVersion = pyinstaller --version 2>$null
        return $pyInstallerVersion -ne $null
    } catch {
        return $false
    }
}
if (-not (Is-PyInstallerInstalled)) {
    Write-Output "PyInstaller n'est pas installé. Installation en cours..."
    pip install pyinstaller
} else {
    Write-Output "PyInstaller est déjà installé."
}
Write-Output "Création du fichier exécutable avec PyInstaller..."
pyinstaller --onefile --windowed --name nightpilot .\main.py
Write-Output "Création du fichier exécutable terminée."
