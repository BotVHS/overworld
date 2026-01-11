"""
Ecosystem - Gestió d'ecosistemes i poblacions

Gestiona poblacions d'espècies distribuïdes pel món
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import random
from .species import Species, AnimalSpecies, PlantSpecies, SpeciesFactory
from ..world.world import World


@dataclass
class Population:
    """Població d'una espècie en un tile"""
    species: Species
    count: int = 0
    biomass: float = 0.0  # Biomassa total (kg)

    def update_biomass(self):
        """Actualitza la biomassa segons el compte"""
        # Biomassa aproximada segons mida de l'espècie
        if self.species.species_type.value == "animal":
            size = self.species.base_genome.get_trait('size', 0.5)
            avg_weight = 1 + size * 499  # 1-500 kg per individu
            self.biomass = self.count * avg_weight
        else:  # Planta
            height = self.species.base_genome.get_trait('height', 0.5)
            avg_weight = 0.1 + height * 99.9  # 0.1-100 kg per planta
            self.biomass = self.count * avg_weight


class EcosystemManager:
    """
    Gestiona tots els ecosistemes del món

    Distribueix espècies pel món i gestiona les seves poblacions
    """

    def __init__(self, world: World):
        """
        Args:
            world: Món on col·locar les espècies
        """
        self.world = world
        self.species: List[Species] = []

        # Poblacions per tile: {(x, y): [Population, ...]}
        self.populations: Dict[tuple, List[Population]] = {}

    def add_species(self, species: Species):
        """Afegeix una espècie al món"""
        self.species.append(species)

    def populate_world(self):
        """
        Pobla el món amb totes les espècies registrades

        Distribueix cada espècie segons les seves preferències d'hàbitat
        """
        print(f"Poblant món amb {len(self.species)} espècies...")

        for species in self.species:
            self._populate_species(species)

        # Calcula estadístiques
        total_populations = sum(len(pops) for pops in self.populations.values())
        total_individuals = sum(
            sum(pop.count for pop in pops)
            for pops in self.populations.values()
        )

        print(f"  ✓ {total_populations} poblacions creades")
        print(f"  ✓ {total_individuals} individus totals")

    def _populate_species(self, species: Species):
        """
        Pobla una espècie específica pel món

        Args:
            species: Espècie a poblar
        """
        tiles_populated = 0
        total_individuals = 0

        # Recorre tots els tiles
        for y in range(self.world.height):
            for x in range(self.world.width):
                tile = self.world.get_tile(x, y)

                # Comprova si l'espècie pot viure aquí
                if not species.is_habitable(tile.biome, tile.temperature, tile.humidity):
                    continue

                # Calcula fitness (com de bé s'adapta)
                fitness = species.get_fitness(tile.biome, tile.temperature, tile.humidity)

                # Probabilitat de colonitzar basat en fitness
                if random.random() < fitness * 0.5:  # Màxim 50% dels tiles habitables
                    # Població inicial basada en fitness
                    base_pop = species.base_population
                    population_count = int(base_pop * fitness * random.uniform(0.5, 1.5))

                    if population_count > 0:
                        # Crea població
                        pop = Population(species=species, count=population_count)
                        pop.update_biomass()

                        # Afegeix al tile
                        tile_key = (x, y)
                        if tile_key not in self.populations:
                            self.populations[tile_key] = []

                        self.populations[tile_key].append(pop)

                        tiles_populated += 1
                        total_individuals += population_count

        print(f"    {species.name}: {total_individuals} individus en {tiles_populated} tiles")

    def get_populations_at(self, x: int, y: int) -> List[Population]:
        """
        Obté totes les poblacions en un tile

        Args:
            x, y: Coordenades del tile

        Returns:
            Llista de poblacions (pot ser buida)
        """
        return self.populations.get((x, y), [])

    def get_statistics(self) -> Dict:
        """Obté estadístiques globals de l'ecosistema"""
        stats = {
            'total_species': len(self.species),
            'animal_species': sum(1 for s in self.species if s.species_type.value == "animal"),
            'plant_species': sum(1 for s in self.species if s.species_type.value == "plant"),
            'total_populations': sum(len(pops) for pops in self.populations.values()),
            'total_individuals': sum(
                sum(pop.count for pop in pops)
                for pops in self.populations.values()
            ),
            'total_biomass': sum(
                sum(pop.biomass for pop in pops)
                for pops in self.populations.values()
            ),
        }

        # Estadístiques per espècie
        species_stats = []
        for species in self.species:
            count = sum(
                pop.count
                for pops in self.populations.values()
                for pop in pops
                if pop.species.id == species.id
            )
            biomass = sum(
                pop.biomass
                for pops in self.populations.values()
                for pop in pops
                if pop.species.id == species.id
            )
            species_stats.append({
                'name': species.name,
                'type': species.species_type.value,
                'count': count,
                'biomass': biomass
            })

        stats['species_details'] = sorted(species_stats, key=lambda x: x['count'], reverse=True)

        return stats


def create_default_ecosystem(world: World) -> EcosystemManager:
    """
    Crea un ecosistema amb espècies per defecte

    Args:
        world: Món a poblar

    Returns:
        EcosystemManager amb espècies predefinides
    """
    ecosystem = EcosystemManager(world)

    # Afegeix plantes
    ecosystem.add_species(SpeciesFactory.create_grass())
    ecosystem.add_species(SpeciesFactory.create_oak_tree())
    ecosystem.add_species(SpeciesFactory.create_cactus())

    # Afegeix animals herbívors
    ecosystem.add_species(SpeciesFactory.create_deer())
    ecosystem.add_species(SpeciesFactory.create_rabbit())

    # Afegeix depredadors
    ecosystem.add_species(SpeciesFactory.create_wolf())

    # Pobla el món
    ecosystem.populate_world()

    return ecosystem
