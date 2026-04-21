import os
import re

file_path = r"P:\dev\TibiaCore\client\data\locales\pt.lua"

# Broken pattern
broken = "ï¿½"

# Read as UTF-8 (since I just saved it as CP1252 but with some broken UTF-8 patterns)
# Actually, let's read it as latin-1 to be safe and see raw bytes.
with open(file_path, "rb") as f:
    content = f.read()

# Convert back to string to perform replacements
# If it's CP1252 but contains UTF-8 broken characters, it's a mess.
# Let's decode as latin-1, replace, then save as cp1252.
text = content.decode('latin-1')

# Extensive mapping for Portuguese characters in this specific broken format
replacements = {
    "Amea" + broken + "ar": "Ameaçar",
    "viola" + broken + broken + "o": "violação",
    "viola" + broken + "o": "violação",
    "solicita" + broken + broken + "o": "solicitação",
    "solicita" + broken + "o": "solicitação",
    "informa" + broken + broken + "o": "informação",
    "informa" + broken + "o": "informação",
    "A" + broken + broken + "o": "Ação",
    "A" + broken + "o": "Ação",
    "dire" + broken + broken + "o": "direção",
    "dire" + broken + "o": "direção",
    "possi" + broken + "vel": "possível",
    "v" + broken + "lido": "válido",
    "at" + broken + " ": "até ",
    "est" + broken + " ": "está ",
    "est" + broken + "o": "estão",
    "voc" + broken + " ": "você ",
    "Voc" + broken + " ": "Você ",
    "n" + broken + "o": "não",
    "N" + broken + "o": "Não",
    "pr" + broken + "ximo": "próximo",
    "n" + broken + "vel": "nível",
    "n" + broken + "veis": "níveis",
    "experi" + broken + "ncia": "experiência",
    "influ" + broken + "ncia": "influência",
    "execu" + broken + broken + "o": "execução",
    "execu" + broken + "o": "execução",
    "permiss" + broken + broken + "o": "permissão",
    "permiss" + broken + "o": "permissão",
    "aten" + broken + broken + "o": "atenção",
    "aten" + broken + "o": "atenção",
    "configura" + broken + broken + "o": "configuração",
    "configura" + broken + "o": "configuração",
    "reunio": "reunião",
    "an" + broken + "ncio": "anúncio",
    "An" + broken + "ncio": "Anúncio",
    "ativida" + broken + "": "atividade",
    "ativida" + broken + "": "atividade",
    "p" + broken + "blica": "pública",
    "P" + broken + "blica": "Pública",
    "m" + broken + "dulo": "módulo",
    "M" + broken + "dulo": "Módulo",
}

# Apply surgical fixes
for old, new in replacements.items():
    text = text.replace(old, new)

# General fallback for common isolated broken characters (often ç or vowels)
# Warning: This can be destructive, but the broken pattern is quite unique.
# Let's only do it if we are sure.

# Final save as CP1252
with open(file_path, "w", encoding="cp1252", errors="ignore") as f:
    f.write(text)

print("Surgical fix for pt.lua completed.")
