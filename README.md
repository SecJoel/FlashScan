# ⚡ FlashScan

Hola Buenass. Les traigo **FlashScan**, una herramienta que diseñé para los que queremos **ir mas rápido en un CTF o auditoria** en una auditoría. Estaba cansado de tirar comandos sueltos de Nmap, buscar subdominios por un lado y hacer fuzzing por otro, así que automaticé todo el flujo en este framework.

Es una herramienta que te ayuda a no perder tiempo y enfocarte en lo que importa: encontrar el vector de entrada.

---

## 🚀 ¿Qué hace esta herramienta?

El flujo está pensado para que un **usuario o hacker** tenga el control total de lo que pasa, pero sin el desorden de la terminal:

1.  **Recon Pasivo:** Si le pasas un dominio, te busca subdominios activos con `subfinder` antes de empezar.
2.  **Identificación de OS:** Te dice si el objetivo es Linux o Windows analizando el TTL (ping).
3.  **Escaneo de Puertos:** Barrido rápido de los 65,535 puertos para localizar dónde hay acción.
4.  **Análisis Detallado:** Te resume qué servicios y versiones corren, sin el "vómito" de texto de Nmap.
5.  **Auditoría de CVEs:** Busca fallos críticos conocidos. Si sale algo, ya sabes: **"Sistema vulnerado"**.
6.  **Fuzzing Web:** Si hay puertos web, lanza `ffuf` en segundo plano para buscar directorios ocultos.

---

## 🛠️ Instalación rápida

Para que no tengas que estar lidiando con `python3`, te dejé un instalador que configura todo como un comando nativo del sistema.

```bash
# Clona el repo
git clone [https://github.com/TU-USUARIO/FlashScan.git](https://github.com/TU-USUARIO/FlashScan.git)
cd FlashScan

# Instala la herramienta en el sistema
chmod +x install.sh
./install.sh

# ⚡ FlashScan

Hola Buenass. Here is **FlashScan**, a tool I designed for those of us who want to **get straight to the point** during an audit. I was tired of running separate Nmap commands, hunting subdomains on one side and fuzzing on the other, so I automated the whole workflow into this framework.

It’s a tool that helps you save time and focus on what really matters: finding the entry vector.

---

## 🚀 What does this tool do?

The workflow is designed so that any **user or hacker** has total control over what’s happening without the terminal mess:

1.  **Passive Recon:** If you provide a domain, it hunts for active subdomains using `subfinder` before starting.
2.  **OS Identification:** It tells you if the target is Linux or Windows by analyzing the TTL (ping).
3.  **Port Scanning:** A fast sweep of all 65,535 ports to locate where the action is.
4.  **Detailed Analysis:** It summarizes the services and versions running, without the Nmap text "vomit."
5.  **CVE Auditing:** Searches for known critical vulnerabilities. If it finds something, you know the drill: **"Sistema vulnerado"** (System compromised).
6.  **Web Fuzzing:** If web ports are open, it launches `ffuf` in the background to find hidden directories.

---

## 🛠️ Quick Installation

To avoid dealing with `python3` every time, I've included an installer that sets everything up as a native system command.

```bash
# Clone the repo
git clone [https://github.com/YOUR-USER/FlashScan.git](https://github.com/YOUR-USER/FlashScan.git)
cd FlashScan

# Install the tool globally
chmod +x install.sh
./install.sh
