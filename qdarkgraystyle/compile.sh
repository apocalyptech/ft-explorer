#!/bin/bash
# vim: set expandtab tabstop=4 shiftwidth=4:

pyrcc4 -py3 style.qrc -o pyqt_style_rc.py
pyrcc5 style.qrc -o pyqt5_style_rc.py
pyside-rcc -py3 style.qrc -o pyside_style_rc.py
