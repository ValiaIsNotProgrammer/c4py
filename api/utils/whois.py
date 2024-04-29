import whois as whois_
from loguru import logger


class WHOIS:
    def __init__(self):
        pass

    def get_whois(self, url):
        logger.info(f'WHOIS start making')
        full_w = whois_.whois(url)
        logger.info(f'WHOIS is got')
        return full_w

    def get_valid_whois_data(self, url):
        whois_data = self.get_whois(url)
        valid_whois_data = {
            "domain_name": whois_data["domain_name"],
            "registrar": whois_data["registrar"],
            "updated_date": whois_data["updated_date"][0].strftime("%Y-%m-%d %H:%M:%S"),
            "country": whois_data["country"],
        }
        return valid_whois_data


whois = WHOIS()
