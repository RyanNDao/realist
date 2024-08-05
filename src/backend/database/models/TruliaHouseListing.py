from dataclasses import dataclass, fields
from datetime import datetime
from backend.database.models.ModelAttribute import ModelAttribute
from collections import OrderedDict
import logging
from psycopg.types.json import Jsonb

from backend.server.utils.CommonLogger import CommonLogger



@dataclass
class TruliaHouseListing:
    key: str = ModelAttribute(str, optional=False)
    location: str = ModelAttribute(str, optional=False)
    address: str = ModelAttribute(str, optional=False)
    city: str = ModelAttribute(str, optional=True)
    state: str = ModelAttribute(str, optional=True)
    zip: str = ModelAttribute(str, optional=False)
    asking_price: int = ModelAttribute(int, optional=False)
    trulia_url: str = ModelAttribute(str, optional=False)
    floor_sqft: int = ModelAttribute(int, optional=True)
    lot_sqft: int = ModelAttribute(int, optional=True)
    bedrooms: str = ModelAttribute(str, optional=True)
    bathrooms: str = ModelAttribute(str, optional=True)
    basement: str = ModelAttribute(str, optional=True)
    foundation: str = ModelAttribute(str, optional=True)
    structure_type: str = ModelAttribute(str, optional=True)
    architecture: str = ModelAttribute(str, optional=True)
    house_material: str = ModelAttribute(str, optional=True)
    condition: str = ModelAttribute(str, optional=True)
    mls_listing_id: str = ModelAttribute(str, optional=True)
    trulia_listing_id: str = ModelAttribute(str, optional=True)
    parcel_number: str = ModelAttribute(str, optional=True)
    date_listed_or_sold: datetime = ModelAttribute((datetime, str), optional=True)
    date_scraped: datetime = ModelAttribute((datetime, str), optional=True)
    listing_status: str = ModelAttribute(str, optional=True)
    neighborhood: str = ModelAttribute(str, optional=True)
    property_type: str = ModelAttribute(str, optional=True)
    property_subtype: str = ModelAttribute(str, optional=True)
    parking: str = ModelAttribute(str, optional=True)
    year_built: int = ModelAttribute((int, str), optional=True)
    year_renovated: int = ModelAttribute((int, str), optional=True)
    price_history: list = ModelAttribute(list, optional=True)
    description: str = ModelAttribute(str, optional=True)

    def __post_init__(self):
        self.dict = self._returnAsDict()

    def _returnAsDict(self) -> OrderedDict:
        # this assumes fields perserves annotation order 
        dictObject = OrderedDict()
        for attributeField in fields(self):
            attributeName = attributeField.name
            dictObject[attributeName] = self.__getattribute__(attributeName)
        return dictObject
    
    def __getattribute__(self, attributeName):
        if isinstance(super().__getattribute__(attributeName), ModelAttribute):
            # when an attribute is not set, it will be ModelAttribute class by default
            # so this is used to return the true value (which is None)
            return None
        return super().__getattribute__(attributeName)
    
    def __eq__(self, other):
        if not isinstance(other, TruliaHouseListing):
            return False
        for attributeField in fields(self):
            attributeName = attributeField.name 
            if isinstance(self.__getattribute__(attributeName), Jsonb) and isinstance(other.__getattribute__(attributeName), Jsonb):
                selfAttribute = self.__getattribute__(attributeName).obj
                otherAttribute = other.__getattribute__(attributeName).obj
            else:
                selfAttribute = self.__getattribute__(attributeName)
                otherAttribute = other.__getattribute__(attributeName)
            if selfAttribute != otherAttribute:
                CommonLogger.LOGGER.warning(f'When comparing TruliaHouseListing objects, \"{attributeName}\" did not match!')
                return False
        else:
            return True
