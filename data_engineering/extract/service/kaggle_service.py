from kaggle import KaggleApi


class KaggleService:
    __api: KaggleApi = None

    def get_api(self):
        if self.__api is None:
            self.__api = KaggleApi()
        return self.__api


kaggle_service = KaggleService()
kaggle_api = kaggle_service.get_api()
kaggle_api.authenticate()
