from django.apps import AppConfig


class AuctionHouseConfig(AppConfig):
    name = 'auction_house'

    def ready(self):
        import auction_house.signals
