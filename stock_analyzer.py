import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Stock Market Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📈 Stock Market Analysis Tool")
st.markdown("Analyze the performance of publicly traded companies with comprehensive metrics and visualizations.")

# Sidebar for user inputs
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Stock ticker input
    ticker_input = st.text_input(
        "Enter Stock Ticker or Company Name",
        placeholder="e.g., AAPL, MSFT, Tesla",
        help="Enter the stock ticker symbol (e.g., AAPL) or company name"
    )
    
    # Time period selection
    time_period = st.selectbox(
        "Select Time Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
        index=3,
        help="Choose the historical data range"
    )
    
    # Analysis options
    st.subheader("Analysis Options")
    show_ma = st.checkbox("Moving Averages", value=True)
    show_volume = st.checkbox("Volume Analysis", value=True)
    show_returns = st.checkbox("Returns Analysis", value=True)
    
    analyze_button = st.button("🔍 Analyze Stock", type="primary", use_container_width=True)

def get_stock_data(ticker, period):
    """Fetch stock data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        return stock, hist, info
    except Exception as e:
        return None, None, None

def calculate_metrics(df):
    """Calculate key financial metrics"""
    if df.empty:
        return None
    
    # Calculate returns
    df['Daily_Return'] = df['Close'].pct_change()
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
    
    # Calculate moving averages
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['MA_200'] = df['Close'].rolling(window=200).mean()
    
    # Calculate volatility
    df['Volatility'] = df['Daily_Return'].rolling(window=20).std() * np.sqrt(252)
    
    return df

def create_price_chart(df, ticker, show_ma):
    """Create interactive price chart with moving averages"""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{ticker} Stock Price', 'Volume')
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )
    
    # Moving averages
    if show_ma:
        colors = {'MA_20': '#FFA726', 'MA_50': '#42A5F5', 'MA_200': '#AB47BC'}
        names = {'MA_20': '20-day MA', 'MA_50': '50-day MA', 'MA_200': '200-day MA'}
        
        for ma, color in colors.items():
            if ma in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[ma],
                        name=names[ma],
                        line=dict(color=color, width=2)
                    ),
                    row=1, col=1
                )
    
    # Volume bars
    colors = ['#ef5350' if row['Close'] < row['Open'] else '#26a69a' 
              for _, row in df.iterrows()]
    
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color=colors,
            showlegend=False
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=600,
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    return fig

def create_returns_chart(df, ticker):
    """Create returns analysis chart"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(f'{ticker} Cumulative Returns', 'Daily Returns Distribution'),
        vertical_spacing=0.15
    )
    
    # Cumulative returns
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Cumulative_Return'] * 100,
            name='Cumulative Return',
            line=dict(color='#1f77b4', width=2),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ),
        row=1, col=1
    )
    
    # Returns distribution
    fig.add_trace(
        go.Histogram(
            x=df['Daily_Return'] * 100,
            name='Daily Returns',
            marker_color='#ff7f0e',
            nbinsx=50
        ),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Daily Return (%)", row=2, col=1)
    fig.update_yaxes(title_text="Return (%)", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=2, col=1)
    
    fig.update_layout(
        height=500,
        showlegend=False,
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_volatility_chart(df, ticker):
    """Create volatility analysis chart"""
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Volatility'] * 100,
            name='20-day Volatility',
            line=dict(color='#d62728', width=2),
            fill='tozeroy',
            fillcolor='rgba(214, 39, 40, 0.2)'
        )
    )
    
    fig.update_layout(
        title=f'{ticker} Rolling Volatility (20-day)',
        xaxis_title='Date',
        yaxis_title='Volatility (%)',
        height=350,
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def display_key_metrics(df, info):
    """Display key financial metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    current_price = df['Close'].iloc[-1]
    price_change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
    price_change_pct = (price_change / df['Close'].iloc[-2]) * 100
    
    total_return = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
    avg_volume = df['Volume'].mean()
    volatility = df['Volatility'].iloc[-1] * 100 if 'Volatility' in df.columns else 0
    
    with col1:
        st.metric(
            label="Current Price",
            value=f"${current_price:.2f}",
            delta=f"{price_change_pct:+.2f}%"
        )
    
    with col2:
        st.metric(
            label="Total Return",
            value=f"{total_return:+.2f}%",
            delta="Period"
        )
    
    with col3:
        st.metric(
            label="Avg Daily Volume",
            value=f"{avg_volume/1e6:.2f}M"
        )
    
    with col4:
        st.metric(
            label="Volatility (20d)",
            value=f"{volatility:.2f}%"
        )

def display_company_info(info):
    """Display company information"""
    st.subheader("📊 Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'longName' in info:
            st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
        if 'sector' in info:
            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        if 'industry' in info:
            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        if 'country' in info:
            st.write(f"**Country:** {info.get('country', 'N/A')}")
    
    with col2:
        if 'marketCap' in info:
            market_cap = info.get('marketCap', 0) / 1e9
            st.write(f"**Market Cap:** ${market_cap:.2f}B")
        if 'fiftyTwoWeekHigh' in info:
            st.write(f"**52 Week High:** ${info.get('fiftyTwoWeekHigh', 0):.2f}")
        if 'fiftyTwoWeekLow' in info:
            st.write(f"**52 Week Low:** ${info.get('fiftyTwoWeekLow', 0):.2f}")
        if 'beta' in info:
            st.write(f"**Beta:** {info.get('beta', 'N/A')}")

# Main application logic
if analyze_button and ticker_input:
    with st.spinner(f"Fetching data for {ticker_input}..."):
        stock, hist_data, stock_info = get_stock_data(ticker_input.upper(), time_period)
        
        if hist_data is not None and not hist_data.empty:
            # Calculate metrics
            hist_data = calculate_metrics(hist_data)
            
            # Display company information
            if stock_info:
                display_company_info(stock_info)
                st.divider()
            
            # Display key metrics
            st.subheader("📈 Key Metrics")
            display_key_metrics(hist_data, stock_info)
            st.divider()
            
            # Price chart
            st.subheader("💹 Price Analysis")
            price_fig = create_price_chart(hist_data, ticker_input.upper(), show_ma)
            st.plotly_chart(price_fig, use_container_width=True)
            
            # Returns analysis
            if show_returns:
                st.divider()
                st.subheader("📊 Returns Analysis")
                returns_fig = create_returns_chart(hist_data, ticker_input.upper())
                st.plotly_chart(returns_fig, use_container_width=True)
            
            # Volatility analysis
            if show_returns:
                col1, col2 = st.columns(2)
                
                with col1:
                    volatility_fig = create_volatility_chart(hist_data, ticker_input.upper())
                    st.plotly_chart(volatility_fig, use_container_width=True)
                
                with col2:
                    st.subheader("📉 Statistical Summary")
                    summary_stats = pd.DataFrame({
                        'Metric': ['Mean Return', 'Std Deviation', 'Min Return', 'Max Return', 'Sharpe Ratio (approx)'],
                        'Value': [
                            f"{hist_data['Daily_Return'].mean() * 100:.4f}%",
                            f"{hist_data['Daily_Return'].std() * 100:.4f}%",
                            f"{hist_data['Daily_Return'].min() * 100:.2f}%",
                            f"{hist_data['Daily_Return'].max() * 100:.2f}%",
                            f"{(hist_data['Daily_Return'].mean() / hist_data['Daily_Return'].std() * np.sqrt(252)):.2f}"
                        ]
                    })
                    st.dataframe(summary_stats, hide_index=True, use_container_width=True)
            
            # Download data option
            st.divider()
            st.subheader("💾 Export Data")
            csv = hist_data.to_csv()
            st.download_button(
                label="📥 Download Historical Data (CSV)",
                data=csv,
                file_name=f"{ticker_input}_{time_period}_data.csv",
                mime="text/csv"
            )
            
        else:
            st.error(f"❌ Unable to fetch data for '{ticker_input}'. Please check the ticker symbol and try again.")
            st.info("💡 **Tip:** Try using the official stock ticker symbol (e.g., AAPL for Apple, MSFT for Microsoft)")

elif analyze_button and not ticker_input:
    st.warning("⚠️ Please enter a stock ticker or company name to begin analysis.")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>📊 Stock Market Analysis Tool | Data provided by Yahoo Finance</p>
        <p style='font-size: 0.8rem;'>⚠️ This tool is for informational purposes only. Not financial advice.</p>
    </div>
    """, unsafe_allow_html=True)
