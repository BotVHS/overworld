"""
Sistema d'esdeveniments per la simulació
"""
from typing import Dict, List, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


class EventType(Enum):
    """Tipus d'esdeveniments"""
    # Geològics
    EARTHQUAKE = "earthquake"
    VOLCANIC_ERUPTION = "volcanic_eruption"
    TECTONIC_SHIFT = "tectonic_shift"

    # Climàtics
    FLOOD = "flood"
    DROUGHT = "drought"
    HURRICANE = "hurricane"
    BLIZZARD = "blizzard"

    # Biològics
    PLAGUE = "plague"
    SPECIES_EXTINCTION = "species_extinction"
    SPECIES_MIGRATION = "species_migration"

    # Civilització
    CITY_FOUNDED = "city_founded"
    CITY_DESTROYED = "city_destroyed"
    WAR_STARTED = "war_started"
    WAR_ENDED = "war_ended"
    LEADER_CHANGED = "leader_changed"
    POLITICAL_REVOLUTION = "political_revolution"
    RELIGIOUS_SCHISM = "religious_schism"
    TECHNOLOGICAL_BREAKTHROUGH = "technological_breakthrough"

    # Altres
    CUSTOM = "custom"


@dataclass
class Event:
    """Representa un esdeveniment a la simulació"""
    event_type: EventType
    day: int
    year: int
    description: str
    data: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"[Any {self.year}, Dia {self.day}] {self.event_type.value}: {self.description}"


class EventSystem:
    """Sistema de gestió d'esdeveniments"""

    def __init__(self):
        self.events: List[Event] = []
        self.listeners: Dict[EventType, List[Callable]] = {}

        # Històric d'esdeveniments (limitat per memòria)
        self.max_history = 10000

    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        """Subscriu un listener a un tipus d'esdeveniment"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def emit(self, event: Event):
        """Emet un esdeveniment"""
        # Afegeix a l'històric
        self.events.append(event)

        # Limita l'històric
        if len(self.events) > self.max_history:
            self.events = self.events[-self.max_history:]

        # Notifica listeners
        if event.event_type in self.listeners:
            for callback in self.listeners[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error en listener: {e}")

    def get_recent_events(self, count: int = 10) -> List[Event]:
        """Obté els esdeveniments més recents"""
        return self.events[-count:]

    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """Obté tots els esdeveniments d'un tipus"""
        return [e for e in self.events if e.event_type == event_type]

    def get_events_in_range(self, start_year: int, end_year: int) -> List[Event]:
        """Obté esdeveniments en un rang d'anys"""
        return [e for e in self.events if start_year <= e.year <= end_year]

    def clear_history(self):
        """Neteja l'històric d'esdeveniments"""
        self.events.clear()
