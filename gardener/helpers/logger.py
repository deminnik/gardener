"""logger.py
Gardener - plugin for QGIS
Copyright (C) 2020  Nikita Demin
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
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
