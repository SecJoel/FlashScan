#!/usr/bin/env python3
import subprocess
import re
import sys
import datetime
import os
import time
import select

# ANSI Colors & Formatting
GREEN, RED, BLUE, YELLOW, CYAN, RESET = "\033[1;32m", "\033[1;31m", "\033[1;34m", "\033[1;33m", "\033[1;36m", "\033[0m"
BOLD = "\033[1m"

# LOGO: FlashScan (F and S uppercase, no version)
LOGO = rf"""{CYAN}
  ███████╗██╗      █████╗ ███████╗██╗  ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
  ██╔════╝██║     ██╔══██╗██╔════╝██║  ██║██╔════╝██╔════╝██╔══██╗████╗  ██║
  █████╗  ██║     ███████║███████╗███████║███████╗██║     ███████║██╔██╗ ██║
  ██╔══╝  ██║     ██╔══██║╚════██║██╔══██║╚════██║██║     ██╔══██║██║╚██╗██║
  ██║     ███████╗██║  ██║███████║██║  ██║███████║╚██████╗██║  ██║██║ ╚████║
  ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

 {YELLOW}[+] PORT SCANNING | PASSIVE RECON | CVE ANALYSIS | WEB FUZZING
{CYAN}-----------------------------------------------------------------------------------{RESET}
"""

def mostrar_manual():
    """Manual in Spanish and English"""
    manual_es = f"""
{BOLD}NOMBRE{RESET}
       flashscan - Herramienta integral de reconocimiento y auditoría.

{BOLD}DESCRIPCIÓN{RESET}
       Framework para automatizar fases de pentesting.
       Uso: sudo flashscan [OBJETIVO]

{BOLD}EJEMPLOS{RESET}
       sudo flashscan 10.10.10.15
       sudo flashscan google.com
    """
    
    manual_en = f"""
{BOLD}NAME{RESET}
       flashscan - Comprehensive reconnaissance and auditing tool.

{BOLD}SYNOPSIS{RESET}
       sudo flashscan [TARGET]
       flashscan man

{BOLD}DESCRIPTION{RESET}
       {BOLD}FlashScan{RESET} is a penetration testing automation framework.
       
       {BOLD}Phase 0: Passive Recon{RESET} (Subdomain mapping via Subfinder).
       {BOLD}OS Identification:{RESET} Detects OS via ICMP TTL values.
       {BOLD}Phase 1: Port Scan:{RESET} Fast TCP port discovery (0-65535).
       {BOLD}Phase 2: Service Enumeration:{RESET} Identifies versions and banners.
       {BOLD}Phase 3: CVE Audit:{RESET} Searches for critical known vulnerabilities.
       {BOLD}Phase 4: Web Fuzzing:{RESET} Background directory brute-forcing via FFUF.

{BOLD}EXAMPLES{RESET}
       sudo flashscan 192.168.1.1
       flashscan mytarget.com
    """
    print(f"{CYAN}--- MANUAL EN ESPAÑOL ---{RESET}{manual_es}")
    print(f"\n{CYAN}--- ENGLISH MANUAL ---{RESET}{manual_en}")

def verificar_entorno():
    tools = ["nmap", "subfinder", "ffuf"]
    return [t for t in tools if subprocess.run(f"command -v {t}", shell=True, capture_output=True).returncode != 0]

def log_to_file(content, filename):
    clean = re.sub(r'\x1b\[[0-9;]*m', '', content)
    with open(filename, "a", encoding="utf-8") as f:
        f.write(clean + "\n")

def parse_nmap_output(output):
    lines = re.findall(r"(\d+)/tcp\s+open\s+([^\s]+)\s+(.*)", output)
    return [f"{CYAN}  -> Port {p}:{RESET} Service {YELLOW}{s}{RESET} | Version: {GREEN}{v.strip()}{RESET}" for p, s, v in lines]

def get_os_by_ttl(target):
    print(f"{BLUE}[*] Executing: {CYAN}ping -c 1 {target}{RESET}")
    try:
        p = subprocess.run(["ping", "-c", "1", target], capture_output=True, text=True, timeout=3)
        ttl = re.search(r"ttl=(\d+)", p.stdout.lower())
        if ttl:
            v = int(ttl.group(1))
            return f"Linux (TTL: {v})" if v <= 64 else f"Windows (TTL: {v})"
        return "Unknown"
    except: return "Error"

def mapeo_subdominios(target):
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target): return target
    print(f"\n{BLUE}[*] Phase 0: Subdomain mapping for {CYAN}{target}{RESET}")
    try:
        proc = subprocess.run(["subfinder", "-d", target, "-silent"], capture_output=True, text=True)
        subs = [s for s in proc.stdout.strip().split("\n") if s]
        if not subs: return target
        print(f"{GREEN}[+] Subdomains found:{RESET}")
        for i, sub in enumerate(subs): print(f"  {YELLOW}{i+1}.{RESET} {sub}")
        choice = input(f"\n{GREEN}Select a number (or ENTER for main domain): {RESET}")
        return subs[int(choice)-1] if choice else target
    except: return target

def run_flash_scan(initial_target):
    missing = verificar_entorno()
    if missing:
        print(f"{RED}[!] ERROR: Missing tools: {', '.join(missing)}{RESET}")
        return

    print(LOGO)
    target = mapeo_subdominios(initial_target)
    
    folder = f"FlashScan_{target}_{datetime.datetime.now().strftime('%H%M%S')}"
    os.makedirs(folder, exist_ok=True)
    report_file = os.path.join(folder, "General_Report.txt")
    
    with open(report_file, "w") as f:
        f.write(f"FLASHSCAN PROFESSIONAL REPORT\nTarget: {target}\n" + "="*40 + "\n")

    os_info = get_os_by_ttl(target)
    print(f"{YELLOW}[!] Target: {CYAN}{target}{RESET} | OS: {CYAN}{os_info}{RESET}\n" + "-"*80)

    # --- PHASE 1: FAST SCAN ---
    print(f"{BLUE}[*] Phase 1: Fast port scanning...{RESET}")
    f1 = subprocess.run(["sudo", "nmap", "-p-", "--open", "--min-rate", "5000", "-n", "-Pn", target], capture_output=True, text=True)
    ports = re.findall(r"(\d+)/tcp\s+open", f1.stdout)
    
    if not ports:
        print(f"{RED}[!] No open ports found.{RESET}"); return
    
    print(f"{GREEN}[+] Found {len(ports)} active ports.{RESET}")
    port_list = ",".join(ports)

    # --- PHASE 2: SERVICES ---
    print(f"\n{YELLOW}------------------------------------------------------------{RESET}")
    if input(f"{GREEN}Perform detailed service/version analysis? (y/n): {RESET}").lower() == 'y':
        print(f"{BLUE}[*] Phase 2: Identifying services...{RESET}")
        f2 = subprocess.run(["sudo", "nmap", "-sV", "-sC", "-p", port_list, target, "-T4"], capture_output=True, text=True)
        log_to_file("\n--- PHASE 2: SERVICES ---\n" + f2.stdout, report_file)
        for s in parse_nmap_output(f2.stdout): print(s)

        # --- PHASE 3: VULN ---
        print(f"\n{YELLOW}------------------------------------------------------------{RESET}")
        if input(f"{RED}Launch VULNERABILITY (CVE) audit? (y/n): {RESET}").lower() == 'y':
            print(f"{BLUE}[*] Phase 3: Analyzing critical flaws...{RESET}")
            f3 = subprocess.run(["sudo", "nmap", "-sV", "--script", "vuln", "-p", port_list, target, "-T4"], capture_output=True, text=True)
            log_to_file("\n--- PHASE 3: CVEs ---\n" + f3.stdout, report_file)
            if "VULNERABLE" in f3.stdout: print(f"{RED}[!] SYSTEM VULNERATED. Check report for details.{RESET}")
            else: print(f"{GREEN}[✓] No critical flaws detected.{RESET}")

    # --- PHASE 4: FFUF ---
    web_ports = [p for p in ports if p in ["80", "443", "8080"]]
    if web_ports:
        print(f"\n{YELLOW}------------------------------------------------------------{RESET}")
        if input(f"{GREEN}Launch FFUF web directory discovery? (y/n): {RESET}").lower() == 'y':
            for wp in web_ports:
                log = os.path.join(folder, f"ffuf_{wp}.log")
                subprocess.Popen(f"ffuf -u http://{target}:{wp}/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -mc 200,301,302 -s > {log} 2>&1", shell=True)
            print(f"{GREEN}[!] Ffuf running in background. Press ENTER for status.{RESET}")
            while subprocess.run(["pgrep", "ffuf"], capture_output=True).stdout:
                if select.select([sys.stdin], [], [], 1)[0]:
                    sys.stdin.readline()
                    print(f"{CYAN}[i] Ffuf still working. Check logs in {folder}{RESET}")
            print(f"\n{GREEN}🔔 FFUF Finished.{RESET}")

    print(f"\n{GREEN}[✓] Audit complete. Files saved in: {folder}{RESET}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(LOGO); sys.exit(1)
    if sys.argv[1].lower() == "man": mostrar_manual()
    else: run_flash_scan(sys.argv[1])
