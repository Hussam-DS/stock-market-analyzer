# Stock Market Analysis Tool

A professional web application built with Streamlit for analyzing stock market performance of publicly traded companies.

## Features

- 📈 **Interactive Price Charts**: Candlestick charts with volume analysis
- 📊 **Moving Averages**: 20-day, 50-day, and 200-day moving averages
- 💹 **Returns Analysis**: Cumulative returns and distribution analysis
- 📉 **Volatility Metrics**: Rolling volatility calculations
- 🎯 **Key Metrics**: Real-time display of important financial indicators
- 📥 **Data Export**: Download historical data in CSV format
- 🎨 **Professional UI**: Clean, intuitive interface with customizable options

## Installation

1. **Install Python** (3.8 or higher)

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install streamlit yfinance pandas plotly numpy
   ```

## Usage

1. **Run the application**:
   ```bash
   streamlit run stock_analyzer.py
   ```

2. **Access the app**:
   - The app will automatically open in your browser
   - Default URL: http://localhost:8501

3. **Analyze stocks**:
   - Enter a stock ticker (e.g., AAPL, MSFT, GOOGL, TSLA)
   - Select your desired time period
   - Choose analysis options
   - Click "Analyze Stock"

## Supported Features

### Time Periods
- 1 month (1mo)
- 3 months (3mo)
- 6 months (6mo)
- 1 year (1y)
- 2 years (2y)
- 5 years (5y)
- Maximum available data (max)

### Analysis Options
- **Moving Averages**: Toggle 20, 50, and 200-day moving averages
- **Volume Analysis**: View trading volume patterns
- **Returns Analysis**: See cumulative returns and distribution

### Key Metrics Displayed
- Current price and daily change
- Total return for selected period
- Average daily trading volume
- 20-day rolling volatility
- Statistical summary (mean, std, min, max returns)
- Sharpe ratio approximation

### Company Information
- Company name and sector
- Industry and country
- Market capitalization
- 52-week high/low
- Beta coefficient

## Technical Details

### Technologies Used
- **Streamlit**: Web application framework
- **yfinance**: Stock data retrieval
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical calculations

### Data Source
- Yahoo Finance (via yfinance library)
- Real-time and historical stock data

## Example Stock Tickers

- **Technology**: AAPL (Apple), MSFT (Microsoft), GOOGL (Google), META (Meta)
- **Finance**: JPM (JPMorgan), BAC (Bank of America), GS (Goldman Sachs)
- **Consumer**: AMZN (Amazon), TSLA (Tesla), NKE (Nike)
- **Healthcare**: JNJ (Johnson & Johnson), PFE (Pfizer), UNH (UnitedHealth)

## Notes

- ⚠️ This tool is for informational and educational purposes only
- 📊 Not intended as financial or investment advice
- 🔄 Data is fetched in real-time from Yahoo Finance
- 💡 Some features require sufficient historical data (e.g., 200-day MA)

## Troubleshooting

**Issue**: Cannot fetch data for a ticker
- **Solution**: Verify the ticker symbol is correct (use official stock ticker)
- Check your internet connection
- Try a different ticker to test connectivity

**Issue**: Missing data or incomplete charts
- **Solution**: Some stocks may have limited historical data
- Try a longer-established company ticker
- Reduce the time period selection

**Issue**: Application won't start
- **Solution**: Ensure all dependencies are installed
- Check Python version (3.8+)
- Try reinstalling requirements: `pip install -r requirements.txt --upgrade`

## License

This project is for educational purposes. Please ensure compliance with Yahoo Finance terms of service when using their data.