from qgis.core import QgsMessageLog, Qgis

def say(message, kind):
    QgsMessageLog.logMessage(message, "Gardener", level=kind)

def info(message):
    say(message, Qgis.Info)

def error(message):
    say(message, Qgis.Critical)

def warning(message):
    say(message, Qgis.Warning)

def success(message):
    say(message, Qgis.Success)
