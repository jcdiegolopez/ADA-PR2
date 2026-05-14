from dataclasses import dataclass


@dataclass
class Job:
    job_id: int
    start: int
    finish: int
    weight: float

    def is_compatible(self, other: "Job") -> bool:
        return self.finish <= other.start or other.finish <= self.start

    def __repr__(self) -> str:
        return f"Job(id={self.job_id}, s={self.start}, f={self.finish}, w={self.weight})"
