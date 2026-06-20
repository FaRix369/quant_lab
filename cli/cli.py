import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Quantitative finance laboratory: data collection, transformation, storage, analysis and visualization.')
    subparsers = parser.add_subparsers(dest='command')

    status_db = subparsers.add_parser('status', help='Status DB')

    collector = subparsers.add_parser('collector', help='Collector Ticker-Period')
    collector.add_argument('--ticker')
    collector.add_argument('--period')

    analysis = subparsers.add_parser('analysis', help='Analysis Ticker-Period --functions(benchmarking, correlations, ratios)')
    analysis.add_argument('--ticker')
    analysis.add_argument('--period')
    analysis.add_argument('--functions', nargs='+')
    analysis.add_argument('--benchmark')

    feature_engineering = subparsers.add_parser('feature_engineering', help='Feature Engineering Ticker-Period-Window --functions(drawdown, returns, rolling, volatility, zscore)')
    feature_engineering.add_argument('--ticker')
    feature_engineering.add_argument('--period')
    feature_engineering.add_argument('--functions', nargs='+')
    feature_engineering.add_argument('--window')

    visualization = subparsers.add_parser('visualization', help='Visualization Ticker-Period --function(analysis_charts, feature_charts, price_charts)')
    visualization.add_argument('--ticker')
    visualization.add_argument('--period')
    visualization.add_argument('--functions', nargs='+')

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    print(args)










