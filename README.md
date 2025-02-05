# Phantom Alerts

Phantom Alerts is a project designed to send Discord notifications to a server named `phantom-alerts` to notify me when a cryptocurrency I am invested in has returned a certain percentage. 

## Features

- **Real-time Price Data**: Utilizes the CoinGecko API to fetch real-time price data for cryptocurrencies.
- **Dynamic Updates**: Continuously updates a JSON file holding all the cryptocurrencies invested in.
- **Custom Alerts**: Sends a Discord notification once the current price of a cryptocurrency has returned 100% from the purchase price.

## Usage

1. **Setup**: Configure the project with Discord server details and the list of cryptocurrencies invested in.
2. **Run**: Execute the project to start monitoring the price data.
3. **Receive Alerts**: Get notified on `phantom-alerts` Discord server when a cryptocurrency hits the target return percentage.

## Dependencies

- CoinGecko API
- Discord API

## License

This project is licensed under the MIT License.
