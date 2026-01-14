#!/usr/bin/env python3
"""
Test del sistema de diplomàcia i guerra

Demostra:
- Relacions diplomàtiques entre civilitzacions
- Tractats (pau, comerç, aliances)
- Declaracions de guerra
- Batalles i forces militars
- Finalització de guerres
"""
import sys
from overworld.world.world import World
from overworld.civilization.civilization import create_civilizations
from overworld.civilization.diplomacy import (
    DiplomacySystem,
    RelationshipType,
    TreatyType
)
from overworld.civilization.warfare import (
    WarfareSystem
)


def main():
    """Test de diplomàcia i guerra"""
    print("=" * 80)
    print("  TEST DE DIPLOMÀCIA I GUERRA")
    print("=" * 80)
    print()

    # Genera un món petit
    print("Generant món 150x150...")
    world = World(width=150, height=150, seed=42)
    world.generate(island_mode=False, num_rivers=10)
    print()

    # Crea civilitzacions
    print("Creant civilitzacions...")
    civ_manager = create_civilizations(world, count=5)
    print()

    # === FASE 1: INICIALITZACIÓ DIPLOMÀTICA ===
    print("=" * 80)
    print("FASE 1: ESTABLIMENT DE RELACIONS DIPLOMÀTIQUES")
    print("=" * 80)
    print()

    diplomacy = DiplomacySystem()
    warfare = WarfareSystem(diplomacy)

    civs = civ_manager.civilizations
    civ_names = [civ.name for civ in civs]

    # Estableix relacions inicials
    print("Establint relacions inicials entre civilitzacions:")
    print()

    # Aliança entre Civ 0 i Civ 1
    diplomacy.set_relationship(civ_names[0], civ_names[1], RelationshipType.FRIENDLY, 60)
    print(f"🤝 {civ_names[0]} ↔ {civ_names[1]}: Amistós (opinió: +60)")

    # Rivalitat entre Civ 2 i Civ 3
    diplomacy.set_relationship(civ_names[2], civ_names[3], RelationshipType.HOSTILE, -70)
    print(f"⚔️  {civ_names[2]} ↔ {civ_names[3]}: Hostil (opinió: -70)")

    # Neutral entre altres
    for i in range(len(civ_names)):
        for j in range(i+1, len(civ_names)):
            if (i, j) not in [(0, 1), (2, 3)]:
                diplomacy.set_relationship(civ_names[i], civ_names[j], RelationshipType.NEUTRAL, 0)

    print()

    # === FASE 2: SIGNATURA DE TRACTATS ===
    print()
    print("=" * 80)
    print("FASE 2: SIGNATURA DE TRACTATS")
    print("=" * 80)
    print()

    # Tractat comercial entre Civ 0 i Civ 4
    trade_treaty = diplomacy.sign_treaty(
        treaty_type=TreatyType.TRADE_AGREEMENT,
        participants=[civ_names[0], civ_names[4]],
        year=100,
        duration_years=50,
        terms={'tariff_reduction': 50}
    )
    print(f"📜 Tractat comercial signat:")
    print(f"   Participants: {', '.join(trade_treaty.participants)}")
    print(f"   Duració: {trade_treaty.duration_years} anys")
    print()

    # Aliança militar entre Civ 0 i Civ 1
    alliance_treaty = diplomacy.sign_treaty(
        treaty_type=TreatyType.MILITARY_ALLIANCE,
        participants=[civ_names[0], civ_names[1]],
        year=100,
        duration_years=-1,  # Permanent
        terms={'mutual_defense': True}
    )
    print(f"🛡️  Aliança militar signada:")
    print(f"   Participants: {', '.join(alliance_treaty.participants)}")
    print(f"   Duració: Permanent")
    print()

    # === FASE 3: REGISTRE DE FORCES MILITARS ===
    print()
    print("=" * 80)
    print("FASE 3: FORCES MILITARS")
    print("=" * 80)
    print()

    print("Registrant forces militars:")
    print()

    for i, civ in enumerate(civs):
        # Força militar basada en cultura militarista
        base_soldiers = 500 + int(civ.culture.militarism * 5)
        morale = 50 + int(civ.culture.militarism / 4)

        force = warfare.register_military_force(
            civilization_name=civ.name,
            soldiers=base_soldiers,
            tech_level=civ.tech_level,
            morale=morale,
            experience=0
        )

        strength = force.get_military_strength()
        print(f"  ⚔️  {civ.name}:")
        print(f"      Soldats: {force.soldiers:,}")
        print(f"      Nivell tècnic: {force.tech_level}/8")
        print(f"      Moral: {force.morale}/100")
        print(f"      Força total: {strength:.0f}")
        print()

    # === FASE 4: DECLARACIÓ DE GUERRA ===
    print()
    print("=" * 80)
    print("FASE 4: DECLARACIÓ DE GUERRA")
    print("=" * 80)
    print()

    # Civ 2 declara guerra a Civ 3 (ja són hostils)
    aggressor = civ_names[2]
    defender = civ_names[3]

    print(f"⚔️  {aggressor} declara guerra a {defender}!")
    print(f"   Casus belli: Disputa territorial")
    print()

    war = warfare.start_war(
        aggressor=aggressor,
        defender=defender,
        year=105,
        casus_belli="Disputa territorial"
    )

    print(f"   Guerra ID: {war.war_id}")
    print(f"   Any d'inici: {war.year_started}")
    print(f"   Estat: {war.status.value}")
    print()

    # === FASE 5: SIMULACIÓ DE BATALLES ===
    print()
    print("=" * 80)
    print("FASE 5: BATALLES")
    print("=" * 80)
    print()

    locations = ["Frontera Nord", "Vall Central", "Pas de Muntanya", "Planura Est"]

    print(f"Simulant 4 batalles en la guerra entre {aggressor} i {defender}:")
    print()

    for i, location in enumerate(locations, 1):
        year = 105 + i
        print(f"Batalla {i} - Any {year} ({location}):")

        battle = warfare.simulate_battle(war, year, location)

        print(f"  {battle.description}")
        print(f"  Victor: {battle.victor}")
        print(f"  Baixes {aggressor}: {battle.attacker_casualties:,}")
        print(f"  Baixes {defender}: {battle.defender_casualties:,}")
        print(f"  Warscore: {war.aggressor_warscore:+d}/100")
        print()

    # Estat de la guerra després de batalles
    print(f"Estat de la guerra després de 4 batalles:")
    print(f"  Estat: {war.status.value}")
    print(f"  Warscore {aggressor}: {war.aggressor_warscore:+d}/100")
    print(f"  Total batalles: {len(war.battles)}")
    print()

    # Forces militars després de batalla
    print(f"Forces militars després de les batalles:")
    aggressor_force = warfare.military_forces[aggressor]
    defender_force = warfare.military_forces[defender]

    print(f"  {aggressor}: {aggressor_force.soldiers:,} soldats (moral: {aggressor_force.morale}/100)")
    print(f"  {defender}: {defender_force.soldiers:,} soldats (moral: {defender_force.morale}/100)")
    print()

    # === FASE 6: PAU I TRACTATS ===
    print()
    print("=" * 80)
    print("FASE 6: FINALITZACIÓ DE LA GUERRA")
    print("=" * 80)
    print()

    print(f"Finalitzant guerra entre {aggressor} i {defender}...")
    print()

    warfare.end_war(war, year=110, terms={'territory_ceded': 'Region Nord'})

    print(f"✅ Guerra finalitzada:")
    print(f"   Duració: {war.get_duration(110)} anys")
    print(f"   Resultat: {war.outcome}")
    print(f"   Estat final: {war.status.value}")
    print()

    # Relació després de la guerra
    relationship = diplomacy.get_relationship(aggressor, defender)
    print(f"Relació després de la guerra:")
    print(f"  Tipus: {relationship.get_relationship_description()}")
    print(f"  Opinió: {relationship.opinion_score}/100")
    print()

    # === FASE 7: ANÀLISI DIPLOMÀTICA ===
    print()
    print("=" * 80)
    print("FASE 7: ANÀLISI DIPLOMÀTICA GLOBAL")
    print("=" * 80)
    print()

    print("Matriu de relacions:")
    print()

    matrix = diplomacy.get_relationship_matrix(civ_names)

    # Capçalera
    print(f"{'':20s}", end='')
    for civ in civ_names[:4]:  # Només 4 per estalviar espai
        print(f"{civ[:8]:>12s}", end='')
    print()
    print("-" * 80)

    for civ1 in civ_names[:4]:
        print(f"{civ1[:20]:20s}", end='')
        for civ2 in civ_names[:4]:
            if civ1 == civ2:
                print(f"{'---':>12s}", end='')
            else:
                rel = matrix[civ1][civ2]
                type_symbol = {
                    'ally': '🤝',
                    'friendly': '😊',
                    'neutral': '😐',
                    'unfriendly': '😠',
                    'hostile': '⚔️',
                    'at_war': '💥'
                }.get(rel['type'], '?')
                text = f"{type_symbol} {rel['opinion']:+3d}"
                print(f"{text:>12s}", end='')
        print()
    print()

    # Poder diplomàtic
    print("Poder diplomàtic per civilització:")
    for civ_name in civ_names:
        diplomatic_power = diplomacy.calculate_diplomatic_power(civ_name, civs)
        allies = diplomacy.get_allies(civ_name, 110)
        enemies = diplomacy.get_enemies(civ_name)

        print(f"  {civ_name}:")
        print(f"    Poder diplomàtic: {diplomatic_power:.1f}/10")
        print(f"    Aliats: {len(allies)} ({', '.join(allies) if allies else 'cap'})")
        print(f"    Enemics: {len(enemies)} ({', '.join(enemies) if enemies else 'cap'})")

    print()

    # Poder militar
    print("Poder militar per civilització:")
    for civ_name in civ_names:
        military_power = warfare.calculate_military_power(civ_name)
        force = warfare.military_forces.get(civ_name)

        if force:
            print(f"  {civ_name}:")
            print(f"    Poder militar: {military_power:.1f}/10")
            print(f"    Soldats: {force.soldiers:,}")
            print(f"    Experiència: {force.experience}/100")

    print()

    # Estadístiques globals
    print("=" * 80)
    print("ESTADÍSTIQUES GLOBALS")
    print("=" * 80)
    print()

    dip_stats = diplomacy.get_statistics()
    war_stats = warfare.get_statistics()

    print("Diplomàcia:")
    print(f"  Total relacions: {dip_stats['total_relationships']}")
    print(f"  Tractats actius: {dip_stats['active_treaties']}")
    print(f"  Tractats trencats: {dip_stats['broken_treaties']}")
    print(f"  Esdeveniments diplomàtics: {dip_stats['diplomatic_events']}")
    print()

    print("Guerra:")
    print(f"  Total guerres: {war_stats['total_wars']}")
    print(f"  Guerres actives: {war_stats['active_wars']}")
    print(f"  Guerres finalitzades: {war_stats['ended_wars']}")
    print(f"  Total batalles: {war_stats['total_battles']}")
    print()

    print("=" * 80)
    print("Test completat!")
    print()
    print("RESUM:")
    print("  ✓ Relacions diplomàtiques establertes")
    print("  ✓ Tractats signats (comercial, aliança militar)")
    print("  ✓ Forces militars registrades")
    print("  ✓ Guerra declarada amb casus belli")
    print("  ✓ 4 batalles simulades amb baixes realistes")
    print("  ✓ Guerra finalitzada amb tractat de pau")
    print("  ✓ Poder diplomàtic i militar calculat")
    print()
    print("Observacions:")
    print("  - Batalles tenen resultats variables segons força militar")
    print("  - Warscore reflecteix victòries/derrotes acumulades")
    print("  - Baixes redueixen força militar i moral")
    print("  - Tractat de pau millora relació (opinió +30)")
    print("  - Aliances afecten poder diplomàtic")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
