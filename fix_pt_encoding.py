import os

file_path = r"P:\dev\TibiaCore\client\data\locales\pt.lua"

# Mapping of common broken patterns found in the grep/read output
# These are typical of CP1252/Latin-1 characters being displayed or handled as broken UTF-8
replacements = {
    "Portugus": "Português",
    "experincia": "experiência",
    "nvel": "nível",
    "solicitao": "solicitação",
    "invlido": "inválido",
    "no": "não",
    "violao": "violação",
    "Afirmao": "Afirmação",
    "pblica": "pública",
    "lingua": "língua",
    "Ao": "Ação",
    "boto": "botão",
    "sacrifcio": "sacrifício",
    "jornadas": "jornadas",
    "mdulos": "módulos",
    "recarregados": "recarregados",
    "perseguio": "perseguição",
    "Leilo": "Leilão",
    "Autenticao": "Autenticação",
    "Annimo": "Anônimo",
    "depsito": "depósito",
    "latncia": "latência",
    "informticas": "informáticas",
    "nveis": "níveis",
    "horrio": "horário",
    "Feitios": "Feitiços",
    "Condio": "Condição",
    "Sesso": "Sessão",
    "Ttulo": "Título",
    "preo": "preço",
    "mdio": "médio",
    "virada": "virada",
    "possvel": "possível",
    "vlido": "válido",
    "Vocao": "Vocação",
    "Ir": "Irá",
    "rpidos": "rápidos",
}

# Read the file as bytes to avoid any encoding mangling during the process
with open(file_path, "rb") as f:
    content = f.read()

# We suspect the file was originally CP1252 or was mangled into a mix.
# Let's try to decode as latin-1 (safe) and then replace characters.
text = content.decode('latin-1', errors='ignore')

# Fix known mangled words (this is surgical)
for old, new in replacements.items():
    # If the 'old' has a '', we need to match what's actually in the string
    # Usually in latin-1, the '' might be a specific byte like 0xEA (ê)
    # But since I saw '' in the tool output, I'll use a more robust way.
    pass

# Direct byte replacements for common Portuguese characters mangled from CP1252 to UTF-8/Broken
# ê = 0xEA, á = 0xE1, é = 0xE9, í = 0xED, ó = 0xF3, ú = 0xFA, ç = 0xE7, ã = 0xE3, õ = 0xF5
# Let's just convert the whole file from CP1252 to UTF-8 properly.

try:
    decoded = content.decode('cp1252')
    # Change the charset line in the file
    decoded = decoded.replace('charset = "cp1252"', 'charset = "UTF-8"')
    # Ensure Melee Fighting is correct
    decoded = decoded.replace('Corpo a Corpo', 'Corpo a Corpo') 
    
    # Write back as UTF-8
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(decoded)
    print("File successfully converted to UTF-8 and fixed.")
except Exception as e:
    print(f"Error: {e}")
