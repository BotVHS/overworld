"""
Gestor de temps de la simulació
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SimulationTime:
    """Representa el temps a la simulació"""
    day: int = 1
    year: int = 1

    def __post_init__(self):
        self.days_per_year = 365

    @property
    def total_days(self) -> int:
        """Total de dies transcorreguts"""
        return (self.year - 1) * self.days_per_year + self.day

    @property
    def season(self) -> str:
        """Estació actual (simplificat a 4 estacions)"""
        day_in_year = self.day
        if day_in_year <= 91:
            return "Primavera"
        elif day_in_year <= 182:
            return "Estiu"
        elif day_in_year <= 273:
            return "Tardor"
        else:
            return "Hivern"

    def advance(self, days: int = 1):
        """Avança el temps"""
        self.day += days
        while self.day > self.days_per_year:
            self.day -= self.days_per_year
            self.year += 1

    def __str__(self) -> str:
        return f"Any {self.year}, Dia {self.day} ({self.season})"


class TimeManager:
    """Gestiona el temps i la velocitat de la simulació"""

    def __init__(self, days_per_year: int = 365):
        self.time = SimulationTime()
        self.time.days_per_year = days_per_year

        self.speed = 1  # Multiplicador de velocitat
        self.paused = False

        self.tick_count = 0
        self.accumulated_time = 0.0

    def update(self, delta_time: float) -> int:
        """
        Actualitza el gestor de temps

        Args:
            delta_time: Temps transcorregut en segons (temps real)

        Returns:
            Nombre de ticks (dies) a simular aquest frame
        """
        if self.paused:
            return 0

        self.accumulated_time += delta_time * self.speed

        # 1 tick = 1 dia simulat
        ticks_to_simulate = int(self.accumulated_time)
        self.accumulated_time -= ticks_to_simulate

        if ticks_to_simulate > 0:
            self.time.advance(ticks_to_simulate)
            self.tick_count += ticks_to_simulate

        return ticks_to_simulate

    def set_speed(self, speed: int):
        """Estableix la velocitat de simulació"""
        self.speed = max(1, min(speed, 10000))

    def toggle_pause(self):
        """Alterna entre pausa i reproducció"""
        self.paused = not self.paused

    def __str__(self) -> str:
        status = "PAUSA" if self.paused else f"{self.speed}x"
        return f"{self.time} [{status}]"
