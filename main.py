#region imports

from AlgorithmImports import *

#endregion



class MomentumAssetAllocationStrategy(QCAlgorithm):



    def Initialize(self):

        self.SetStartDate(2020, 1, 1)


        self.SetCash(100000)

        self.data = {}

        period = 3 
        market_trend_period = 10

        self.SetWarmUp(period, Resolution.Daily)

        self.traded_count = 10

        self.symbols = ["SPY", "EFA", "IEF", "VNQ", "GSG", "QQQ", "IWM", "BABA", "AAPL", "MSFT", "TSLA", "AMZN", "NVDA", "META",
                "DUK", "SO", "NEE", "PG", "KO", "PEP", "JNJ", "PFE", "MRK", "O", "SPG", "WELL", "GLD", "GOLD", "NEM"]


        for symbol in self.symbols:

            self.AddEquity(symbol, Resolution.Minute)

            self.data[symbol] = self.ROC(symbol, period, Resolution.Daily)

        # setting rebalance period
        self.recent_month = -1
        # self.next_rebalance_date = self.Time

    

        self.short_count = 5
        self.stop_loss_percentage = 0  # Stop-loss at 5% of the short position value

        # Initialize ROC for SPY with a 3-day period
        self.spy_roc = self.ROC("SPY", period, Resolution.Daily)
        self.spy_momp = self.MOMP("SPY", 7, Resolution.Daily)

        self.Plot("Performance", "Portfolio Value", self.Portfolio.TotalPortfolioValue)

        

    def OnData(self, data):

        if self.IsWarmingUp or not self.spy_momp.IsReady:
            return

        
        roc_value = self.spy_roc.Current.Value
        market_momp = self.spy_momp.Current.Value

        # Determine market condition
        long_allocation = 0.8 # Default long allocation
        short_allocation = 0.2 # Default short allocation
        delta = 0.01

        # Adjust allocations based on SPY's average momentum
        if roc_value > market_momp:  # Bullish market
            long_allocation += delta  # Increase long allocation by 10%
            short_allocation -= delta  # Decrease short allocation by 10%
        elif roc_value < market_momp:  # Bearish market
            long_allocation -= delta  # Decrease long allocation by 10%
            short_allocation += delta  # Increase short allocation by 10%

        # Normalize and ensure allocations are within 0 and 1
        long_allocation = min(max(long_allocation, 0), 1)
        short_allocation = min(max(short_allocation, 0), 1)

        if not (self.Time.hour == 9 and self.Time.minute == 31):

            return

        ## This is for monthly rebalance
        if self.Time.month == self.recent_month:

            return

        self.recent_month = self.Time.month

        # ### This is for weekly rebalance
        # if self.Time >= self.next_rebalance_date:
        #     self.next_rebalance_date = self.Time + timedelta(days=7)

        selected = {symbol: roc.Current.Value for symbol, roc in self.data.items() if symbol in data and roc.IsReady}

        # modify from here
        # Select long and short candidates
        sorted_by_momentum = sorted(selected.items(), key=lambda x: x[1], reverse=True)
        long_candidates = sorted_by_momentum[:self.traded_count]
        short_candidates = sorted_by_momentum[-self.short_count:]
        
        # Normalize momentum for long positions
        total_long_momentum = sum([x[1] for x in long_candidates])
        total_short_momentum = sum([-x[1] for x in short_candidates])  # Negative to make positive for calculation
        
        # Manage positions
        for symbol in self.Portfolio.Keys:
            if symbol not in [x[0] for x in long_candidates + short_candidates]:
                self.Liquidate(symbol)
        
        # Allocate long positions
        for symbol, momentum in long_candidates:
            if total_long_momentum > 0:  # Prevent division by zero
                allocation_percentage = long_allocation * (momentum / total_long_momentum)
                self.SetHoldings(symbol, allocation_percentage)
        
        # # Allocate and manage short positions
        # for symbol, momentum in short_candidates:
        #     self.SetHoldings(symbol, -0.1)  # Example fixed short allocation

        # Allocate short positions dynamically based on decreasing momentum
        for symbol, momentum in short_candidates:
            if total_short_momentum > 0:  # Prevent division by zero
                allocation_percentage = -short_allocation * (momentum / total_short_momentum)  # 20% of capital to shorts, negative for shorting
                self.SetHoldings(symbol, allocation_percentage)
        
            # Implement stop-loss
            if self.Securities[symbol].Price > self.Portfolio[symbol].AveragePrice * (1 + self.stop_loss_percentage):
                self.Liquidate(symbol)  # Exit if the price rises more than the stop-loss threshold
        
        
        
        self.Plot("Asset Allocation", "Portfolio Value", self.Portfolio.TotalPortfolioValue)

    def OnEndOfMonth(self):
        self.Plot("Performance", "Portfolio Value", self.Portfolio.TotalPortfolioValue)
