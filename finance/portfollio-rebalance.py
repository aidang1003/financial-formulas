class PortfolioRebalance():
    def __init__(self, ethAmount, usdAmount, rebalancePercentage):
        # Take in the Eth Amount, USD amount and desired rebalance percentage in ETH/(eth+USD)
        self.ethAmount = ethAmount
        self.usdAmount = usdAmount
        self.rebalancePercentage = rebalancePercentage
        self.currentPercentage = self.ethAmount / (self.ethAmount + self.usdAmount)

    def __repr__(self):
        return "eth amount >> ${0}, USD amount ${1}".format(self.ethAmount, self.usdAmount)

    def rebalanceYesOrNo(self, slipPercentage=.05):
        # Returns true when the balance is outside of a given percentage
        if self.currentPercentage - self.rebalancePercentage > slipPercentage or self.currentPercentage - self.rebalancePercentage < slipPercentage:
            self.needsToRebalance = True
            return True
        else:
            return False
        
    def portfolioRebalance(self):
        # Function to rebalance the portfolio
        if self.needsToRebalance == True:
            total = self.usdAmount + self.ethAmount
            self.ethAmount = total * self.rebalancePercentage
            self.usdAmount = total * (1 - self.rebalancePercentage)
            self.needsToRebalance = False
        else:
            pass
        

portfolio = PortfolioRebalance(1500, 1000, .5)
print(portfolio)
var = portfolio.rebalanceYesOrNo()
print(var)
portfolio.portfolioRebalance()
print(portfolio)
