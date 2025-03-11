from relari_otel.specifications import (
    Specifications,
    Scenario,
    Contract,
    Precondition,
    Pathcondition,
    Postcondition,
    Level,
)

tesla_income = Scenario(
    uuid="tesla_income",
    name="Tesla Income",
    data="How has Tesla's net income changed over the last five years?",
    contracts=[
        Contract(
            uuid="ctr-tsla-income",
            name="Right Tickers",
            requirements=[
                Precondition("Question about Tesla's net income"),
                Postcondition(
                    "A numeric value for net income expressed in dollars",
                    on="output",
                    level=Level.SHOULD,
                ),
                Pathcondition("Retrieve Tesla's net income with the ticker TSLA"),
            ],
        )
    ],
)


nike_vs_adidas = Scenario(
    uuid="nike_vs_adidas",
    name="Nike vs Adidas",
    data="Between Nike and Adidas, which company has stronger operating margins?",
    contracts=[
        Contract(
            uuid="ctr-nike-vs-adidas",
            name="Right Tickers",
            requirements=[
                Precondition("Comparison between Nike and Adidas"),
                Pathcondition("Retrieve Nike financials with the ticker NKE"),
                Pathcondition("Retrieve Adidas financials with the ticker ADDYY"),
                Postcondition(
                    "A numeric value for operating margins expressed in percentage",
                    on="output",
                    level=Level.SHOULD,
                ),
            ],
        )
    ],
)

de_ratio = Scenario(
    uuid="de_ratio",
    name="Debt-to-Equity Ratio",
    data="Which car manufacturer has the highest debt-to-equity ratio right now?",
    contracts=[
        Contract(
            uuid="ctr-de-ratio",
            name="Right Tickers",
            requirements=[
                Precondition("Question about the debt-to-equity ratio"),
                Postcondition("Output a table", on="output"),
                Postcondition(
                    "Include at least Tesla, Ford, and General Motors",
                    on="output",
                    level=Level.SHOULD,
                ),
                Pathcondition(
                    "Retrieve the financials of at least 3 car manufacturers"
                ),
            ],
        )
    ],
)

spec = Specifications(scenarios=[tesla_income, nike_vs_adidas, de_ratio])

spec.save("specifications.json")
