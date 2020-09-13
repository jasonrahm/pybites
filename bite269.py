"""Tax Bracket Calculator

Here is the break-down on how much a US citizen's income was
taxed in 2019.

      $0 - $9,700   10%
  $9,701 - $39,475  12%
 $39,476 - $84,200  22%
 $84,201 - $160,725 24%
$160,726 - $204,100 32%
$204,101 - $510,300 35%
$510,301 +          37%

For example someone earning $40,000 would
pay $4,658.50, not $40,000 x 22% = $8,800!

    9,700.00 x 0.10 =       970.00
   29,775.00 x 0.12 =     3,573.00
      525.00 x 0.22 =       115.50
----------------------------------
              Total =     4,658.50

More detail can be found here:
https://www.nerdwallet.com/blog/taxes/federal-income-tax-brackets/

Sample output from running the code in the if/main clause:

          Summary Report
==================================
 Taxable Income:        40,000.00
     Taxes Owed:         4,658.50
       Tax Rate:           11.65%

         Taxes Breakdown
==================================
    9,700.00 x 0.10 =       970.00
   29,775.00 x 0.12 =     3,573.00
      525.00 x 0.22 =       115.50
----------------------------------
              Total =     4,658.50
"""
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
    """Taxes class

    Given a taxable income and optional tax bracket, it will
    calculate how much taxes are owed to Uncle Sam.

    """

    income: float
    bracket: List[Bracket] = field(default_factory=list)

    def __post_init__(self):
        """Initiates default values"""
        if not self.bracket:
            self.bracket = BRACKET
        self.tax_amounts: List[Taxed] = []

    def __str__(self) -> str:
        """Summary Report

        Returns:
            str -- Summary report

            Example:

                      Summary Report
            ==================================
             Taxable Income:        40,000.00
                 Taxes Owed:         4,658.50
                   Tax Rate:           11.65%
        """
        desc = f"{'Summary Report':^34}\n"
        desc += f"{'=' * 34}\n"
        desc += f"{'Taxable Income':>15}: {self.income:16,.2f}\n"
        desc += f"{'Taxes Owed':>15}: {self.taxes:16,.2f}\n"
        desc += f"{'Tax Rate':>15}: {self.tax_rate:15.2f}%"
        return desc

    def _record(self, amount: float, rate: float):
        """Helper function to record tax amounts and rates

        Arguments:
            amount {float} -- Amount being taxed
            rate {float} -- The rate that the amount is being taxed at
        """
        taxed = round(amount * rate, 2)
        t = Taxed(amount, rate, taxed)
        self.tax_amounts.append(t)

    def report(self):
        """Prints taxes breakdown report"""
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
        """Calculates the taxes owed

        As it's calculating the taxes, it is also populating the tax_amounts list
        which stores the Taxed named tuples.

        Returns:
            float -- The amount of taxes owed
        """
        if not self.tax_amounts:
            for n, b in enumerate(self.bracket):
                # if the taxable income is less than the first bracket
                # tax the income amount and break out of the loop
                if n == 0:
                    if self.income > b.end:
                        self._record(b.end, b.rate)
                    else:
                        self._record(self.income, b.rate)
                        break
                # if we've gotten to the last bracket just tax the amount
                # that's above it
                elif n == len(self.bracket) - 1:
                    amount = self.income - self.bracket[n - 1].end
                    self._record(amount, b.rate)
                else:
                    # check to see if the taxable income is below the end
                    # of the current bracket and tax that amount
                    if self.income <= b.end:
                        amount = self.income - self.bracket[n - 1].end
                    else:
                        amount = b.end - self.bracket[n - 1].end
                    self._record(amount, b.rate)
                    # if the taxable income is below the end of the current
                    # bracket break out of the loop
                    if self.income <= b.end:
                        break
        return self.total

    @property
    def total(self) -> float:
        """Calculates total taxes owed

        Returns:
            float -- Total taxes owed
        """
        if not self.tax_amounts:
            return self.taxes
        else:
            return round(sum(t.tax for t in self.tax_amounts), 2)

    @property
    def tax_rate(self) -> float:
        """Calculates the actual tax rate

        Returns:
            float -- Tax rate
        """
        return round((self.total / self.income) * 100, 2)


if __name__ == "__main__":
    salary = float(input("Taxable income: "))
    t = Taxes(salary)
    t.report()