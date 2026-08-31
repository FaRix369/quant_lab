import inspect
from cli.cli import parse_args
from pipelines.stock_collector import collector
from analysis import benchmarking, correlation, ratios
from visualization import analysis_charts, feature_charts, price_charts
from feature_engineering import drawdown, returns, rolling, volatility, zscore
from database.querys import q_returns, q_returns_indexed
from feature_engineering.returns import log_return
from feature_engineering.drawdown import function_drawdown
from analysis.benchmarking import excess_return
from feature_engineering.volatility import rolling_volatility
from database.db_connection import get_status

def main():
    args = parse_args()

    if args.command == 'status':
        get_status()

    elif args.command == 'collector':
        collection = collector.collect(args.ticker, args.period)

    elif args.command == 'analysis':
        df = q_returns(args.ticker, args.period)

        functions_map = {
            'sharpe_ratio': ratios.sharpe_ratio,
            'sortino_ratio': ratios.sortino_ratio,
            'calmar_ratio': ratios.calmar_ratio,
            'beta_ratio': ratios.beta_ratio,             
            'alpha_ratio': ratios.alpha_ratio,
            'excess_return': benchmarking.excess_return,
            'tracking_error': benchmarking.tracking_error,
            'information_ratio': benchmarking.information_ratio,
            'returns_correlation': correlation.returns_correlation,
            'prices_correlation': correlation.prices_correlation,
        }

        if args.benchmark is not None:
            benchmark = q_returns_indexed(args.benchmark, args.period)

        for i in args.functions:
            function = functions_map[i]  #get the real function object using the key
            bench = inspect.signature(function) #get the signature

            if 'benchmark' in bench.parameters:
                result = function(df, benchmark)
            else:
                result = function(df)
            print(result)
            
            

    elif args.command == 'feature_engineering':
        df = q_returns(args.ticker, args.period)
        drawdown_variable = function_drawdown(df)
        return_log = log_return(df)

        functions_map = {
             'function_drawdown':drawdown.function_drawdown,
             'max_drawdown':drawdown.max_drawdown,
             'peak_price':drawdown.peak_price,
             'trough_price':drawdown.trough_price,
             'drawdown_duration':drawdown.drawdown_duration,
             'recovery_time':drawdown.recovery_time,
             'log_return':returns.log_return,
             'log_return_digit':returns.log_return_digit,
             'simple_return':returns.simple_return,
             'aritmetic_return':returns.aritmetic_return,
             'aritmetic_return_digit':returns.aritmetic_return_digit,
             'rolling_mean':rolling.rolling_mean,
             'rolling_std':rolling.rolling_std,
             'rolling_min':rolling.rolling_min,
             'rolling_max':rolling.rolling_max,
             'historic_simple_volatility':volatility.historic_simple_volatility,
             'anualized_volatility':volatility.anualized_volatility,
             'rolling_volatility':volatility.rolling_volatility,
             'ewma_volatility':volatility.ewma_volatility,
             'z_score_historic':zscore.z_score_historic,
             'z_score_mobile':zscore.z_score_mobile
        }

        for i in args.functions:
            function = functions_map[i]  #get the real function object using the key
            signature = inspect.signature(function) #get the signature

            if 'window' in signature.parameters and 'return_log' in signature.parameters and 'drawdown' in signature.parameters:
                result = function(args.window, return_log, drawdown_variable)
            elif 'window' in signature.parameters and 'return_log' in signature.parameters:
                result = function(args.window, return_log)
            elif 'window' in signature.parameters and 'drawdown' in signature.parameters:
                result = function(args.window, drawdown_variable)
            elif 'return_log' in signature.parameters and 'drawdown' in signature.parameters:
                result = function(return_log, drawdown_variable)
            elif 'window' in signature.parameters:
                result = function(args.window)
            elif 'return_log' in signature.parameters:
                result = function(return_log)
            elif 'drawdown' in signature.parameters:
                result = function(drawdown_variable)
            else:
                result = function(df)
            print(result)


    elif args.command == 'visualization':
        df = q_returns(args.ticker, args.period)
        close = df['close']  
        adj = df['adj_close']
        volume = df['volume']
        returns = log_return(df)
        volatility = rolling_volatility(returns, args.window)

        if args.benchmark is not None:
            benchmark = q_returns_indexed(args.benchmark, args.period)
            benchmark_returns = log_return(benchmark)
            excess = excess_return(df, benchmark_returns)

        functions_map = {
             'correlation_scatter':analysis_charts.correlation_scatter,
             'benchmarking_chart':analysis_charts.benchmarking_chart,
             'returns_chart':feature_charts.returns_chart,
             'volatility_chart':feature_charts.volatility_chart,
             'close_price':price_charts.close_price,
             'volume_chart':price_charts.volume_chart
        }

        for i in args.functions:
            function = functions_map[i]  #get the real function object using the key
            signature = inspect.signature(function) #get the signature

            if 'asset1' in signature.parameters:
                 result = function(returns, benchmark_returns, args.ticker, args.benchmark)
            elif 'date' in signature.parameters and 'excess' in signature.parameters:
                 result = function(excess.index, excess)
            elif 'date' in signature.parameters and 'returns' in signature.parameters:
                 result = function(returns.index, returns)
            elif 'date' in signature.parameters and 'volatility' in signature.parameters:
                 result = function(volatility.index, volatility)
            elif 'date' in signature.parameters and 'close' in signature.parameters and 'adj_close' in signature.parameters:
                 result = function(close.index, close, adj)
            else: 
                 result = function(volume.index, volume)
            print(result)

    else:
        print("Error: no command specified. Use: status, collector, analysis, feature_engineering, visualization")

if __name__ == "__main__":
    main()