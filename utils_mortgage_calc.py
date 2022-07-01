import json
from typing import Dict
import plotly.graph_objs as go
import plotly


def GetMonthlyMortgage(principal, rate, numOfMonths) -> float:
    monthly_mortgage = (principal * rate * (1 + rate)**numOfMonths)/((1 + rate)**numOfMonths - 1)
    return monthly_mortgage


def create_line_plot(mortgageInfo) -> Dict:
    N = mortgageInfo.monthsAmortizationPeriod
    x = [i for i in range(1, N + 1)]
    principalContribution = mortgageInfo.monthlyContributionsToPrincipal
    mortgagesPaid = mortgageInfo.mortgagePerMonth
    interestPaid = [mortgagesPaid[indx] - principalContribution[indx] for indx in range(N)]
    data = [
        go.Line(x=x, y=principalContribution),
        #go.Line(x=x, y=mortgagesPaid),
        #go.Line(x=x, y=interestPaid)
    ]

    graphJson = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJson
