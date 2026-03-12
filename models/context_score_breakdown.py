from dataclasses import dataclass


@dataclass
class ContextScoreBreakdown:
    base_score: int
    movement_bonus: int
    functional_bonus: int
    cadence_bonus: int

    @property
    def total_score(self) -> int:
        return self.base_score + self.movement_bonus + self.functional_bonus + self.cadence_bonus
    
