#!/usr/bin/env python3
import sys
import argparse

def evaluate_command(command_args):
    """
    Sub-agent filter: evaluates if a simulated or about-to-be-executed command 
    attempts to exfiltrate data from restricted paths.
    """
    restricted_keywords = ['data/', './data', '.env', 'ChequesDeudoresMFT']
    git_push_commands = ['push', 'commit -a', 'add data', 'add .env', 'add .']
    
    cmd_str = ' '.join(command_args).lower()
    
    # Check 1: Using git with restricted paths
    if 'git' in cmd_str:
        for restrict in restricted_keywords:
            if restrict in cmd_str:
                return False, f"ALERTA CRÍTICA: Intento de agregar rutassensibles al control de versiones ({restrict})."
        
        for push_cmd in git_push_commands:
            if push_cmd in cmd_str:
                 return False, f"ALERTA DE SEGURIDAD: Comandos amplios de git detectados. Recuerda el protocolo Anti-GitHub. Revisa qué archivos estás commiteando."
                 
    # Check 2: Unsafe web exports (curl/wget with data payload)
    if 'curl' in cmd_str or 'wget' in cmd_str or 'scp' in cmd_str or 'ftp' in cmd_str:
        if 'data/' in cmd_str or '.csv' in cmd_str:
             return False, "ALERTA CRÍTICA: Intento de transferencia de archivos de datos al exterior."

    return True, "[OK] Comando seguro según protocolo."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Privacy check para comandos del sub-agente.")
    parser.add_argument('command', nargs=argparse.REMAINDER, help="Comando a evaluar")
    args = parser.parse_args()
    
    if not args.command:
        print("Protocolo Activo. Sistema de monitoreo Anti-Exfiltración en línea.")
        sys.exit(0)
        
    is_safe, msg = evaluate_command(args.command)
    
    if not is_safe:
        print(f"\n{'='*50}\n[BLOQUEO DE SEGURIDAD] TAREA ABORTADA\n{'='*50}")
        print(msg)
        print("Acción prevenida para cumplir con el Bloque 3: Protocolo de Privacidad.")
        sys.exit(1)
    else:
        print(msg)
        sys.exit(0)
