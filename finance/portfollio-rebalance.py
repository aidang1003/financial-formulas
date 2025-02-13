class PortfolioRebalance():
    def __init__(self, ethAmount, ethPrice, usdAmount, maxPrice, rebalanceSlippage):
        self.ethAmount = ethAmount # eth amount in eth
        self.ethPrice = ethPrice # eth price in usd
        self.usdAmount = usdAmount # usd amount in usd
        self.maxPrice = maxPrice # Max expected price of eth
        self.rebalancePercentage = 1 - ((1 / (self.maxPrice ** 2)) * (self.ethPrice ** 2)) # Calculate rebalance percentage based on price
        self.rebalanceSlippage = rebalanceSlippage # The percent slippage at which a rebalance happens automatically
        self.currentPercentage = (self.ethAmount * self.ethPrice) / ((self.ethAmount * self.ethPrice) + self.usdAmount)


    def __repr__(self):
        return "eth amount >> ${0}, USD amount >> ${1}\n Rebalance Percentage Eth/USD >> {2}".format(self.ethAmount * self.ethPrice, self.usdAmount, self.rebalancePercentage)

    def rebalanceYesOrNo(self):
        # Returns true when the balance is outside of a given percentage
        if self.currentPercentage - self.rebalancePercentage > self.rebalanceSlippage or self.currentPercentage - self.rebalancePercentage < self.rebalanceSlippage:
            self.needsToRebalance = True
            print("determined there needs to be a rebalance")
            return True
        else:
            return False
        
    def portfolioRebalance(self):
        # Function to rebalance the portfolio
        if self.needsToRebalance == True:
            total = self.usdAmount + (self.ethAmount * self.ethPrice)
            self.ethAmount = total * self.rebalancePercentage / self.ethPrice
            self.usdAmount = total * (1 - self.rebalancePercentage)
            self.needsToRebalance = False
            print("Rebalancing portfolio")
        else:
            pass

    def increaseEthPrice(self, priceIncrease=.05):
        # Takes as input the amount you want to increase the eth price
        self.ethPrice = self.ethPrice * (1 + priceIncrease)
        print("Increasing Eth price")

    def reCalculateRebalancePercentage(self, maxPrice=12500, factor=2):
        # Calculate the new rebalance percentage
        # Take the existing variables and a max price into account using formula in allocation.py
        self.maxPrice = maxPrice
        self.formattingValue = 1 / (self.maxPrice ** factor)
        self.rebalancePercentage = 1 - (self.formattingValue * (self.ethPrice ** factor))
        print("Calculating portfolio percentage")
        return


class SimulateEthPriceMovement():
    def allocationLevelsMax(self, maximumAmount):
        # return allocation levels in a list
        returnList = []
        while maximumAmount > 0:
            returnList.append(round(maximumAmount, 2))
            maximumAmount = maximumAmount * (1 - self.rebalanceSlippage)
            if maximumAmount < 100:
                maximumAmount = 0
        return returnList
    

portfolio = PortfolioRebalance(10, 3000, 5000, 12500, .02)
print(portfolio)
portfolio.rebalanceYesOrNo()
portfolio.portfolioRebalance()
print(portfolio)
portfolio.increaseEthPrice(.05)
portfolio.reCalculateRebalancePercentage()
portfolio.rebalanceYesOrNo()
portfolio.portfolioRebalance()
print(portfolio)
