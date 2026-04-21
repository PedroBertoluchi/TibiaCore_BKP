# Vocation Balance Analysis Framework

**Analysis Date:** 2026-04-16  
**Analyzed By:** Lambert (Vocation & Balance Specialist)  
**Repository:** TibiaCore

---

## 1. Vocation Identity Matrix

The 12-vocation system is organized into 4 base classes, each with 2 promotion specializations:

### MAGE LINE (Magic DPS & Healing)

#### **Mage** (Base)
- **Primary Role:** Pure DPS / Spell Support
- **Key Strengths:**
  - Highest mana generation (gainmana: 30/lvl in base, 30 in Archmage)
  - Lowest mana cost multiplier (1.1×) = efficient spell casting
  - Balanced HP/Mana for learning phase
  - Access to Fire Punch at level 1
- **Key Weaknesses:**
  - Low HP growth (5/lvl base, 5 promoted) - vulnerable to direct damage
  - Limited survival tools outside mana shield
  - Minimal physical combat capability
- **Spell Progression:** Fire Punch (1), Arcane Bolt (12), Arcane Wave (38) - has gaps between 12-38 (26 levels)

#### **Archmage** (Promotion - Master Spellcaster)
- **Primary Role:** Pure DPS with burst potential
- **Identity vs. Necromancer:**
  - Emphasis: **Damage output and spell efficiency**
  - Faster mana regen (gainmanaticks: 2 vs Necro's 3) - cast more frequently
  - Same soul max (200) but gains mana faster mid-combat
  - Niche: Heavy offensive play, burst damage focus
- **Key Strengths:**
  - Fastest mana recovery among mages
  - Excellent for sustained spell rotation
  - Soul max doubled vs. base Mage (100→200)
- **Issues:**
  - HP gain (gainhpamount: 10) is OK but still vulnerable
  - No healing spell in current spell list for self-sustain

#### **Necromancer** (Promotion - Dark Summoner/Hybrid)
- **Primary Role:** Balanced hybrid with summon/damage focus
- **Identity vs. Archmage:**
  - Emphasis: **Survival and sustained damage**
  - Higher HP growth (gainhp: 10 vs Archmage's 5) - better survivability
  - Slightly slower mana regen (gainmanaticks: 3) but steadier
  - Niche: Solo play, summoner focus, damage with durability
- **Key Strengths:**
  - More durable than Archmage (double HP growth rate)
  - Soul max doubled (100→200) for summoning mechanics
  - Better equipped for solo PvE
- **Issues:**
  - No summon/undead spells in current spell list (spec incomplete)
  - Missing healing spells for self-healing gameplay

---

### ARCHER LINE (Ranged DPS & Mobility)

#### **Archer** (Base)
- **Primary Role:** Ranged DPS with support capability
- **Key Strengths:**
  - Solid HP growth (10/lvl) - survives better than mages
  - Balanced mana multiplier (1.4×) for skill-based spellcasting
  - Higher capacity gain (20/lvl) for equipment flexibility
  - Faster HP regen (gainhpticks: 4)
- **Key Weaknesses:**
  - Moderate mana generation (gainmana: 15/lvl) - fewer spells per rotation
  - Limited spell variety in current spell list
  - Mana multiplier (1.4×) means spells cost more
- **Spell Progression:** Fire Punch (1), Piercing Shot (23), Rangers Remedy (20) - **Rangers Remedy at level 20 before Piercing Shot at 23 (inverted progression)**

#### **Marksman** (Promotion - Precision DPS)
- **Primary Role:** Burst damage with special abilities
- **Identity vs. Beastmaster:**
  - Emphasis: **Precision, critical strikes, heavy burst**
  - Lower HP growth (10 vs Beast's 15) but equal mana
  - Faster mana regen (gainmanaticks: 3) - more ability spam
  - Niche: Single-target burst, critical focus, skill-shot mechanics
- **Key Strengths:**
  - Fast ability recharge (gainmanaticks: 3)
  - Effective for PvP burst combos
  - Soul doubled (100→200)
- **Issues:**
  - Currently only has Eagle Eye support spell at level 60 (no combat spells beyond base)
  - Large gap: Piercing Shot (23) → Eagle Eye (60) = 37 level gap

#### **Beastmaster** (Promotion - Tanky Ranger)
- **Primary Role:** Durable ranged with pet/summon focus
- **Identity vs. Marksman:**
  - Emphasis: **Durability, pet synergy, crowd control**
  - Highest archer HP growth (15/lvl) - closer to knight durability
  - Fastest HP regen among archers (gainhpticks: 2) - even better survival
  - Niche: Beast commander, off-tank with ranged capability
- **Key Strengths:**
  - Comparable HP growth to melee classes (15/lvl)
  - Fastest HP recovery (gainhpticks: 2)
  - Excellent for solo farming and survival
- **Issues:**
  - No pet/summon spells in current spell list
  - Missing combat ability progression (relies on base class spells)
  - Soul doubled (100→200)

---

### KNIGHT LINE (Melee Tank & Crowd Control)

#### **Knight** (Base)
- **Primary Role:** Melee tank / Physical DPS hybrid
- **Key Strengths:**
  - Highest capacity gain (25/lvl) - carries most equipment
  - Good HP growth (15/lvl) - naturally tanky
  - Strong physical skill multiplier (id=4: 1.4×)
  - Fast HP regen (gainhpticks: 3)
- **Key Weaknesses:**
  - Very low mana generation (gainmana: 5/lvl) - limited spell usage
  - High mana cost multiplier (3.0×) - spells are expensive
  - No healing spell available in current spell list
  - Combined: Can cast very few spells per fight
- **Spell Progression:** Fire Punch (1), Crushing Blow (16), War Stomp (33) - 17 level gap, then 16+ level gap to next spell

#### **Templar** (Promotion - Defensive Tank/Support)
- **Primary Role:** Tank with support/healing capability
- **Identity vs. Death Knight:**
  - Emphasis: **Defensive stacking, healing, survivability**
  - Highest HP growth among knights (20/lvl vs DK's 15) - ultra-tanky
  - Lower mana generation (gainmana: 5) but still limited
  - Niche: Group tank, healer tank, group synergy
- **Key Strengths:**
  - Exceptional HP growth (20/lvl) - only Beastmaster rivals it
  - Fastest HP regen (gainhpticks: 2) - unmatched survival
  - Soul doubled (100→200) for defensive mechanics
  - High physical skill bonus (1.4×)
- **Issues:**
  - Still extremely limited mana (gainmana: 5/lvl + 3.0× multiplier)
  - No healing or support spells in current spell list (spec incomplete)
  - Battle Trance at level 60 is only support spell (huge gap from level 33)

#### **Death Knight** (Promotion - Offensive Tank/Hybrid)
- **Primary Role:** Hybrid DPS/Tank with lifesteal potential
- **Identity vs. Templar:**
  - Emphasis: **Aggressive durability, lifesteal, damage over tanking**
  - Moderate HP growth (15/lvl vs Templar's 20) - more glass-cannon
  - Higher mana generation (gainmana: 10 vs Templar's 5) - more spellcasting
  - Niche: Self-healing tank, solo farming, aggro management
- **Key Strengths:**
  - Better mana pool than Templar (double mana gain: 10 vs 5)
  - Still respectable HP (15/lvl), though less than Templar
  - Soul doubled (100→200)
  - More balanced for mixed combat
- **Issues:**
  - Still very limited spell access due to high mana multiplier (3.0×)
  - No lifesteal/healing spells in current spell list (spec incomplete)
  - Missing endgame combat spells

---

### OCCULTIST LINE (Magic Hybrid & Crowd Control)

#### **Occultist** (Base)
- **Primary Role:** Mixed magic DPS / Crowd control hybrid
- **Key Strengths:**
  - Balanced stat distribution (15 HP/20 Mana/15 Cap per level)
  - Moderate mana multiplier (1.2×) - more spell casting than knights
  - Unique skill multipliers: Melee (1.5×), Magic (1.8×4) - versatile damage
  - Average mana regen (gainmanaticks: 4)
- **Key Weaknesses:**
  - Lower HP than archers (10 vs 10, but archers have 20 cap)
  - No spells in current spell list for base class - **completely missing spell progression**
  - Unclear primary role: hybrid? support? DPS?
- **Spell Progression:** Fire Punch (1) only - **missing all Occultist-specific spells**

#### **Blood Mage** (Promotion - Lifesteal Tank)
- **Primary Role:** HP-scaling damage / Melee vampire hybrid
- **Identity vs. Heretic:**
  - Emphasis: **Physical-magical blend, lifesteal, HP scaling**
  - Higher HP growth (15/lvl) - mirrors Beastmaster durability
  - Balanced mana (gainmana: 15) - more spellcasting than base
  - Niche: Blood magic user, lifesteal focus, melee-magic hybrid
- **Key Strengths:**
  - Best HP growth among Occultist line (15/lvl, same as Beastmaster)
  - Decent mana (gainmana: 15) - spell access much improved
  - Soul doubled (100→200)
  - Magic skill bonus (1.8×4) still strong
- **Issues:**
  - No spells in current spell list for Blood Mage (spec incomplete)
  - No lifesteal/blood magic spells at all
  - Missing entire spell progression tree

#### **Heretic** (Promotion - Spellpower Caster)
- **Primary Role:** Magic DPS with utility focus
- **Identity vs. Blood Mage:**
  - Emphasis: **Pure magic output, utility, spell spam**
  - Lower HP (gainmana: 25 vs Blood's 15) - prioritizes mana
  - Fastest mana regen among Occultist line (gainmanaticks: 2)
  - Niche: Magic-focused specialist, spell spammer, pure caster
- **Key Strengths:**
  - Highest mana gain in Occultist line (gainmana: 25)
  - Fastest mana regen (gainmanaticks: 2) - highest spell cast rate
  - Soul doubled (100→200)
  - Strong magic skill multiplier (1.8×4)
- **Issues:**
  - Lower HP (gainmana: 10 vs Blood's 15) - fragile
  - No spells in current spell list for Heretic (spec incomplete)
  - Missing utility/support spells entirely

---

## 2. Stat Balance Review

### HP Growth Analysis (Per Level)

| Vocation | Base HP/Lvl | Promoted HP/Lvl | HPticks (lower=faster) | HPgain/tick | Notes |
|----------|-------------|-----------------|----------------------|-------------|-------|
| Mage | 5 | 5 (Archmage) | 6 / 4 | 5 / 10 | Squishy base, slightly better promoted |
| Necromancer | - | 10 | 3 | 10 | **Necro most durable mage** |
| Archer | 10 | 10 | 4 / 3 | 5 / 10 | Good base, better promoted regen |
| Marksman | - | 10 | 3 | 10 | Archer-level durability |
| Beastmaster | - | 15 | 2 | 10 | **Archer-class tank, rivals Templar** |
| Knight | 15 | 15 | 3 / 2 | 5 / 15 | Strong base, Templar ultra-durable |
| Templar | - | 20 | 2 | 15 | **Highest HP growth in game (20/lvl)** |
| Death Knight | - | 15 | 2 | 10 | Moderate tank, better than Mage line |
| Occultist | 10 | 10 | 5 / 3 | 5 / 10 | Fragile base, improved promoted |
| Blood Mage | - | 15 | 3 | 10 | **Rivals Beastmaster (15/lvl)** |
| Heretic | - | 10 | 4 / 2 | 5 / 15 | Low durability, fast regen when high-level |

**Balance Assessment:**
- ✅ **Templar** (20/lvl) is clearly the tank
- ✅ **Beastmaster** (15/lvl) and **Blood Mage** (15/lvl) provide mid-tier durability
- ⚠️ **Knight base** (15/lvl) is OK but Templar overshadows it significantly (20 vs 15 = 33% more HP)
- ❌ **Mage base** (5/lvl) is significantly weaker than every promoted class - creates power cliff at level 55

---

### Mana Growth Analysis (Per Level)

| Vocation | Base Mana/Lvl | Promoted Mana/Lvl | Manaticks (lower=faster) | Managain/tick | Notes |
|----------|----------------|-------------------|------------------------|--------------| -------|
| Mage | 30 | 30 (Archmage) | 6 / 2 | 5 / 10 | Highest mana gen, tied in promotion |
| Necromancer | - | 25 | 3 | 10 | **5 less mana/lvl but faster regen** |
| Archer | 15 | 15 | 4 / 3 | 5 / 10 | Moderate mana, solid for support |
| Marksman | - | 15 | 3 | 10 | Stable mana regen |
| Beastmaster | - | 15 | 3 | 10 | Same as Marksman |
| Knight | 5 | 5 | 6 / 4 | 5 / 5 | **Critically low - nearly uncastable** |
| Templar | - | 5 | 4 | 5 | **Still critically low** |
| Death Knight | - | 10 | 3 | 10 | **Double Knight mana, essential hybrid** |
| Occultist | 20 | 20 | 4 / 3 | 5 / 10 | Good mana, exceeds Archer |
| Blood Mage | - | 15 | 3 | 10 | Archer-level (improved from base) |
| Heretic | - | 25 | 2 | 15 | **Highest mana regen (gainmanaticks: 2, gainmanaamount: 15)** |

**Balance Assessment:**
- ✅ **Heretic** dominates mana regen (25/lvl + 2 ticks + 15/tick = 187.5 mana per tick at lvl 100)
- ✅ **Mage/Archmage** tied for mana generation (30/lvl)
- ✅ **Occultist/Heretic** tied in base mana gain (20-25/lvl)
- ⚠️ **Knight/Templar** have only 5/lvl mana - extremely limiting for spell-based abilities
- ❌ **Death Knight** (10/lvl) is better but still half of other hybrids

---

### Mana Multiplier (Spell Cost Scaling)

| Class | Multiplier | Impact | Strategy |
|-------|-----------|--------|----------|
| Mage / Archmage / Necromancer | 1.1× | **Most efficient** | Spam spells freely |
| Archer / Marksman / Beastmaster | 1.4× | 27% more expensive | Cast selectively |
| Knight / Templar / Death Knight | 3.0× | **27× more expensive than Mage!** | Spells are luxury items |
| Occultist / Blood Mage / Heretic | 1.2× | 9% more expensive | Balanced casting |

**Critical Balance Issue:**
- Knights pay **27 times** the mana cost per spell compared to Mages (3.0× vs 1.1×)
- Combined with 5/lvl mana generation, Knights are essentially **melee-only** classes
- A Knight at level 100: ~500 mana total, a 30-mana spell costs 90 mana (18% of pool per cast)
- A Mage at level 100: ~3300 mana total, a 30-mana spell costs 33 mana (1% of pool per cast)

**This multiplier design makes Knights and Templar functionally unable to engage in spell-based gameplay.**

---

### Attack Speed & Combat Pacing

| Vocation | Attackspeed (ms) | Basespeed | Notes |
|----------|-----------------|-----------|-------|
| ALL | 2000 | 220 | **Identical across all vocations** |

**Assessment:** No differentiation in combat speed. All vocations attack at the same rate.

---

## 3. Spell Progression Audit

### Current Spell Availability by Vocation

#### MAGE LINE
**Mage / Archmage:**
- Level 1: Fire Punch (attack, 15 mana)
- Level 8: Arcane Mend (healing, 20 mana) ✅
- Level 12: Arcane Bolt (attack, 20 mana) ✅
- Level 14: Arcane Shield (support, 50 mana) ✅
- Level 38: Arcane Wave (attack, 170 mana) ✅
- **Spells: 5 total | Gaps: 12→14 (2 lvl), 14→38 (24 lvl)**
- ❌ **24-level gap from level 14-38 with no new abilities**

**Necromancer:**
- Same spell list as Archmage (1, 8, 12, 14, 38)
- ❌ **No summon/undead-specific spells** (spec incomplete)

#### ARCHER LINE
**Archer / Marksman:**
- Level 1: Fire Punch (attack, 15 mana)
- Level 20: Rangers Remedy (healing, 70 mana) ✅ **EARLY HEALING**
- Level 23: Piercing Shot (attack, 25 mana) ✅
- Level 60: Eagle Eye (support, 450 mana) ✅
- **Spells: 4 total | Gaps: 23→60 (37 lvl)**
- ❌ **37-level gap from level 23-60 with no new attack abilities**
- ❌ **Rangers Remedy at level 20 before Piercing Shot at level 23 (inverted progression)**

**Beastmaster:**
- Same as Archer/Marksman (1, 20, 23, 60)
- ❌ **No pet/beast-specific spells** (spec incomplete)

#### KNIGHT LINE
**Knight / Templar:**
- Level 1: Fire Punch (attack, 15 mana)
- Level 16: Crushing Blow (attack, 30 mana) ✅
- Level 33: War Stomp (attack, 160 mana) ✅
- Level 60: Battle Trance (support, 290 mana) ✅
- **Spells: 4 total | Gaps: 16→33 (17 lvl), 33→60 (27 lvl)**
- ❌ **27-level gap from level 33-60 with no mid-level abilities**
- ❌ **No healing spells at all** (critical for survival-based classes)

**Death Knight:**
- Same as Knight/Templar (1, 16, 33, 60)
- ❌ **No lifesteal/blood-based spells** (spec incomplete)

#### OCCULTIST LINE
**Occultist / Blood Mage / Heretic:**
- Level 1: Fire Punch (attack, 15 mana) ONLY
- ❌ **COMPLETELY MISSING SPELL PROGRESSION**
- ❌ **No class-specific spells at all**

### Spell Coverage Analysis

#### ✅ What Works
1. Early game spells (Fire Punch at level 1) - all vocations covered
2. Mid-game transitions (levels 8-24) - Mage/Archer have reasonable progression
3. Promotion-exclusive abilities (levels 50+) - some support spells exist
4. Healing coverage - Mages (8), Archers (20), Clerics (35) - reasonable

#### ❌ Critical Gaps

| Class | Level Range | Gap Size | Missing |
|-------|------------|----------|---------|
| Mage | 14→38 | 24 levels | Mid-tier spell |
| Archer | 23→60 | 37 levels | Mid-tier and late-tier spells |
| Knight | 33→60 | 27 levels | Late-tier spell, healing spells |
| Occultist | 1→∞ | All levels | **Entire progression missing** |

**Scale:** In traditional Tibia, players advance ~2-3 levels per hour early game. A 24-level gap means 8-12 hours with no new abilities. This is extremely punishing.

#### ❌ Missing Promotion Identity Spells

| Promotion | Expected Theme | Missing |
|-----------|----------------|---------|
| Archmage | Burst damage, area control | No high-level AoE beyond Arcane Wave |
| Necromancer | Summons, undead control | **All summon spells missing** |
| Marksman | Precision, critical strikes | **No Marksman-exclusive abilities** |
| Beastmaster | Beast summoning, pet synergy | **All pet spells missing** |
| Templar | Divine protection, group support | **No Templar-exclusive healing** |
| Death Knight | Lifesteal, dark power | **All lifesteal spells missing** |
| Blood Mage | Blood magic, HP scaling | **No blood magic spells** |
| Heretic | Chaos/utility magic | **No Heretic-exclusive utilities** |

---

## 4. Balance Flags

### 🚨 CRITICAL ISSUES

1. **Occultist Line Has Zero Spell Progression**
   - Impact: 3 entire vocations (Occultist, Blood Mage, Heretic) cannot cast spells beyond Fire Punch
   - Severity: BLOCKING - players cannot reach intended power
   - Workaround: None

2. **Knight Line Mana System is Fundamentally Broken**
   - Knight mana multiplier (3.0×) + low mana generation (5/lvl) = unable to cast spells
   - Example: 30-mana spell costs 90 mana. At level 10 (50 mana pool), this is impossible
   - Impact: Knights are forced melee-only despite having spell slots
   - Severity: CRITICAL - breaks designed hybrid role

3. **24-37 Level Spell Gaps**
   - Players level up with no new abilities for 20+ levels
   - Creates gameplay boredom during crucial mid-level progression
   - Severity: HIGH - impacts player retention

4. **Inverted Spell Progression (Archer)**
   - Rangers Remedy (healing) available at level 20
   - Piercing Shot (attack) available at level 23
   - Should be reversed - combat skills before support
   - Severity: MEDIUM - breaks logical flow

### ⚠️ HIGH PRIORITY ISSUES

5. **Promotion Classes Have Minimal Differentiation**
   - Archmage vs. Necromancer: **identical spell list**
   - Marksman vs. Beastmaster: **identical spell list**
   - Templar vs. Death Knight: **identical spell list**
   - Blood Mage vs. Heretic: **identical spell list**
   - Players cannot distinguish class identities
   - Severity: HIGH - removes meaningful choice

6. **Support Spells Come Too Late**
   - Arcane Shield (14) is reasonable
   - But Battle Trance (60) and Eagle Eye (60) are endgame only
   - Mid-game players (levels 30-50) have no supportive tools
   - Severity: MEDIUM - limits build variety

7. **No Healing for Tank Classes**
   - Knights have zero healing spells
   - Death Knight has zero lifesteal spells
   - Templar has zero healing spells
   - These are survival-based classes with no survival tools
   - Severity: HIGH - incompatible with class identity

8. **Mana Cost Scaling is Inverted**
   - War Stomp (Knight) costs 160 mana - requires 2-3 full Knight mana pools
   - Arcane Wave (Mage) costs 170 mana - only 5% of Mage pool
   - Knights cannot use their own spells effectively
   - Severity: MEDIUM - punishes resource-intensive classes

### 📋 MEDIUM PRIORITY ISSUES

9. **Promotion Spell Timing**
   - First promotion spells appear around level 50-60
   - Promotions typically unlock around level 55-60 (standard Tibia)
   - Current timing is too late - players promote first, then get abilities
   - Severity: MEDIUM - impacts power curve

10. **Missing Spell Types**
    - No summon/pet spells for Beastmaster, Necromancer
    - No lifesteal/blood spells for Blood Mage, Death Knight
    - No utility/control spells for Heretic
    - Severity: MEDIUM - incomplete promotion identity

---

## 5. Balance Recommendations

### HIGH PRIORITY (Implement Immediately)

1. **CREATE OCCULTIST SPELL PROGRESSION**
   - Add class-specific spells for Occultist (base: levels 1-50)
   - Add promotion-exclusive spells (Blood Mage, Heretic: levels 55+)
   - Suggested structure:
     - Occultist: Spell Hex (25), Chaos Orb (40), Dark Ritual (50)
     - Blood Mage: Blood Lance (55), Crimson Nova (65), Sanguine Surge (80)
     - Heretic: Profane Blast (55), Chaos Storm (65), Anathema (80)

2. **FIX KNIGHT MANA SYSTEM**
   - Option A: Lower Knight mana multiplier from 3.0× to 2.0× (33% reduction)
   - Option B: Increase Knight mana gain from 5/lvl to 10/lvl (double)
   - Option C: Create "Weapon Ability" system where Knights cast melee-spells (0 mana cost, 6s cooldown)
   - **Recommendation:** Implement Option C + Option A for hybrid flexibility

3. **ADD HEALING SPELLS TO TANK CLASSES**
   - Knight: Minor Heal (20 mana) at level 8
   - Templar: Holy Mend (35 mana) at level 35 (improved healing)
   - Death Knight: Blood Drain (30 mana, lifesteal) at level 25
   - Ensures tanks can survive solo content

4. **FILL SPELL PROGRESSION GAPS**
   - Mage (14→38): Add tier spell at level 25 (e.g., "Arcane Burst" - AoE blast)
   - Archer (23→60): Add spells at levels 35, 45, 55 (progression to Eagle Eye)
   - Knight (33→60): Add spells at levels 45, 55 (progression to Battle Trance)
   - Fill with thematic abilities that build toward promotion playstyle

### MEDIUM PRIORITY (Implement in Next Cycle)

5. **CREATE PROMOTION-EXCLUSIVE SPELL IDENTITIES**
   - Archmage: Mastery of Area Control (Arcane Meteor, Arcane Explosion)
   - Necromancer: Undead Summoning (Summon Skeleton, Summon Ghoul, Summon Wraith)
   - Marksman: Critical Strike Abilities (Aimed Shot, Explosive Arrow, Piercing Barrage)
   - Beastmaster: Pet Commands (Summon Wolf, Summon Bear, Beast Pack Tactics)
   - Templar: Divine Protection (Holy Shield, Divine Blessing, Group Sanctuary)
   - Death Knight: Lifesteal & Corruption (Life Tap, Dark Pact, Unholy Aura)
   - Blood Mage: Blood Magic (Blood Ritual, Sanguine Empowerment, Life Exchange)
   - Heretic: Chaos & Curses (Chaos Bolt, Curse of Weakness, Dimensional Rift)

6. **REBALANCE STAT PROGRESSION FOR ROLE CLARITY**
   - Archmage: Increase mana regen advantage (maintain 30/lvl, lower gainmanaticks from 2→1)
   - Necromancer: Slightly lower HP (from 10→8) to reduce durability, gain 1-2 minion summons
   - Templar: Cap HP gain at 18/lvl (currently 20, which overshadows all DPS)
   - Death Knight: Increase mana to 12/lvl (currently 10) to support hybrid playstyle
   - Blood Mage: Add unique stat (Blood Pool) scaling with HP

7. **ADJUST MANA COSTS FOR CLASS BALANCE**
   - Reduce War Stomp mana cost from 160→90 (more castable for Knights)
   - Increase Arcane Wave mana cost from 170→200 (more valued for Mages)
   - Create "scaling" cost structure: cost increases 5% per 10 levels
   - Example: Fire Punch costs 15 at level 1, 18 at level 30, 21 at level 60

### LOWER PRIORITY (Quality of Life)

8. **SMOOTH LEVELING CURVE**
   - Ensure spells available every 10-15 levels (currently 20+ gaps)
   - Creates sense of progression and reward
   - Suggested interval: Level 1, 8, 15, 23, 32, 42, 53, 65, 78, 90

9. **REORDER ARCHER SPELL PROGRESSION**
   - Move Piercing Shot to level 15 (before Rangers Remedy at 20)
   - Rangers Remedy moves to level 25 or becomes shared healing spell
   - Restores logical: attack → utility → healing progression

10. **IMPLEMENT SOULFIGHT MECHANICS FOR MELEE CLASSES**
    - Soul currently only used for kick cooldown (noPongKickTime)
    - Add soul consumption for special attacks (Knights could use soul for low-cost ability spam)
    - Example: "Soul Strike" costs 20 soul instead of 100 mana, 6-second cooldown
    - Gives Knights meaningful spell gameplay without mana redesign

---

## Summary: Vocation Balance Status

### By Completeness
- ✅ **COMPLETE:** Mage, Archer, Knight (have spells, though incomplete)
- ⚠️ **PARTIAL:** Promotions (spells exist but not differentiated)
- ❌ **BROKEN:** Occultist, Blood Mage, Heretic (zero spell progression)

### By Power Viability
- ✅ **Viable:** Mage, Archmage, Archer, Marksman, Beastmaster
- ⚠️ **Limited:** Necromancer, Knight, Templar, Death Knight (designed for specific playstyles)
- ❌ **Unviable:** Occultist, Blood Mage, Heretic (cannot cast outside Fire Punch)

### By Identity Clarity
- ✅ **Clear:** Mage (damage), Archer (ranged), Knight (tank)
- ⚠️ **Fuzzy:** Archmage vs. Necromancer, Marksman vs. Beastmaster, Templar vs. Death Knight, Blood Mage vs. Heretic (identical spell access)
- ❌ **Undefined:** Occultist (unclear role, no spells)

---

## Technical Implementation Notes

### Files to Modify
1. `server/data/spells/spells.xml` - Add missing spells, adjust costs, differentiate promotions
2. `server/data/XML/vocations.xml` - Adjust mana multipliers, HP growth, mana generation
3. Create spell scripts in `server/data/spells/` for each new ability

### Testing Checklist
- [ ] All 12 vocations have spells at levels 1, 25, 50, 75, 100
- [ ] No level gaps exceed 15 levels
- [ ] Each promotion has 3+ unique spells (not shared with other promotion)
- [ ] Knight mana costs allow 2+ casts per full mana pool
- [ ] Occultist line has complete progression (minimum 5 spells each)
- [ ] Promotion spells unlock at level 50+
- [ ] Stat scaling matches role identity (tanks > DPS in HP, mages > knights in mana)

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-16  
**Review Status:** Ready for Team Implementation
