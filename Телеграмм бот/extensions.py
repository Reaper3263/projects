import requests
import json

class API_Exceptions(Exception):
    pass
class Counter:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise API_Exceptions("Введите 3 параметра")
        base, quote, amount = values
        if quote == base:
            raise API_Exceptions(f"Ошибка, Одинаковые валюты {quote}")
        try:
            amount = float(amount)
        except ValueError:
            raise API_Exceptions(f"Не удалось обработать количество {amount}")
        response = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}").content
        result = round(float(json.loads(response)[quote]) * float(amount),2)
        return round(result,3)