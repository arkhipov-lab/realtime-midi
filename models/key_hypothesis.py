from dataclasses import dataclass


@dataclass
class KeyHypothesis:
    tonic_pc: int
    mode: str  # 'major' | 'minor'
    score: int
    
    