"""
Genome - Sistema de genètica

Implementa genomes, gens, i herència genètica per organismes
"""
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
import random
import numpy as np


@dataclass
class Gene:
    """
    Un gen individual amb alels dominants i recessius
    """
    name: str
    allele_1: float  # Primer alel (0.0 - 1.0)
    allele_2: float  # Segon alel (0.0 - 1.0)

    @property
    def expression(self) -> float:
        """
        Expressió fenotípica del gen (com es manifesta)

        Usa dominància parcial: promig ponderat dels alels
        """
        # Promig simple (co-dominància)
        return (self.allele_1 + self.allele_2) / 2.0

    def mutate(self, mutation_rate: float = 0.01, mutation_strength: float = 0.1) -> 'Gene':
        """
        Crea una còpia mutada del gen

        Args:
            mutation_rate: Probabilitat de mutació (0-1)
            mutation_strength: Força de la mutació

        Returns:
            Nou gen (possiblement mutat)
        """
        new_allele_1 = self.allele_1
        new_allele_2 = self.allele_2

        # Muta alel 1
        if random.random() < mutation_rate:
            change = random.gauss(0, mutation_strength)
            new_allele_1 = np.clip(new_allele_1 + change, 0.0, 1.0)

        # Muta alel 2
        if random.random() < mutation_rate:
            change = random.gauss(0, mutation_strength)
            new_allele_2 = np.clip(new_allele_2 + change, 0.0, 1.0)

        return Gene(self.name, new_allele_1, new_allele_2)


class Genome:
    """
    Genoma complet d'un organisme

    Conté múltiples gens que determinen les seves característiques
    """

    def __init__(self, genes: Optional[Dict[str, Gene]] = None):
        """
        Args:
            genes: Diccionari de gens (nom -> Gene)
        """
        self.genes: Dict[str, Gene] = genes or {}

    def get_trait(self, gene_name: str, default: float = 0.5) -> float:
        """
        Obté el valor expressat d'un gen

        Args:
            gene_name: Nom del gen
            default: Valor per defecte si el gen no existeix

        Returns:
            Valor del tret (0.0 - 1.0)
        """
        if gene_name in self.genes:
            return self.genes[gene_name].expression
        return default

    def set_gene(self, gene_name: str, allele_1: float, allele_2: float):
        """Estableix un gen en el genoma"""
        self.genes[gene_name] = Gene(gene_name, allele_1, allele_2)

    def mutate(self, mutation_rate: float = 0.01) -> 'Genome':
        """
        Crea una còpia mutada del genoma

        Args:
            mutation_rate: Probabilitat de mutació per gen

        Returns:
            Nou genoma mutat
        """
        new_genes = {}
        for name, gene in self.genes.items():
            new_genes[name] = gene.mutate(mutation_rate)

        return Genome(new_genes)

    @staticmethod
    def crossover(parent1: 'Genome', parent2: 'Genome') -> 'Genome':
        """
        Crea un fill combinant els genomes de dos pares

        Usa recombinació mendeliana: cada gen hereta un alel de cada pare

        Args:
            parent1: Primer pare
            parent2: Segon pare

        Returns:
            Genoma del fill
        """
        child_genes = {}

        # Combina tots els gens dels pares
        all_gene_names = set(parent1.genes.keys()) | set(parent2.genes.keys())

        for gene_name in all_gene_names:
            # Obté els gens dels pares (o crea valors per defecte)
            gene1 = parent1.genes.get(gene_name, Gene(gene_name, 0.5, 0.5))
            gene2 = parent2.genes.get(gene_name, Gene(gene_name, 0.5, 0.5))

            # El fill hereta un alel de cada pare (seleccionat aleatòriament)
            allele_from_parent1 = gene1.allele_1 if random.random() < 0.5 else gene1.allele_2
            allele_from_parent2 = gene2.allele_1 if random.random() < 0.5 else gene2.allele_2

            child_genes[gene_name] = Gene(gene_name, allele_from_parent1, allele_from_parent2)

        return Genome(child_genes)

    @staticmethod
    def random(gene_names: List[str]) -> 'Genome':
        """
        Crea un genoma aleatori

        Args:
            gene_names: Llista de noms de gens a generar

        Returns:
            Genoma amb gens aleatoris
        """
        genes = {}
        for name in gene_names:
            allele_1 = random.random()
            allele_2 = random.random()
            genes[name] = Gene(name, allele_1, allele_2)

        return Genome(genes)

    def to_dict(self) -> Dict:
        """Serialitza el genoma a diccionari"""
        return {
            'genes': {
                name: {
                    'allele_1': gene.allele_1,
                    'allele_2': gene.allele_2
                }
                for name, gene in self.genes.items()
            }
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Genome':
        """Deserialitza un genoma des de diccionari"""
        genes = {}
        for name, gene_data in data['genes'].items():
            genes[name] = Gene(
                name,
                gene_data['allele_1'],
                gene_data['allele_2']
            )
        return Genome(genes)


# Gens predefinits per animals
ANIMAL_GENES = [
    'size',              # Mida (0=petit, 1=gran)
    'speed',             # Velocitat
    'strength',          # Força
    'intelligence',      # Intel·ligència
    'aggression',        # Agressivitat
    'sociability',       # Sociabilitat (vida en grup)
    'fertility',         # Fertilitat (descendència)
    'longevity',         # Esperança de vida
    'camouflage',        # Camuflatge
    'venom',             # Verí/toxicitat
    'cold_resistance',   # Resistència al fred
    'heat_resistance',   # Resistència a la calor
    'carnivore',         # Carnívor (0=herbívor, 1=carnívor)
]

# Gens predefinits per plantes
PLANT_GENES = [
    'height',            # Altura
    'growth_rate',       # Velocitat de creixement
    'seed_production',   # Producció de llavors
    'root_depth',        # Profunditat de les arrels
    'drought_resistance', # Resistència a la sequera
    'cold_resistance',   # Resistència al fred
    'toxicity',          # Toxicitat (defensa)
    'fruit_size',        # Mida del fruit
]
