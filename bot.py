import interactions
import json
import os

SANCIONES_FILE = "sanciones.json"
PERMISOS_FILE = "permisos.json"

def cargar_sanciones():
    if not os.path.isfile(SANCIONES_FILE):
        with open(SANCIONES_FILE, "w") as f:
            json.dump({}, f)
    with open(SANCIONES_FILE, "r") as f:
        return json.load(f)

def guardar_sanciones(data):
    with open(SANCIONES_FILE, "w") as f:
        json.dump(data, f, indent=4)

def cargar_permisos():
    if not os.path.isfile(PERMISOS_FILE):
        with open(PERMISOS_FILE, "w") as f:
            json.dump({"roles_permitidos": []}, f)
    with open(PERMISOS_FILE, "r") as f:
        return json.load(f)

def guardar_permisos(data):
    with open(PERMISOS_FILE, "w") as f:
        json.dump(data, f, indent=4)

bot = interactions.Client(token=os.getenv("DISCORD_BOT_TOKEN"))

@bot.slash_command(name="setperm", description="Define qué roles pueden usar comandos de sanción")
@interactions.slash_option(
    name="rol",
    description="Rol a permitir",
    type=interactions.OptionType.ROLE,
    required=True
)
async def setperm(ctx, rol: interactions.Role):
    if not ctx.author.permissions.administrator:
        await ctx.send("❌ Solo administradores pueden usar este comando.", ephemeral=True)
        return

    permisos = cargar_permisos()
    if rol.id not in permisos["roles_permitidos"]:
        permisos["roles_permitidos"].append(rol.id)
        guardar_permisos(permisos)
        await ctx.send(f"✅ El rol {rol.name} ahora puede usar los comandos de sanción.", ephemeral=True)
    else:
        await ctx.send(f"❌ El rol {rol.name} ya tiene permiso.", ephemeral=True)

async def tiene_permiso(ctx):
    permisos = cargar_permisos()
    roles_permitidos = permisos.get("roles_permitidos", [])
    author_roles = [r.id for r in ctx.author.roles]
    if ctx.author.permissions.administrator:
        return True
    return any(r in roles_permitidos for r in author_roles)

@bot.slash_command(name="sancionar", description="Aplica una sanción a un usuario")
@interactions.slash_option(
    name="staff",
    description="Usuario que será sancionado",
    type=interactions.OptionType.USER,
    required=True,
)
@interactions.slash_option(
    name="razon",
    description="Motivo de la sanción",
    type=interactions.OptionType.STRING,
    required=True,
)
@interactions.slash_option(
    name="sancion",
    description="Tipo de sanción (ejemplo: W1)",
    type=interactions.OptionType.STRING,
    required=True,
)
async def sancionar(ctx, staff: interactions.Member, razon: str, sancion: str):
    if not await tiene_permiso(ctx):
        await ctx.send("❌ No tienes permiso para usar este comando.", ephemeral=True)
        return

    sanciones = cargar_sanciones()
    user_id = str(staff.id)

    warns_actuales = sanciones.get(user_id, {}).get("warns", 0)
    warns_actuales += 1

    sanciones[user_id] = {"warns": warns_actuales}
    guardar_sanciones(sanciones)

    if warns_actuales < 3:
        sancion_texto = f"Warn {warns_actuales}/3"
    else:
        sancion_texto = f"Warn 3/3 + descenso"
        sanciones[user_id] = {"warns": 0}
        guardar_sanciones(sanciones)

    mensaje = (
        f"🔨 Sanción aplicada:\n\n"
        f"- Nombre: <@{user_id}>\n"
        f"- Sanción: {sancion_texto}\n"
        f"- Razón: {razon}"
    )

    await ctx.send(mensaje)

bot.start()
