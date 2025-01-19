from SearchStrategy import SearchStrategy


class SearchContext:

    def __init__(self, search_strategy: SearchStrategy):
        self.search_strategy = search_strategy

    def set_searching_strategy(self, search_strategy):
        self.search_strategy = search_strategy

    def search_name(self, name):
        return self.search_strategy.search_name(name)

    def search_author(self, name):
        return self.search_author(name)

    def search_genre(self, name):
        return self.search_genre(name)
