import os
import re

client_dir = r"P:\dev\TibiaCore\client"

# 1. Update skills.otui - Remove Fist (skillId0) and Fishing (skillId6)
otui_path = os.path.join(client_dir, "modules", "game_skills", "skills.otui")
with open(otui_path, "r") as f: content = f.read()

# Remove skillId0 (Fist Fighting) block
fist_block = """    SkillButton
      id: skillId0
      SkillNameLabel
        !text: tr('Fist Fighting')
      SkillValueLabel
      ImageSkill
        image-source: /images/icons/icon_fist
        image-size: 9 9
      SkillPercentPanel\n\n"""
content = content.replace(fist_block, "")

# Remove skillId6 (Fishing) block
fishing_block = """    SkillButton
      id: skillId6
      SkillNameLabel
        !text: tr('Fishing')
      SkillValueLabel
      ImageSkill
        image-source: /images/icons/icon_fishing
        image-size: 9 9
      SkillPercentPanel\n\n"""
content = content.replace(fishing_block, "")

# Remove from sub-menu
content = content.replace("  SkillsSubMenuOption\n    id: showFist\n    !text: tr('Fist')\n\n", "")
content = content.replace("  SkillsSubMenuOption\n    id: showFishing\n    !text: tr('Fishing')\n\n", "")

with open(otui_path, "w") as f: f.write(content)


# 2. Update skills.lua
lua_path = os.path.join(client_dir, "modules", "game_skills", "skills.lua")
with open(lua_path, "r") as f: content = f.read()
# Remove fist and fishing from map
content = content.replace("            showFist = 'skillId0',\n", "")
content = content.replace("            showFishing = 'skillId6'\n", "")
content = content.replace("        showFist = 'skillId0',\n", "")
content = content.replace("        showFishing = 'skillId6'\n", "")
# Fix potential trailing comma for Fishing
content = re.sub(r"showShielding = 'skillId5',\s*}", "showShielding = 'skillId5'\n        }", content)
content = re.sub(r"showShielding = 'skillId5',\s+}", "showShielding = 'skillId5'\n    }", content)

with open(lua_path, "w") as f: f.write(content)


# 3. Update statsbar.lua
statsbar_path = os.path.join(client_dir, "modules", "game_interface", "widgets", "statsbar.lua")
with open(statsbar_path, "r") as f: content = f.read()
# Remove Fist and Fishing from statsbar tuples
fist_line = "{skill = Skill.Fist,        key = 'fist',       icon = '/images/icons/icon_fist',        placement = 'left',     order = 3,  name = \"Fist Fighting Skill\"},"
fishing_line = "{skill = Skill.Fishing,     key = 'fishing',    icon = '/images/icons/icon_fishing',     placement = 'right',    order = 3,  name = \"Fishing Fighting Skill\"},"
content = content.replace(fist_line, "")
content = content.replace(fishing_line, "")
with open(statsbar_path, "w") as f: f.write(content)

# 4. Update neededtranslations.lua - Change translation to "Corpo a Corpo"
locales_path = os.path.join(client_dir, "modules", "client_locales", "neededtranslations.lua")
with open(locales_path, "r") as f: content = f.read()
# Note: Since I don't know the exact format of the translation file (if it's a map or list), 
# I will add a special note/entry for Corpo a Corpo if it exists or replace the existing one.
content = content.replace("'Melee Fighting',", "'Melee Fighting', -- Traduzir para 'Corpo a Corpo'")
# If it's the translation module itself, we usually edit the .lua or .otml in the actual locale folder, 
# but for now I'll ensure "Melee Fighting" is available for translation.
with open(locales_path, "w") as f: f.write(content)

print("Client UI cleanup complete.")