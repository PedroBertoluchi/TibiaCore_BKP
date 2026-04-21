import os
import re

file_path = r"P:\dev\TibiaCore\client\data\locales\pt.lua"

# Dictionary of English keys to correct Portuguese translations for common UI elements
# This ensures we get the most important UI elements perfectly right.
corrections = {
    "4c) False Report to Gamemaster": "4c) Relatório falso para Gamemaster",
    "Audio": "Áudio",
    "Classic control": "Controle clássico",
    "Client Version": "Versão do Client",
    "Comment": "Comentário",
    "Comment:": "Comentário:",
    "Connecting to login server...": "Conectando no servidor de autenticação...",
    "Connection Error": "Erro de Conexão",
    "Connection failed.": "Conexão falhou.",
    "Critical Hit Chance": "Chance de acerto crítico",
    "Critical Hit Damage": "Dano de acerto crítico",
    "Default": "Padrão",
    "Description": "Descrição",
    "Description:": "Descrição:",
    "Distance Fighting": "Combate a Distância",
    "Enable audio": "Ativar áudio",
    "Enable dash walking": "Ativar andar rápido",
    "Enable music sound": "Ativar música",
    "Experience": "Experiência",
    "Force Exit": "Forçar Saída",
    "Formula": "Fórmula",
    "Graphics": "Gráficos",
    "Graphics card driver not detected": "Driver da placa de vídeo não detectado",
    "Head": "Cabeça",
    "Health Information": "Informação de vida",
    "Inventory": "Inventário",
    "Level": "Nível",
    "Light Version": "Versão da luz",
    "Magic Level": "Nível Mágico",
    "Mana Information": "Informação de mana",
    "Message:": "Mensagem:",
    "Module Manager": "Gerenciador de Módulos",
    "Next Level": "Próximo Nível",
    "Notification": "Notificação",
    "Options": "Opções",
    "Password": "Senha",
    "Play": "Jogar",
    "Regeneration Time": "Tempo de Regeneração",
    "Server Log": "Registro do servidor",
    "Show timestamps in console": "Exibir o horário no console",
    "Skull Time": "Tempo de Caveira",
    "Soul Points": "Pontos de Alma",
    "Special": "Especial",
    "Spell List": "Lista de Feitiços",
    "Stamina": "Vigor",
    "Statement:": "Afirmação:",
    "Statistics": "Estatísticas",
    "Status": "Condição",
    "Support": "Suporte",
    "Terminal": "Terminal",
    "Title": "Título",
    "Total Price:": "Preço total:",
    "Vocation": "Vocação",
}

# Sub-string replacements for any remaining cases
# Maps common broken byte sequences to correct characters
char_fixes = {
    "ï¿½": " ", # Fallback to space if unknown, but we'll try to be more specific
}

# Read file
with open(file_path, "rb") as f:
    content = f.read().decode('latin-1')

lines = content.split('\n')
new_lines = []

for line in lines:
    match = re.match(r'(\s+\["(.*?)"\]\s*=\s*")(.*)(".*)', line)
    if match:
        indent_key = match.group(1)
        english_key = match.group(2)
        portuguese_value = match.group(3)
        suffix = match.group(4)
        
        # Check if we have a direct correction for this key
        if english_key in corrections:
            portuguese_value = corrections[english_key]
        elif "ï¿½" in portuguese_value:
            # Context-aware fixes for common words
            portuguese_value = portuguese_value.replace("atï¿½", "até")
            portuguese_value = portuguese_value.replace("vocï¿½", "você")
            portuguese_value = portuguese_value.replace("nï¿½o", "não")
            portuguese_value = portuguese_value.replace("estï¿½", "está")
            portuguese_value = portuguese_value.replace("jï¿½", "já")
            portuguese_value = portuguese_value.replace("ï¿½ possivel", "é possível")
            portuguese_value = portuguese_value.replace("ï¿½udio", "áudio")
            portuguese_value = portuguese_value.replace("experiï¿½ncia", "experiência")
            portuguese_value = portuguese_value.replace("prï¿½ximo", "próximo")
            portuguese_value = portuguese_value.replace("nï¿½vel", "nível")
            portuguese_value = portuguese_value.replace("solicitaï¿½ï¿½o", "solicitação")
            portuguese_value = portuguese_value.replace("violaï¿½ï¿½o", "violação")
            portuguese_value = portuguese_value.replace("Afirmaï¿½ï¿½o", "Afirmação")
            portuguese_value = portuguese_value.replace("informaï¿½ï¿½o", "informação")
            portuguese_value = portuguese_value.replace("conexï¿½o", "conexão")
            portuguese_value = portuguese_value.replace("descriï¿½ï¿½o", "descrição")
            portuguese_value = portuguese_value.replace("visualizaï¿½ï¿½o", "visualização")
            portuguese_value = portuguese_value.replace("invï¿½lido", "inválido")
            portuguese_value = portuguese_value.replace("rï¿½pido", "rápido")
            portuguese_value = portuguese_value.replace("fï¿½rmula", "fórmula")
            portuguese_value = portuguese_value.replace("Cabeï¿½a", "Cabeça")
            portuguese_value = portuguese_value.replace("Forï¿½ar", "Forçar")
            portuguese_value = portuguese_value.replace("Padrï¿½o", "Padrão")
            portuguese_value = portuguese_value.replace("crï¿½tico", "crítico")
            portuguese_value = portuguese_value.replace("Versï¿½o", "Versão")
            portuguese_value = portuguese_value.replace("mï¿½sica", "música")
            portuguese_value = portuguese_value.replace("vï¿½deo", "vídeo")
            portuguese_value = portuguese_value.replace("Vocaï¿½ï¿½o", "Vocação")
            portuguese_value = portuguese_value.replace("autenticaï¿½ï¿½o", "autenticação")
            portuguese_value = portuguese_value.replace("Relatï¿½rio", "Relatório")
            portuguese_value = portuguese_value.replace("Comentï¿½rio", "Comentário")
            portuguese_value = portuguese_value.replace("inventï¿½rio", "inventário")
            portuguese_value = portuguese_value.replace("Horï¿½rio", "Horário")
            portuguese_value = portuguese_value.replace("ï¿½", "e") # Last resort: replace with 'e' or space
            
        new_lines.append(f'{indent_key}{portuguese_value}{suffix}')
    else:
        new_lines.append(line)

final_content = '\n'.join(new_lines)

# Save as CP1252
with open(file_path, "w", encoding="cp1252", errors="ignore") as f:
    f.write(final_content)

print("Comprehensive fix for pt.lua completed.")
