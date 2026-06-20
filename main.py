python main.py status #staus of DB

python main.py collector --ticker ASML --period 1y


#######################################
python main.py analysis --ticker ASML --period 1y
1) python main.py analysis --ticker ASML --period 1y --functions benchmarking 
2) python main.py analysis --ticker ASML --period 1y --functions correlation 
3) python main.py analysis --ticker ASML --period 1y --functions ratios

1)
python main.py analysis --ticker ASML --period 1y --benchmark SPY --functions excess_return #si no se pasa el benchmark en caso de ser necesario, se lanza error
python main.py analysis --ticker ASML --period 1y --benchmark SPY --functions tracking_error
python main.py analysis --ticker ASML --period 1y --benchmark SPY --functions information_ratio

2)
python main.py analysis --ticker ASML --period 1y --functions returns_correlation
python main.py analysis --ticker ASML --period 1y --functions prices_correlation

3)
python main.py analysis --ticker ASML --period 1y --functions sharpe_ratio
python main.py analysis --ticker ASML --period 1y --functions sortino_ratio
python main.py analysis --ticker ASML --period 1y --functions calmar_ratio
python main.py analysis --ticker ASML --period 1y --benchmark SPY --functions beta_ratio
python main.py analysis --ticker ASML --period 1y --benchmark SPY --functions alpha_ratio
#######################################


#######################################
python main.py feature_engineering --ticker ASML --period 1y
1) python main.py feature_engineering --ticker ASML --period 1y --functions drawdown
2) python main.py feature_engineering --ticker ASML --period 1y --functions returns
3) python main.py feature_engineering --ticker ASML --period 1y --functions rolling
4) python main.py feature_engineering --ticker ASML --period 1y --functions volatility
5) python main.py feature_engineering --ticker ASML --period 1y --functions zscore

1)
python main.py feature_engineering --ticker ASML --period 1y --functions function_drawdown
python main.py feature_engineering --ticker ASML --period 1y --functions max_drawdown
python main.py feature_engineering --ticker ASML --period 1y --functions peak_price
python main.py feature_engineering --ticker ASML --period 1y --functions trough_price
python main.py feature_engineering --ticker ASML --period 1y --functions drawdown_duration
python main.py feature_engineering --ticker ASML --period 1y --functions recovery_time

2)
python main.py feature_engineering --ticker ASML --period 1y --functions log_return
python main.py feature_engineering --ticker ASML --period 1y --functions log_return_digit
python main.py feature_engineering --ticker ASML --period 1y --functions simple_return
python main.py feature_engineering --ticker ASML --period 1y --functions aritmetic_return
python main.py feature_engineering --ticker ASML --period 1y --functions aritmetic_return_digit

3)
python main.py feature_engineering --ticker ASML --period 1y --window 20 --functions rolling_mean
python main.py feature_engineering --ticker ASML --period 1y --window 20 --functions rolling_std
python main.py feature_engineering --ticker ASML --period 1y --window 20 --functions rolling_min
python main.py feature_engineering --ticker ASML --period 1y --window 20 --functions rolling_max

4)
python main.py feature_engineering --ticker ASML --period 1y --functions historic_simple_volatility
python main.py feature_engineering --ticker ASML --period 1y --functions anualized_volatility
python main.py feature_engineering --ticker ASML --period 1y --window 20 --functions rolling_volatility
python main.py feature_engineering --ticker ASML --period 1y --functions ewma_volatility

5)
python main.py feature_engineering --ticker ASML --period 1y --functions z_score_historic
python main.py feature_engineering --ticker ASML --period 1y --window 20 --functions z_score_mobile
#######################################

#######################################
python main.py visualization --ticker ASML --period 1y
1) python main.py visualization --ticker ASML --period 1y --functions analysis_charts
2) python main.py visualization --ticker ASML --period 1y --functions feature_charts
3) python main.py visualizaton --ticker ASML --period 1y --functions price_charts 

1)
python main.py visualization --ticker ASML --period 1y --functions correlation_scatter
python main.py visualization --ticker ASML --period 1y --functions benchmarking_chart

2)
python main.py visualization --ticker ASML --period 1y --functions returns_chart
python main.py visualization --ticker ASML --period 1y --functions volatility_chart

3)
python main.py visualizaton --ticker ASML --period 1y --functions close_price
python main.py visualizaton --ticker ASML --period 1y --functions volume_chart
#######################################