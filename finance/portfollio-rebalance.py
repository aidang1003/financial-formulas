class PortfolioRebalance():
    def __init__(self, ethAmount, ethPrice, usdAmount, maxPrice, priceChangePercentage, v=0):
        self.v = v # Turns on verbose mode, only use while debugging
        if self.v == 1:
            print("Initiating the portfolio...")
        
        self.ethAmount = ethAmount # eth amount in eth
        self.ethPrice = ethPrice # eth price in usd
        self.usdAmount = usdAmount # usd amount in usd
        self.maxPrice = maxPrice # Max expected price of eth
        self.priceChangePercentage = priceChangePercentage # The percent slippage at which a rebalance happens automatically, no use for this currently

        self.factor = 2 # Factor for calculating re-allocation percentage, 1 is linear and a number greater than 1 means as price gets higher more sales will take place
        self.calculateAllocationPercentage()


    def __repr__(self):
        return f"""    Total Portfolio Value: ${round(self.totalPortfolioValue, 2)}
    ETH price >> ${round(self.ethPrice, 2)}
    ETH amount in ETH >> {round(self.ethAmount, 9)}
    ETH amount in USD >> ${round(self.ethAmount * self.ethPrice, 2)}
    USD amount in USD >> ${round(self.usdAmount, 2)}
    Current ETH/USD ratio >> {round(self.currentPercentage * 100, 2)}%
    Desired ETH/USD ratio >> {round(self.rebalancePercentage * 100, 2)}%"""

    def rebalanceYesOrNo(self):
        # Returns true when the balance is outside of a given percentage
        if abs(self.currentPercentage - self.rebalancePercentage) > 0:
            if self.v==1:
                print("Determined there can be a rebalance")
            return True
        else:
            if self.v==1:
                print("Determined there cannot be a rebalance")
            return False
        
    def calculateAllocationPercentage(self):
        # Calculates the current and desired portfolio allocation percentages
        # Call this after there is a change in either the eth price, eth amount, usd amount, max price (rare), or factor (rare)
        self.totalPortfolioValue = ((self.ethAmount * self.ethPrice) + self.usdAmount) # Calculate total portfolio value
        self.currentPercentage = (self.ethAmount * self.ethPrice) / self.totalPortfolioValue # Set current ETH/USD ratio
        self.rebalancePercentage = 1 - ((1 / (self.maxPrice ** self.factor)) * (self.ethPrice ** self.factor)) # Set desired ETH/USD ratio
        if self.v==1:
            print("Calculating portfolio allocation percentages and total value...") # Calculation technically happens before this line
            print(self)
        return
        
    def portfolioRebalance(self):
        # Function to rebalance the portfolio through the buying/selling of eth
        if self.v == 1:
            print(">>> Portfolio state before any rebalancing")
        self.calculateAllocationPercentage()
        if self.rebalanceYesOrNo() == True:
            self.totalPortfolioValue = (self.ethAmount * self.ethPrice) + self.usdAmount
            self.ethAmount = self.totalPortfolioValue * self.rebalancePercentage / self.ethPrice # Calculates amount of eth in the portfolio after any adjustments
            self.usdAmount = self.totalPortfolioValue * (1 - self.rebalancePercentage) # Calculates USD in the portfolio after any adjustments
            
        if self.v==1:
            if self.currentPercentage > self.rebalancePercentage:
                print(f"Sold {(self.totalPortfolioValue * (self.currentPercentage - self.rebalancePercentage)) / self.ethPrice} ETH to balance the portfolio")
                self.calculateAllocationPercentage() # Re-caclulate now that the postfolio is balanced, after this runs the current and desired ETH/USD raitos should be the same
            elif self.rebalancePercentage > self.currentPercentage:
                print(f"Bought ${round(self.totalPortfolioValue * (self.rebalancePercentage - self.currentPercentage), 2)} in ETH to balance the portfolio")
                self.calculateAllocationPercentage() # Re-caclulate now that the postfolio is balanced, after this runs the current and desired ETH/USD raitos should be the same
            else:
                print("Current and desired ETH/USD ratio are the same, no blancing needed")

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

    def generateAllocationPriceList(self):
        # Create a 2-D numbered array for prices which rebalncing will take place at
        self.allocationPriceList = []
        minPrice = 10 # Hard code minimum price of Eth to $10, any less is irrelevant
        i = 0
        while minPrice < self.maxPrice:
            self.allocationPriceList.append([i,round(minPrice, 2)])
            minPrice = minPrice * (1 + self.priceChangePercentage)
            i+=1
        self.allocationPriceList.append([i,round(self.maxPrice, 2)]) # Add the last value, when price is at max
        return self.allocationPriceList

    

portfolio = PortfolioRebalance(10, 3000, 5000, 12500, .03, 1)
print(portfolio.generateAllocationPriceList())
