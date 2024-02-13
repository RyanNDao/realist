from abc import ABC, abstractmethod

class Scraper(ABC):
    
    @abstractmethod
    def makeRequest(self):
        pass