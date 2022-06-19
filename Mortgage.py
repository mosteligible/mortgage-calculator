from constants import PRINCIPALCONTRIBPERCENTAGEDELTA
from utils_mortgage_calc import GetMonthlyMortgage


class Mortgage:
    def __init__(self, housePrice, annualInterestRate, downpaymentPercent,
                 monthlyPrincipalContributionPercent=0.25, paidOverYears=25):
        self.housePrice = housePrice
        self.annualInterestRate = annualInterestRate
        self.monthlyInterestRate = annualInterestRate / 1200
        self.amortizationPeriod = paidOverYears
        self.monthlyPrincipalContributionPercent = monthlyPrincipalContributionPercent
        self.monthsAmortizationPeriod = paidOverYears * 12
        self.downpaymentPercent = downpaymentPercent/100
        self.downpayment = self.downpaymentPercent * housePrice
        self.mortgagePrincipal = housePrice - self.downpayment
        self._calculateMortgages()

    def _calculateMortgages(self):
        self.remainingPrincipal = []
        self.monthlyContributionsToPrincipal = []
        self.mortgagePerMonth = []
        self.monthlyContributionsToPrincipalPercentages = []
        mortgagePrincipal = self.mortgagePrincipal
        monthlyPrincipalContributionPercent = self.monthlyPrincipalContributionPercent
        for month in range(self.monthsAmortizationPeriod, 0, -1):
            self.remainingPrincipal.append(mortgagePrincipal)
            monthlyAmount = GetMonthlyMortgage(
                principal=mortgagePrincipal,
                rate=self.monthlyInterestRate,
                numOfMonths=month
            )

            self.mortgagePerMonth.append(monthlyAmount)
            monthlyPrincipalContribution = monthlyAmount * monthlyPrincipalContributionPercent
            self.monthlyContributionsToPrincipal.append(monthlyPrincipalContribution)

            self.monthlyContributionsToPrincipalPercentages.append(monthlyPrincipalContributionPercent)
            monthlyPrincipalContributionPercent += PRINCIPALCONTRIBPERCENTAGEDELTA/100

    def MortgagePaidPerMonth(self, month=None):
        if month is not None:
            if month > 0 and month <= self.monthsAmortizationPeriod:
                return self.mortgagePerMonth[month-1]
            else:
                raise ValueError(f"{month} is beyond amortization period")
        else:
            return self.mortgagePerMonth

    def MonthlyPrincipalAmount(self, month=None):
        if month is not None:
            if month > 0 and month <= self.monthsAmortizationPeriod:
                return self.monthlyContributionsToPrincipal[month-1]
            else:
                raise ValueError(f"{month} is beyond amortization period")
        else:
            return self.monthlyContributionsToPrincipal

    def JsonData(self):
        return {
            "HousePrice": self.housePrice,
            "DownPayment": self.downpayment,
            "InterestRate": self.annualInterestRate,
            "AmortizationPeriod": self.amortizationPeriod,
            "MonthlyPrincipalPaid": self.monthlyContributionsToPrincipal,
            "MortgagePaidPerMonth": self.mortgagePerMonth,
            "MonthlyContributionToPrincipalPercent": self.monthlyContributionsToPrincipalPercentages
        }
