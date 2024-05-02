import whois as whois_
from loguru import logger


class WHOIS:
    def __init__(self):
        pass

    def get_whois(self, url: str) -> dict:
        "Метод для получения WHOIS по url"
        logger.info(f'WHOIS start making')
        full_w = whois_.whois(url)
        logger.info(f'WHOIS is got')
        return full_w

    def get_valid_whois_data(self, url: str) -> dict:
        "Метод для получения валидного, сериализованного WHOIS словаря"
        whois_data = self.get_whois(url)
        if whois_data.get("updated_date", None):
            try:
                uploated_date = whois_data["updated_date"][0].strftime("%Y-%m-%d %H:%M:%S")
            except TypeError:
                uploated_date = whois_data["updated_date"].strftime("%Y-%m-%d")
        else:
            uploated_date = whois_data["creation_date"].strftime("%Y-%m-%d %H:%M:%S")
        try:
            country = whois_data["country"]
        except KeyError:
            country = None
        valid_whois_data = {
            "domain_name": whois_data["domain_name"],
            "registrar": whois_data["registrar"],
            "updated_date": uploated_date,
            "country": country,
        }
        return valid_whois_data


whois = WHOIS()
