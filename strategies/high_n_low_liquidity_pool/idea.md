### **Liquidity-Based Trading Strategy for High-Volume Market Sessions**

This trading strategy is designed around the concept of market liquidity and focuses on high-volume trading sessions (London and New York). It targets liquidity zones at the highs and lows of hourly candles to capitalize on potential reversals triggered by liquidity sweeps. The strategy uses the ATR (Average True Range) for stop-loss placement and seeks optimization to determine the best parameters.

---

#### **Strategy Overview**

1. **Session Focus**:  
   - The strategy is active only during high-liquidity market sessions, specifically **London** and **New York** sessions.  
   - Trading outside these sessions is avoided to filter out periods of low market activity and reduce noise.  
   - The specific time range can be optimized as a parameter to identify the best-performing trading windows.

2. **Targeting Hourly Candle Highs and Lows**:  
   - Liquidity often resides at the **highs** and **lows** of hourly candles.  
   - The strategy focuses on candles of varying durations (1-hour, 2-hour, 3-hour, etc.).  
   - Optimization is used to determine the optimal candle duration for the best performance.

3. **Formation of a Range**:  
   - At the start of the trading session, the strategy waits for the first hourly candle to form.  
   - The high and low of this candle define the range to monitor for potential trades.

4. **Liquidity Sweep and Trade Trigger**:  
   - When the price **takes out the high** (or low) of the range but **closes below the high** (or above the low), it indicates a potential reversal.  
   - A "low market tension" candle (small body relative to its range) at these points further confirms the trade signal.

5. **Entry Rules**:  
   - **Sell Signal**:  
     - If the price takes out the **high** of the range and closes **below** it with a low-tension candle, initiate a sell position.  
   - **Buy Signal** (not explicitly mentioned but inferred for symmetry):  
     - If the price takes out the **low** of the range and closes **above** it with a low-tension candle, initiate a buy position.

6. **Exit Rules**:  
   - **Take Profit**:  
     - The profit target is set at the **opposite end** of the initial hourly range.  
   - **Stop Loss**:  
     - The stop loss is placed at **2x the ATR** of the triggering candle.  

7. **Optimization Parameters**:  
   - The strategy includes parameters for:  
     - **Session Time**: To determine the most profitable trading window.  
     - **Candle Duration**: To optimize the timeframe for identifying liquidity pools.  
     - Other relevant parameters (e.g., ATR multiplier) can be added as needed.

---

### **Implementation Plan**

#### **Key Components**
- **Indicator Calculation**:  
  - Use ATR to calculate stop loss.  
  - Determine session timing for trade filtering.  

- **Trade Signal Logic**:  
  - Detect liquidity sweeps and confirm low-tension candles.  

- **Risk Management**:  
  - Set take profit and stop-loss rules as outlined.  

- **Optimization**:  
  - Allow testing of various session timings, candle durations, and ATR multipliers to refine strategy performance.

Now, let’s move on to implementing this strategy in **Backtrader**. Would you like the entire code or specific parts first?