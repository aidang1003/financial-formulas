class PortfolioRebalance():
    def __init__(self, ethAmount, ethPrice, usdAmount, maxPrice, rebalanceSlippage,v=0):
        self.ethAmount = ethAmount # eth amount in eth
        self.ethPrice = ethPrice # eth price in usd
        self.usdAmount = usdAmount # usd amount in usd
        self.maxPrice = maxPrice # Max expected price of eth
        self.rebalanceSlippage = rebalanceSlippage # The percent slippage at which a rebalance happens automatically
        self.v = v # Turns on verbose mode, only use while debugging

        self.factor = 2 # Factor for calculating re-allocation percentage, 1 is linear and a number greater than 1 means as price gets higher more sales will take place
        self.totalPortfolioValue = (self.ethAmount * self.ethPrice) + self.usdAmount
        self.calculateAllocationPercentage()


    def __repr__(self):
        return f"""Total Portfolio Value: ${round(self.totalPortfolioValue, 2)}
    ETH price >> ${round(self.ethPrice, 2)}
    ETH amount in ETH >> {round(self.ethAmount, 9)}
    ETH amount in USD >> ${round(self.ethAmount * self.ethPrice, 2)}
    USD amount in USD >> ${round(self.usdAmount, 2)}
    Current ETH/USD ratio >> {round(self.currentPercentage * 100, 2)}%
    Desired ETH/USD ratio >> {round(self.rebalancePercentage * 100, 2)}%"""

    def rebalanceYesOrNo(self):
        # Returns true when the balance is outside of a given percentage
        if abs(self.currentPercentage - self.rebalancePercentage) >= self.rebalanceSlippage:
            if self.v==1:
                print("Determined there needs to be a rebalance")
            return True
        else:
            if self.v==1:
                print("Determined there does not need to be a rebalance")
            return False
        
    def calculateAllocationPercentage(self):
        # Calculates the current and desired portfolio allocation percentages
        # Call this after there is a change in either the eth price, eth amount, usd amount, max price (rare), or factor (rare)
        self.currentPercentage = (self.ethAmount * self.ethPrice) / ((self.ethAmount * self.ethPrice) + self.usdAmount) # Set current ETH/USD ratio
        self.rebalancePercentage = 1 - ((1 / (self.maxPrice ** self.factor)) * (self.ethPrice ** self.factor)) # Set desired ETH/USD ratio
        if self.v==1:
            print("Calculated the current and desired portfolio allocation percentages")
        return
        
    def portfolioRebalance(self):
        # Function to rebalance the portfolio through the buying/selling of eth
        self.calculateAllocationPercentage()
        if self.rebalanceYesOrNo() == True:
            self.totalPortfolioValue = (self.ethAmount * self.ethPrice) + self.usdAmount
            self.ethAmount = self.totalPortfolioValue * self.rebalancePercentage / self.ethPrice # Calculates amount of eth in the portfolio after any adjustments
            self.usdAmount = self.totalPortfolioValue * (1 - self.rebalancePercentage) # Calculates USD in the portfolio after any adjustments
            
        
        if self.v==1:
            if self.currentPercentage > self.rebalancePercentage:
                print(f"Sold {self.totalPortfolioValue * (self.currentPercentage - self.rebalancePercentage)} ETH to balance the portfolio")
            elif self.rebalancePercentage > self.currentPercentage:
                print(f"Bought {self.totalPortfolioValue * (self.rebalancePercentage - self.currentPercentage)} ETH to balance the portfolio")
            else:
                print("Current and desired ETH/USD ratio aret the same, no blancing needed")
        self.calculateAllocationPercentage() # Re-caclulate now that the postfolio is balanced, after this runs the current and desired ETH/USD raitos should be the same
        return

    def increaseEthPrice(self, priceIncreasePercent=.05):
        # Takes as input the amount you want to increase the eth price
        self.ethPrice = self.ethPrice * (1 + priceIncreasePercent)
        if self.v==1:
            print(f"Increasing Eth price by {round(priceIncreasePercent * 100, 2)}%")
        return

    def decreaseEthPrice(self, priceDecreasePercent=.05):
        # Takes as input the amount you want to decrease the eth price
        self.ethPrice = self.ethPrice * (1 - priceDecreasePercent)
        if self.v==1:
            print(f"Decreasing Eth price by {round(priceDecreasePercent * 100, 2)}%")
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
    

portfolio = PortfolioRebalance(10, 3000, 5000, 12500, .03,1)
print(portfolio)
portfolio.portfolioRebalance()
portfolio.increaseEthPrice(.1)
portfolio.portfolioRebalance()
print(portfolio)
