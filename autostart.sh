#!/bin/sh

#Configuracion de idioma de teclado
#setxkbmap es &

#Picom
picom --config ~/.config/picom/picom.conf &

#Nitrogen
nitrogen --restore &

#Crear archivo con los colores del wal
/bin/python3 /home/aadu/utils/conexion_wal-terminal/crear_json_colores_wal.py &

#XScreenSaver
xscreensaver &

#Iconos de sistema
udiskie -t &
nm-applet &
