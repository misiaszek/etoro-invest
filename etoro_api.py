import requests
import logging

class EtoroAPI:
    def __init__(self, api_key, base_url="https://api.etoro.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_account_info(self):
        endpoint = "/v1/accounts"
        return self._get(endpoint)

    def get_portfolio(self):
        endpoint = "/v1/portfolios"
        return self._get(endpoint)

    def get_market_data(self, symbol):
        endpoint = f"/v1/markets/{symbol}"
        return self._get(endpoint)

    def place_order(self, order_data):
        endpoint = "/v1/orders"
        return self._post(endpoint, order_data)

    def _get(self, endpoint):
        url = self.base_url + endpoint
        self.logger.info(f"GET request to {url}")
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def _post(self, endpoint, data):
        url = self.base_url + endpoint
        self.logger.info(f"POST request to {url} with data {data}")
        response = requests.post(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 200:
            self.logger.info(f"Response: {response.json()}")
            return response.json()
        else:
            self.logger.error(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()

if __name__ == "__main__":
    api_key = "YOUR_ETORO_API_KEY"
    etoro = EtoroAPI(api_key)

    # Example usage
    try:
        account_info = etoro.get_account_info()
        print("Account Info:", account_info)

        portfolio = etoro.get_portfolio()
        print("Portfolio:", portfolio)

        market_data = etoro.get_market_data("AAPL")
        print("Market Data for AAPL:", market_data)

        order_data = {
            "symbol": "AAPL",
            "quantity": 10,
            "orderType": "market",
            "side": "buy"
        }
        order_response = etoro.place_order(order_data)
        print("Order Response:", order_response)

    except Exception as e:
        print(f"An error occurred: {e}")
