# Guía de uso del bot de sanciones

## 1. Configuración
- Crea una variable de entorno llamada `DISCORD_BOT_TOKEN` con tu token del bot.
- Ejecuta el bot con: `python bot.py`

## 2. Comandos disponibles

### /setperm
Permite a un administrador asignar qué roles pueden usar el comando `/sancionar`.

Ejemplo:
/setperm rol: @Moderador

### /sancionar
Aplica una sanción a un miembro. Si el usuario acumula 3 warns, se le "resetea" y se indica descenso.

Ejemplo:
/sancionar staff: @Usuario razon: No hizo expediente sancion: W1
