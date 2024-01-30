import yfinance as yf
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

# Setting sidebar size using CSS
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 270px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# Putting all radio buttons side by side
st.sidebar.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

st.header('Stock analysis')

asset_type = st.sidebar.radio('Choose the type of asset',['FIIs','Stocks'], index=None)

fiis = ['AIEC11.SA','CACR11.SA','KIVO11.SA']
stock = ['CPLE6.SA','PETR4.SA']


if asset_type == 'FIIs':
    asset = st.sidebar.selectbox('What fii do you want to forecast?',fiis,index=None)
else:
    asset = st.sidebar.selectbox('What stock do you want to forecast?',stock,index=None)

data_time = st.sidebar.radio('Time to show',['1d','5d','1mo','12mo','2y','Max'])

st.write(asset)
stock_data = yf.Ticker(asset).history("Max")
training = stock_data.reset_index()
training['Date'] = training['Date'].dt.date
columns = ['Date','Close']
training = training[columns]
training.columns = ['ds','y']
model = Prophet()
model.fit(training)
period = model.make_future_dataframe(10)
prediction = model.predict(period)
st.write(prediction.tail(5))
st.plotly_chart(plot_plotly(model, prediction))
st.plotly_chart(plot_components_plotly(model, prediction))