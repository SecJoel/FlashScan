#!/bin/bash

# Colores para que se vea bien en Kali
GREEN="\033[1;32m"
BLUE="\033[1;34m"
RED="\033[1;31m"
RESET="\033[0m"

echo -e "${BLUE}[*] Instalando FlashScan: Professional Edition...${RESET}"

# 1. Chequeamos que el script de python esté en esta misma carpeta
if [ ! -f "flashscan.py" ]; then
    echo -e "${RED}[!] Error: No se encuentra flashscan.py en esta carpeta.${RESET}"
    exit 1
fi

# 2. Darle permisos de ejecución al script
chmod +x flashscan.py

# 3. Copiarlo a la carpeta de binarios del sistema (renombrándolo a 'flashscan')
# Usamos sudo porque /usr/local/bin es una carpeta protegida
echo -e "${BLUE}[*] Moviendo script a /usr/local/bin/flashscan...${RESET}"
sudo cp flashscan.py /usr/local/bin/flashscan

# 4. Finalización
if [ -f "/usr/local/bin/flashscan" ]; then
    echo -e "${GREEN}[✓] ¡Instalación completada!${RESET}"
    echo -e "${YELLOW}[i] Ahora puedes usarlo escribiendo: ${BOLD}${GREEN}flashscan <objetivo>${RESET}"
else
    echo -e "${RED}[!] Hubo un error en la copia. Inténtalo de nuevo con sudo.${RESET}"
fi
