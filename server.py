from flask import Flask, render_template, request

from Mortgage import Mortgage
from utils_mortgage_calc import create_line_plot


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("home.html", title="Mortgage Information Form")
    elif request.method == "POST":
        downpayment = float(request.form.get("downpaymentPercent"))
        houseprice = float(request.form.get("houseprice"))
        annualInterestRate = float(request.form.get("annualInterestRate"))
        amortPeriod = int(request.form.get("amortPeriod"))
        months = [i+1 for i in range(amortPeriod*12)]

        mortgageInfo = Mortgage(housePrice=houseprice,
                                downpaymentPercent=downpayment,
                                annualInterestRate=annualInterestRate,
                                paidOverYears=amortPeriod)

        paymentDetails = [i for i in zip(
            months,
            mortgageInfo.mortgagePerMonth,
            mortgageInfo.monthlyContributionsToPrincipal,
            mortgageInfo.monthlyContributionsToPrincipalPercentages
            )]
        line_graph = create_line_plot(mortgageInfo)

        return render_template("basic_table.html", title="Mortgage Payment Details Breakdown",
                               housePrice=houseprice,
                               downPayment=mortgageInfo.downpayment,
                               amortizationPeriod=amortPeriod,
                               annualIR=annualInterestRate,
                               mortgageInfo=paymentDetails,
                               line_plot=line_graph
                               )
    else:
        return "<h1>Something Wrong!</h1>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
