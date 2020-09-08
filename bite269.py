"""Tax Bracket Calculator

Here is the break-down on how much a US citizen's income was
taxed in 2019

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
TAX_AMOUNTS = []

class Taxes:
    """Taxes class

    Given a taxable income and optional tax bracket, it will
    calculate how much taxes are owed to Uncle Sam.

    """
    def __init__(self, salary: float):
        self.salary: float = salary
        self.tax: float = 0
        self.rate: float = 0

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
        msg = (
            '         Summary Report           \n'
            '==================================\n'
            f' Taxable Income: {self.salary:>17,.2f}\n'
            f'     Taxes Owed: {self.tax:>17,.2f}\n'
            f'       Tax Rate: {self.rate:>17.2%}'
        )
        return msg

    def report(self):
        """Prints taxes breakdown report"""
        self.tax = self.taxes()
        self.rate = self.tax_rate(self.tax)

        msg = (
            '         Summary Report           \n'
            '==================================\n'
            f' Taxable Income: {self.salary:>17,.2f}\n'
            f'     Taxes Owed: {self.tax:>17,.2f}\n'
            f'       Tax Rate: {self.rate:>17.2%}\n\n'
            '         Taxes Breakdown          \n'
            '==================================\n'
        )
        for tax in TAX_AMOUNTS:
            msg += f"{tax.amount:>12,.2f} x {tax.rate:4.2f} = {tax.tax:>12,.2f}\n"

        msg += '----------------------------------\n'
        msg += f'              Total = {self.tax:>12,.2f}'
        return print(msg)

    def taxes(self) -> float:
        """Calculates the taxes owed

        As it's calculating the taxes, it is also populating the tax_amounts list
        which stores the Taxed named tuples.

        Returns:
            float -- The amount of taxes owed
        """
        remaining_income = self.salary
        previous_ceiling = 0
        for current_ceiling, tax in BRACKET:
            tier_income = min(remaining_income, current_ceiling - previous_ceiling)
            previous_ceiling += current_ceiling
            tier_tax = tier_income * tax
            TAX_AMOUNTS.append(Taxed(tier_income, tax, tier_tax))
            remaining_income -= tier_income
            if remaining_income <= 0:
                break
        return self.total()

    def total(self) -> float:
        """Calculates total taxes owed

        Returns:
            float -- Total taxes owed
        """

        total_tax = 0
        for taxes in TAX_AMOUNTS:
            total_tax += taxes.tax
        return total_tax

    def tax_rate(self, taxes) -> float:
        """Calculates the actual tax rate

        Returns:
            float -- Tax rate
        """
        return taxes / self.salary


if __name__ == "__main__":
    salary = 40_000
    t = Taxes(salary)
    t.report()