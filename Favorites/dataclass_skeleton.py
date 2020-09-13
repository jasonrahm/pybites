from dataclasses import dataclass, field
from typing import List, NamedTuple

Bracket = NamedTuple("Bracket", [("end", int), ("rate", float)])
Taxed = NamedTuple("Taxed", [("amount", float), ("rate", float), ("tax", float)])
BRACKET = [
    Bracket(9_700, 0.1),
    Bracket(39_475, 0.12),
    Bracket(84_200, 0.22),
    Bracket(160_725, 0.24),
    Bracket(204_100, 0.32),
    Bracket(510_300, 0.35),
    Bracket(510_301, 0.37),
]


@dataclass
class Taxes:

    income: float
    bracket: List[Bracket] = field(default_factory=list)

    def __post_init__(self):
        """Initiates default values"""
        if not self.bracket:
            self.bracket = BRACKET
        self.tax_amounts: List[Taxed] = []

    def __str__(self) -> str:

        desc = f"{'Summary Report':^34}\n"
        desc += f"{'=' * 34}\n"
        desc += f"{'Taxable Income':>15}: {self.income:16,.2f}\n"
        desc += f"{'Taxes Owed':>15}: {self.taxes:16,.2f}\n"
        desc += f"{'Tax Rate':>15}: {self.tax_rate:15.2f}%"
        return desc

    def report(self):
        desc = f"{str(self)}\n"
        desc += f"\n{'Taxes Breakdown':^34}\n"
        desc += f"{'=' * 34}\n"
        for tax in self.tax_amounts:
            desc += f"{tax.amount:12,.2f} x {tax.rate:4.2f} = {tax.tax:12,.2f}\n"
        desc += f"{'-' * 34}\n"
        desc += f"{'Total =':>21} {self.taxes:12,.2f}"
        print(desc.rstrip())

    @property
    def taxes(self) -> float:
        previous_ceiling = 0
        remaining_income = self.income
        for i, b in enumerate(self.bracket):
            tier_income = min(remaining_income, b.end - previous_ceiling)
            previous_ceiling += b.end
            tier_tax = round(tier_income * b.rate, 2)
            self.tax_amounts.append(Taxed(tier_income, b.rate, tier_tax))
            remaining_income -= tier_income
            if remaining_income <= 0:
                break
        return self.total

    @property
    def total(self) -> float:
        # if not self.tax_amounts:
        #     return self.taxes
        # else:
        #     return round(sum(t.tax for t in self.tax_amounts), 2)
        return round(sum(t.tax for t in self.tax_amounts), 2)

    @property
    def tax_rate(self) -> float:
        return round((self.total / self.income) * 100, 2)


if __name__ == "__main__":
    salary = float(input("Taxable income: "))
    t = Taxes(salary)
    t.report()