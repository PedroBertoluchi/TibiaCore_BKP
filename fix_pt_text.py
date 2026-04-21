import os
import re

file_path = r"P:\dev\TibiaCore\client\data\locales\pt.lua"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Pattern for the broken character sequence ï¿½
broken = "ï¿½"

# Mapping of specific broken words to fixed ones
# I'll use regex to find words containing the broken character and replace them
word_fixes = {
    r"Portugu" + broken + "s": "Português",
    r"experi" + broken + "ncia": "experiência",
    r"pr" + broken + "ximo": "próximo",
    r"n" + broken + "vel": "nível",
    r"solicita" + broken + broken + "o": "solicitação",
    r"solicita" + broken + "o": "solicitação",
    r"inv" + broken + "lido": "inválido",
    r"n" + broken + "o": "não",
    r"viola" + broken + broken + "o": "violação",
    r"viola" + broken + "o": "violação",
    r"Afirma" + broken + broken + "o": "Afirmação",
    r"Afirma" + broken + "o": "Afirmação",
    r"p" + broken + "blica": "pública",
    r"l" + broken + "ngua": "língua",
    r"A" + broken + broken + "o": "Ação",
    r"A" + broken + "o": "Ação",
    r"bot" + broken + broken + "o": "botão",
    r"bot" + broken + "o": "botão",
    r"sacrif" + broken + "cio": "sacrifício",
    r"m" + broken + "dulos": "módulos",
    r"recarregados": "recarregados",
    r"persegui" + broken + broken + "o": "perseguição",
    r"persegui" + broken + "o": "perseguição",
    r"Leil" + broken + broken + "o": "Leilão",
    r"Leil" + broken + "o": "Leilão",
    r"Autentica" + broken + broken + "o": "Autenticação",
    r"Autentica" + broken + "o": "Autenticação",
    r"An" + broken + "nimo": "Anônimo",
    r"dep" + broken + "sito": "depósito",
    r"lat" + broken + "ncia": "latência",
    r"inform" + broken + "ticas": "informáticas",
    r"n" + broken + "veis": "níveis",
    r"hor" + broken + "rio": "horário",
    r"Feiti" + broken + "os": "Feitiços",
    r"Condi" + broken + broken + "o": "Condição",
    r"Condi" + broken + "o": "Condição",
    r"Sess" + broken + broken + "o": "Sessão",
    r"Sess" + broken + "o": "Sessão",
    r"T" + broken + "tulo": "Título",
    r"pre" + broken + "o": "preço",
    r"m" + broken + "dio": "médio",
    r"voc" + broken + " ": "você ",
    r"Voc" + broken + " ": "Você ",
    r"est" + broken + " ": "está ",
    r"Est" + broken + " ": "Está ",
    r"n" + broken + " ": "não ",
    r"at" + broken + " ": "até ",
    r"tamb" + broken + "m": "também",
    r"aten" + broken + broken + "o": "atenção",
    r"aten" + broken + "o": "atenção",
    r"configura" + broken + broken + "o": "configuração",
    r"configura" + broken + "o": "configuração",
    r"permiss" + broken + broken + "o": "permissão",
    r"permiss" + broken + "o": "permissão",
    r"est" + broken + "o": "estão",
    r"at" + broken + " ": "até ",
}

new_text = text
for pattern, replacement in word_fixes.items():
    new_text = re.sub(pattern, replacement, new_text)

# Also do a general fallback for any remaining broken characters if they match common vowels
# broken = ï¿½
# This is risky but let's try some common ones
# ï¿½ in the middle of words is usually an accented vowel or ç.

# Change back to cp1252 header
new_text = new_text.replace('charset = "UTF-8"', 'charset = "cp1252"')

with open(file_path, "w", encoding="cp1252", errors="ignore") as f:
    f.write(new_text)

print("File fixed with Portuguese characters and saved as CP1252.")
