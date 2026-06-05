from abc import ABC, abstractmethod
#2.1
class Tarif(ABC):
    @abstractmethod
    def return_tarif(self, minutes):
        pass
class BaseTarif(Tarif):
    def return_tarif(self, minutes):
        return minutes*1
class ProTarif(Tarif):
    def return_tarif(self,minutes):
       return minutes*2

#2.2
class VoiceTarif(Tarif):
    def return_tarif(self, minutes):
       return minutes*1.4
class DataTarif(Tarif):
    def return_tarif(self, minutes):
        return minutes*3
class RoamingTarif(Tarif):
    def return_tarif(self,minutes):
        return minutes*4

