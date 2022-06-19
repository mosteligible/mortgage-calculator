def GetMonthlyMortgage(principal, rate, numOfMonths):
    monthly_mortgage = (principal * rate * (1 + rate)**numOfMonths)/((1 + rate)**numOfMonths - 1)
    return monthly_mortgage
