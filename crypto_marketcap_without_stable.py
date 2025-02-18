import requests

def get_top_cryptos(limit=10):
    # Make a request to the CoinGecko API to get the top cryptocurrencies by market cap
    url = f'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,  # Fetch more than 10 to ensure we exclude stablecoins and still get top 10
        'page': 1
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

def filter_stablecoins(cryptos):
    # List of well-known stablecoin symbols
    stablecoin_symbols = ["usdt", "usdc", "busd", "dai", "tusd", "usdp", "gusd", "ust", "bnb", "steth", "wsteth"]
    
    # Filter out stablecoins based on their symbol
    non_stablecoins = []
    for crypto in cryptos:
        if crypto['symbol'].lower() not in stablecoin_symbols:
            non_stablecoins.append(crypto)
        if len(non_stablecoins) == 10:
            break  # Stop once we have 10 non-stablecoins
    return non_stablecoins

def calculate_market_cap_percentage(cryptos):
    # Calculate the total market cap of the top 10 cryptos
    total_market_cap = sum(crypto['market_cap'] for crypto in cryptos)
    
    # Create a list with each crypto and its percentage of the total market cap
    crypto_data = []
    for crypto in cryptos:
        market_cap = crypto['market_cap']
        percentage = (market_cap / total_market_cap) * 100
        crypto_data.append({
            'name': crypto['name'],
            'market_cap_usd': market_cap,
            'percentage_of_total': percentage
        })
    
    return crypto_data

def display_cryptos(crypto_data):
    # Display the cryptocurrency information
    print(f"{'Name':<20} {'Market Cap (USD)':<20} {'% of Total Market Cap'}")
    print("-" * 60)
    for crypto in crypto_data:
        name = crypto['name']
        market_cap = f"${crypto['market_cap_usd']:,.2f}"
        percentage = f"{crypto['percentage_of_total']:.2f}%"
        print(f"{name:<20} {market_cap:<20} {percentage}")

if __name__ == "__main__":
    # Fetch top cryptos and filter out stablecoins
    top_cryptos = get_top_cryptos()
    if top_cryptos:
        non_stablecoins = filter_stablecoins(top_cryptos)
        crypto_data = calculate_market_cap_percentage(non_stablecoins)
        display_cryptos(crypto_data)
