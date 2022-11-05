import requests
import json
import re
import pandas as pd
from datetime import datetime
from collections import OrderedDict
import itertools

requests.packages.urllib3.disable_warnings()
pd.set_option('display.max_columns', None)


def initializeRequest():
    url=''
    if not url:
        url = input('Type url:\n')
    #### json dict here ####
    payloadDict = \
        {
            "operationName": "WEB_searchResultsMapQuery",
            "variables": {
                "isSwipeableFactsEnabled": False,
                "heroImageFallbacks": [
                    "STREET_VIEW",
                    "SATELLITE_VIEW"
                ],
                "searchDetails": {
                    "searchType": "FOR_SALE",
                    "location": {
                        "cities": [
                            {
                                "city": "Philadelphia",
                                "state": "PA"
                            }
                        ],
                    },
                    "filters": {
                        "sort": {
                            "type": "DATE",
                            "ascending": False
                        },
                        "page": 1,
                        "limit": 25,
                        "offset": 0,
                        "isAlternateListingSource": False,
                        "propertyTypes": [],
                        "listingTypes": [],
                        "pets": [],
                        "rentalListingTags": [],
                        "foreclosureTypes": [],
                        "buildingAmenities": [],
                        "unitAmenities": [],
                        "landlordPays": [],
                        "propertyAmenityTypes": []

                    }
                },
                "includeOffMarket": False,
                "includeLocationPolygons": False,
                "isSPA": False,
                "includeNearBy": True
            },
            "query": "query WEB_searchResultsMapQuery($searchDetails: SEARCHDETAILS_Input!, $heroImageFallbacks: [MEDIA_HeroImageFallbackTypes!], $includeOffMarket: Boolean!, $includeLocationPolygons: Boolean!, $isSPA: Boolean!, $includeNearBy: Boolean!, $isSwipeableFactsEnabled: Boolean = false) {\n  searchResultMap: searchHomesByDetails(searchDetails: $searchDetails, includeNearBy: $includeNearBy) {\n    ...SearchResultsMapClientFragment\n    __typename\n  }\n  offMarketHomes: searchOffMarketHomes(searchDetails: $searchDetails) @include(if: $includeOffMarket) {\n    ...HomeMarkerLayersContainerFragment\n    ...HoverCardLayerFragment\n    __typename\n  }\n}\n\nfragment SearchResultsMapClientFragment on SEARCH_Result {\n  ...HomeMarkerLayersContainerFragment\n  ...HoverCardLayerFragment\n  ...SearchLocationBoundaryFragment @include(if: $includeLocationPolygons)\n  ...SchoolSearchMarkerLayerFragment\n  ...TransitLayerFragment\n  __typename\n}\n\nfragment HomeMarkerLayersContainerFragment on SEARCH_Result {\n  ...HomeMarkersLayerFragment\n  __typename\n}\n\nfragment HomeMarkersLayerFragment on SEARCH_Result {\n  homes {\n    location {\n      coordinates {\n        latitude\n        longitude\n        __typename\n      }\n      __typename\n    }\n    url\n    metadata {\n      compositeId\n      __typename\n    }\n    ...HomeMarkerFragment\n    __typename\n  }\n  nearByHomes {\n    ...HomeMarkerFragment\n    __typename\n  }\n  __typename\n}\n\nfragment HomeMarkerFragment on HOME_Details {\n  media {\n    hasThreeDHome\n    __typename\n  }\n  location {\n    coordinates {\n      latitude\n      longitude\n      __typename\n    }\n    __typename\n  }\n  displayFlags {\n    enableMapPin\n    __typename\n  }\n  price {\n    calloutMarkerPrice: formattedPrice(formatType: SHORT_ABBREVIATION)\n    __typename\n  }\n  url\n  ... on HOME_Property {\n    activeForSaleListing {\n      openHouses {\n        formattedDay\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ...HomeDetailsTopThirdFragment @include(if: $isSPA)\n  __typename\n}\n\nfragment HomeDetailsTopThirdFragment on HOME_Details {\n  bathrooms {\n    summaryBathrooms: formattedValue(formatType: COMMON_ABBREVIATION)\n    __typename\n  }\n  bedrooms {\n    summaryBedrooms: formattedValue(formatType: COMMON_ABBREVIATION)\n    __typename\n  }\n  floorSpace {\n    formattedDimension\n    __typename\n  }\n  location {\n    city\n    coordinates {\n      latitude\n      longitude\n      __typename\n    }\n    neighborhoodName\n    stateCode\n    zipCode\n    cityStateZipAddress: formattedLocation(formatType: CITY_STATE_ZIP)\n    homeFormattedAddress: formattedLocation\n    summaryFormattedLocation: formattedLocation(formatType: STREET_COMMUNITY_BUILDER)\n    __typename\n  }\n  media {\n    metaTagHeroImages: heroImage(fallbacks: $heroImageFallbacks) {\n      url {\n        desktop: custom(size: {width: 2048, height: 200})\n        __typename\n      }\n      __typename\n    }\n    topThirdHeroImages: heroImage(fallbacks: $heroImageFallbacks) {\n      __typename\n      url {\n        extraSmallSrc: custom(size: {width: 375, height: 275})\n        smallSrc: custom(size: {width: 570, height: 275})\n        mediumSrc: custom(size: {width: 768, height: 500})\n        largeSrc: custom(size: {width: 992, height: 500})\n        hiDipExtraSmallSrc: custom(size: {width: 1125, height: 825})\n        hiDpiSmallSrc: custom(size: {width: 1710, height: 825})\n        hiDpiMediumSrc: custom(size: {width: 2048, height: 1536})\n        __typename\n      }\n      webpUrl: url(compression: webp) {\n        extraSmallWebpSrc: custom(size: {width: 375, height: 275})\n        smallWebpSrc: custom(size: {width: 570, height: 275})\n        mediumWebpSrc: custom(size: {width: 768, height: 500})\n        largeWebpSrc: custom(size: {width: 992, height: 500})\n        hiDipExtraSmallWebpSrc: custom(size: {width: 1125, height: 825})\n        hiDpiSmallWebpSrc: custom(size: {width: 1710, height: 825})\n        hiDpiMediumWebpSrc: custom(size: {width: 2048, height: 1536})\n        __typename\n      }\n    }\n    totalPhotoCount\n    __typename\n  }\n  metadata {\n    compositeId\n    currentListingId\n    __typename\n  }\n  pageText {\n    title\n    metaDescription\n    __typename\n  }\n  price {\n    formattedPrice\n    ... on HOME_LastSoldPrice {\n      formattedPriceDifferencePercent\n      formattedSoldDate(dateFormat: \"MMM D, YYYY\")\n      listingPrice {\n        formattedPrice(formatType: SHORT_ABBREVIATION)\n        __typename\n      }\n      priceDifferencePercent\n      pricePerDimension {\n        formattedDimension\n        __typename\n      }\n      __typename\n    }\n    ... on HOME_ForeclosureEstimatePrice {\n      price\n      typeDescription\n      __typename\n    }\n    ... on HOME_PriceRange {\n      currencyCode\n      max\n      min\n      __typename\n    }\n    ... on HOME_SinglePrice {\n      currencyCode\n      price\n      __typename\n    }\n    __typename\n  }\n  tracking {\n    key\n    value\n    __typename\n  }\n  url\n  ... on HOME_Property {\n    currentStatus {\n      isOffMarket\n      isRecentlySold\n      isForeclosure\n      isActiveForRent\n      isActiveForSale\n      isRecentlyRented\n      label\n      __typename\n    }\n    __typename\n  }\n  ... on HOME_RentalCommunity {\n    location {\n      rentalCommunityFormattedLocation: formattedLocation(formatType: STREET_COMMUNITY_NAME)\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HoverCardLayerFragment on SEARCH_Result {\n  homes {\n    ...HomeHoverCardFragment\n    __typename\n  }\n  nearByHomes {\n    ...HomeHoverCardFragment\n    __typename\n  }\n  __typename\n}\n\nfragment HomeHoverCardFragment on HOME_Details {\n  ...HomeDetailsCardFragment\n  ...HomeDetailsCardHeroFragment\n  ...HomeDetailsCardPhotosFragment\n  ...HomeDetailsGroupInsightsFragment @include(if: $isSwipeableFactsEnabled)\n  location {\n    coordinates {\n      latitude\n      longitude\n      __typename\n    }\n    __typename\n  }\n  displayFlags {\n    enableMapPin\n    showMLSLogoOnMapMarkerCard\n    __typename\n  }\n  __typename\n}\n\nfragment HomeDetailsCardFragment on HOME_Details {\n  __typename\n  location {\n    city\n    stateCode\n    zipCode\n    fullLocation: formattedLocation(formatType: STREET_CITY_STATE_ZIP)\n    partialLocation: formattedLocation(formatType: STREET_ONLY)\n    __typename\n  }\n  price {\n    formattedPrice\n    __typename\n  }\n  url\n  tags(include: MINIMAL) {\n    level\n    formattedName\n    icon {\n      vectorImage {\n        svg\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  fullTags: tags {\n    level\n    formattedName\n    icon {\n      vectorImage {\n        svg\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  floorSpace {\n    formattedDimension\n    __typename\n  }\n  lotSize {\n    ... on HOME_SingleDimension {\n      formattedDimension(minDecimalDigits: 2, maxDecimalDigits: 2)\n      __typename\n    }\n    __typename\n  }\n  bedrooms {\n    formattedValue(formatType: TWO_LETTER_ABBREVIATION)\n    __typename\n  }\n  bathrooms {\n    formattedValue(formatType: TWO_LETTER_ABBREVIATION)\n    __typename\n  }\n  isSaveable\n  preferences {\n    isSaved\n    isSavedByCoShopper @include(if: false)\n    __typename\n  }\n  metadata {\n    compositeId\n    legacyIdForSave\n    __typename\n  }\n  tracking {\n    key\n    value\n    __typename\n  }\n  displayFlags {\n    showMLSLogoOnListingCard\n    addAttributionProminenceOnListCard\n    __typename\n  }\n  ... on HOME_RoomForRent {\n    numberOfRoommates\n    availableDate: formattedAvailableDate(dateFormat: \"MMM D\")\n    providerListingId\n    __typename\n  }\n  ... on HOME_RentalCommunity {\n    activeListing {\n      provider {\n        summary(formatType: SHORT)\n        listingSource {\n          logoUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    location {\n      communityLocation: formattedLocation(formatType: STREET_COMMUNITY_NAME)\n      __typename\n    }\n    providerListingId\n    __typename\n  }\n  ... on HOME_Property {\n    currentStatus {\n      isRecentlySold\n      isRecentlyRented\n      isActiveForRent\n      isActiveForSale\n      isOffMarket\n      isForeclosure\n      __typename\n    }\n    priceChange {\n      priceChangeDirection\n      __typename\n    }\n    activeListing {\n      provider {\n        summary(formatType: SHORT)\n        extraShortSummary: summary(formatType: EXTRA_SHORT)\n        listingSource {\n          logoUrl\n          __typename\n        }\n        __typename\n      }\n      dateListed\n      __typename\n    }\n    lastSold {\n      provider {\n        summary(formatType: SHORT)\n        extraShortSummary: summary(formatType: EXTRA_SHORT)\n        listingSource {\n          logoUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    providerListingId\n    __typename\n  }\n  ... on HOME_FloorPlan {\n    priceChange {\n      priceChangeDirection\n      __typename\n    }\n    provider {\n      summary(formatType: SHORT)\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment HomeDetailsCardHeroFragment on HOME_Details {\n  media {\n    heroImage(fallbacks: $heroImageFallbacks) {\n      url {\n        small\n        __typename\n      }\n      webpUrl: url(compression: webp) {\n        small\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment HomeDetailsCardPhotosFragment on HOME_Details {\n  media {\n    __typename\n    heroImage(fallbacks: $heroImageFallbacks) {\n      url {\n        small\n        __typename\n      }\n      webpUrl: url(compression: webp) {\n        small\n        __typename\n      }\n      __typename\n    }\n    photos {\n      url {\n        small\n        __typename\n      }\n      webpUrl: url(compression: webp) {\n        small\n        __typename\n      }\n      __typename\n    }\n  }\n  __typename\n}\n\nfragment HomeDetailsGroupInsightsFragment on HOME_Details {\n  ... on HOME_Property {\n    groupedInsights {\n      insights {\n        ... on HOME_FeatureInsights {\n          insightTags {\n            formattedName\n            __typename\n          }\n          __typename\n        }\n        ... on HOME_SmartInsights {\n          insightTags {\n            formattedName\n            __typename\n          }\n          __typename\n        }\n        ... on HOME_ContextualPhrases {\n          phrases {\n            description\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SearchLocationBoundaryFragment on SEARCH_Result {\n  location {\n    encodedPolygon\n    ... on SEARCH_ResultLocationCity {\n      locationId\n      __typename\n    }\n    ... on SEARCH_ResultLocationCounty {\n      locationId\n      __typename\n    }\n    ... on SEARCH_ResultLocationNeighborhood {\n      locationId\n      __typename\n    }\n    ... on SEARCH_ResultLocationPostalCode {\n      locationId\n      __typename\n    }\n    ... on SEARCH_ResultLocationState {\n      locationId\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SchoolSearchMarkerLayerFragment on SEARCH_Result {\n  schools {\n    ...SchoolMarkersLayerFragment\n    __typename\n  }\n  __typename\n}\n\nfragment SchoolMarkersLayerFragment on School {\n  id\n  latitude\n  longitude\n  categories\n  ...SchoolHoverCardFragment\n  __typename\n}\n\nfragment SchoolHoverCardFragment on School {\n  id\n  name\n  gradesRange\n  providerRating {\n    rating\n    __typename\n  }\n  streetAddress\n  studentCount\n  latitude\n  longitude\n  __typename\n}\n\nfragment TransitLayerFragment on SEARCH_Result {\n  transitStations {\n    stationName\n    iconUrl\n    coordinates {\n      latitude\n      longitude\n      __typename\n    }\n    radius\n    __typename\n  }\n  __typename\n}\n"
        }
    #### json dict here ####

    headers = \
        {
            'Content-Type': 'application/json',
            'Cookie': '_pxhd=FEdz2RO1thvNb7wYieHUICcOHmLIrHdBzPMgjET02a/oBqPp3ZR0FrooSi9gTj9jQMb9QKg8BmV7S/3fUlx8AA==:gfN5DVGjUBwpQj0qwRvxon44QUFFscfum2lX0pL3zuP9JMo8pqq3nynzu9MxsR6zFHdddUkvAi/4pxc8VTibxkC11SN-p3Xk6owTF/2nYCs='
        }
    scrapeMoreFeatures = False  ### creates lag
    changeQueryParameters = False  #### set this true to change parameters
    if changeQueryParameters:
        editQueryList = editQuery(payloadDict)
        payloadDict = editQueryList[0]
        keywordsToExclude = editQueryList[1] if scrapeMoreFeatures else []
        keywordsToInclude = editQueryList[2] if scrapeMoreFeatures else []
    else:
        keywordsToExclude = []
        keywordsToInclude = []
    searchType = payloadDict['variables']['searchDetails']['searchType']

    return [url, payloadDict, headers, scrapeMoreFeatures, searchType, keywordsToExclude, keywordsToInclude]


def editQuery(payloadDict):
    searchDetails = payloadDict['variables']['searchDetails']
    searchDetails['searchType'], searchDetails['filters']['sort']['type'], searchDetails['filters'][
        'soldWithin'] = "SOLD", "LAST_SALE_DATE", 9
    searchDetails['location'].pop('cities', None)
    searchDetails['location'].pop('zips', None)
    searchDetails['location']['cities'] = [{"city": "Philadelphia", "state": "PA"}]
    searchDetails['filters']['price'] = {'min': "*", "max": "*"}
    searchDetails['filters']['bedrooms'] = {'min': "4", "max": "*"}
    searchDetails['filters']['bathrooms'] = {'min': "2", "max": "*"}
    # searchDetails['location']['zips'] = ["19142"]
    searchDetails['filters']['limit'] = 25
    searchDetails['filters']['propertyTypes'] = ["MULTI_FAMILY"]
    keywordsToExclude = [x.lower() for x in []]
    keywordsToInclude = [x.lower() for x in []]
    return [payloadDict, keywordsToExclude, keywordsToInclude]


def callMoreFeatures(home, url, headers):
    for attempt in range(0, 5):
        featuresPayloadDict = {
            "operationName": "WEB_homeDetailsClientTopThirdLookUp",
            "variables": {
                "isOffMarket": False,
                "url": "{url}".format(url=home['url']),
                "query": None,
                "searchTypeForQuery": None,
                "isBot": False,
                "limit": 40,
                "filters": {
                    "limit": 40
                },
                "searchDetails": {
                    "searchType": None,
                    "location": {},
                    "filters": {
                        "limit": 40
                    }
                }
            },
            "query": "query WEB_homeDetailsClientTopThirdLookUp($url: String!) {\n  homeDetailsByUrl(url: $url) {\n    url\n    ...HomeDetailsDescriptionFragment\n    ...HomeDetailsListingProviderFragment\n    ...HomeDetailsFeaturesFragment\n    ...HomeDetailsPriceHistoryFragment\n  }\n}\n\nfragment HomeDetailsDescriptionFragment on HOME_Details {\n        __typename\n        description {\n          value\n          formattedDateLastUpdated(dateFormat:\"MMMM DD, YYYY\")\n          contactPhoneNumber\n          additionalInfoHyperlink {\n            title\n            url\n          }\n          subheader\n        }\n      }\n\nfragment HomeDetailsFeaturesFragment on HOME_Details {\n        features {\n          title\n          categories {\n            formattedName\n            ... on HOME_FeatureCategoryGroup {\n              formattedName\n              attributes {\n                ...HomeDetailsFeatureAttributesFragment\n              }\n              additionalNotes {\n                ...HomeDetailsFeatureAttributesFragment\n              }\n              categories {\n                ... on HOME_FeatureSubCategory {\n                  formattedName\n                  formattedSubtitle\n                  attributes {\n                    ...HomeDetailsFeatureAttributesFragment\n                  }\n                  additionalNotes {\n                    ...HomeDetailsFeatureAttributesFragment\n                  }\n                }\n              }\n            }\n            ... on HOME_FeatureSubCategory {\n              formattedName\n              formattedSubtitle\n              attributes {\n                ...HomeDetailsFeatureAttributesFragment\n              }\n              additionalNotes {\n                ...HomeDetailsFeatureAttributesFragment\n              }\n            }\n          }\n        }\n      }\n\nfragment HomeDetailsFeatureAttributesFragment on HOME_FeatureAttributeValue {\n    ... on HOME_FeatureAttributeGenericNameValue {\n      formattedName\n    }\n    ... on HOME_FeatureAttributeLink {\n      formattedName\n      linkURL\n    }\n    formattedValue\n  }\n\n\n\nfragment HomeDetailsListingProviderFragment on HOME_Details {\n        ...on HOME_Property {\n          lastSold {\n            provider {\n              disclaimer {\n                name\n                value\n              }\n            }\n          }\n          activeListing {\n            provider {\n              lastModified\n            }\n          }\n        }\n\n      }\n\nfragment HomeDetailsPriceHistoryFragment on HOME_Property {\n  titleToPriceHistory\n  priceHistory {\n    __typename\n    formattedDate(dateFormat:\"MM/DD/YYYY\")\n    event\n    source\n    mlsLogo\n    ... on HOME_PriceHistoryStandardEvent {\n      price {\n        formattedPrice\n        formattedPriceAbb: formattedPrice(formatType: SHORT_ABBREVIATION)\n      }\n      attributionSource\n    }\n    ... on HOME_PriceHistoryChangeEvent {\n      price {\n        formattedPrice\n        formattedPriceAbb: formattedPrice(formatType: SHORT_ABBREVIATION)\n      }\n      priceChange {\n        priceChangeValue {\n          formattedPrice\n        }\n        priceChangePercent\n        formattedPriceChangePercent\n        priceChangeDirection\n      }\n    }\n    attributes {\n      key\n      formattedAttribute\n    }\n  }\n}"
        }
        featuresPayload = json.dumps(featuresPayloadDict)
        featuresResponse = json.loads(
            requests.request("POST", url, headers=headers, data=featuresPayload, verify=False).text)
        if featuresResponse['data']['homeDetailsByUrl'] is not None:
            break
        print('Attempt to scrape failed, trying again')
    featuresResponse = featuresResponse['data']['homeDetailsByUrl']
    featuresCategories = featuresResponse['features']['categories']
    df = pd.DataFrame(featuresCategories)
    featuresDict = getFeatures(df)
    try:
        description = featuresResponse['description']['value']
    except Exception as e:
        print('Description could not be scraped. Error has occurred: {error}'.format(error=e))
        description = None
    return description, featuresDict


def getFeatures(df):
    featuresDict = OrderedDict()
    if not df[df.formattedName == 'Exterior Features'].empty:
        dfExternalFeatures = searchInDataFrame(df, 'Exterior Features', 'categories')
        dfExteriorHomeFeatures = searchInDataFrame(dfExternalFeatures, 'Exterior Home Features', 'attributes')
        featuresDict['foundation'] = searchInDataFrame(dfExteriorHomeFeatures, 'Foundation', 'formattedValue')
        dfParkingFeatures = searchInDataFrame(dfExternalFeatures, 'Parking & Garage', 'attributes')
        featuresDict['parking'] = searchInDataFrame(dfParkingFeatures, 'Parking', 'formattedValue')
    else:
        featuresDict['foundation'] = None
        featuresDict['parking'] = None
    if not df[df.formattedName == 'Interior Features'].empty:
        dfInternalFeatures = searchInDataFrame(df, 'Interior Features', 'categories')
        dfInternalDetailsFeatures = searchInDataFrame(dfInternalFeatures, 'Interior Details', 'attributes')
        featuresDict['basement'] = searchInDataFrame(dfInternalDetailsFeatures, 'Basement', 'formattedValue')
        dfSquareFootage = searchInDataFrame(dfInternalFeatures, 'Dimensions and Layout', 'attributes')
        featuresDict['floor_sqft'] = searchInDataFrame(dfSquareFootage, 'Living Area',
                                                       'formattedValue')
        if featuresDict['floor_sqft'] is not None:
            featuresDict['floor_sqft'] = featuresDict['floor_sqft'].lower().replace('square feet', 'sqft')
    else:
        featuresDict['basement'] = None
        featuresDict['floor_sqft'] = None
    if not df[df.formattedName == 'Property Information'].empty:
        dfPropertyFeatures = searchInDataFrame(df, 'Property Information', 'categories')
        dfYearBuilt = searchInDataFrame(dfPropertyFeatures, 'Year Built', 'attributes')
        featuresDict['year_built'] = searchInDataFrame(dfYearBuilt, 'Year Built', 'formattedValue')
        #featuresDict['year_built'] = int(featuresDict['year_built']) if featuresDict['year_built'].isnumeric() else \
        #featuresDict['year_built']
        featuresDict['year_renovated'] = searchInDataFrame(dfYearBuilt, 'Year Renovated', 'formattedValue')
        #featuresDict['year_renovated'] = int(featuresDict['year_renovated']) if featuresDict[
        #    'year_renovated'].isnumeric() else featuresDict['year_renovated']
        dfPropertyTypeFeatures = searchInDataFrame(dfPropertyFeatures, 'Property Type / Style', 'attributes')
        # featuresDict['property_type'] = searchInDataFrame(dfPropertyTypeFeatures, 'Property Subtype','formattedValue').lower()
        featuresDict['structure_type'] = searchInDataFrame(dfPropertyTypeFeatures, 'Structure Type', 'formattedValue')
        featuresDict['architecture'] = searchInDataFrame(dfPropertyTypeFeatures, 'Architecture', 'formattedValue')
        dfBuildingFeatures = searchInDataFrame(dfPropertyFeatures, 'Building', 'attributes')
        featuresDict['house_material'] = searchInDataFrame(dfBuildingFeatures, 'Construction Materials',
                                                           'formattedValue')
        dfPropertyInformationFeatures = searchInDataFrame(dfPropertyFeatures, 'Property Information', 'attributes')
        featuresDict['condition'] = searchInDataFrame(dfPropertyInformationFeatures, 'Condition', 'formattedValue')
    else:
        featuresDict['year_built'] = None
        featuresDict['year_renovated'] = None
        # featuresDict['property_type'] = None
        featuresDict['structure_type'] = None
        featuresDict['architecture'] = None
        featuresDict['house_material'] = None
        featuresDict['lot_size'] = None
        featuresDict['condition'] = None
    if not df[df.formattedName == 'Lot Information'].empty:
        dfLotFeatures = searchInDataFrame(df, 'Lot Information', 'attributes')
        featuresDict['lot_size'] = searchInDataFrame(dfLotFeatures, 'Lot Area', 'formattedValue').lower().replace(
            'square feet', 'sqft')
    return featuresDict


def searchInDataFrame(df, searchedName, columnName):
    try:
        return pd.DataFrame(getattr(df[df.formattedName == str(searchedName)], columnName).reset_index(drop=True)[0])
    except Exception as e:
        try:
            return getattr(df[df.formattedName == str(searchedName)], columnName).reset_index(drop=True)[0]
        except Exception as e:
            return None


def appendHomeToList(home, url, headers, scrapeMoreFeatures, searchType, keywordsToExclude, keywordsToInclude):
    attributesToDelete = ['media', 'displayFlags', 'activeForSaleListing', 'tags', 'isSaveable',
                          'preferences', 'providerListingId']
    for attribute in attributesToDelete:
        home.pop(attribute, None)
    homeDict = OrderedDict()
    try:
        homeDict['location'] = ' '.join(home['location']['fullLocation'].split())
        homeDict['address'] = ' '.join(home['location']['partialLocation'].split())
        homeDict['asking_price'] = int(home['price']['formattedPrice'].replace('$', '').replace(',', ''))
    except AttributeError as e:
        if home['location']:
            print('{address} could not be added due to missing asking price'.format(
                address=home['location']['partialLocation']))
        else:
            print('House could not be added due to missing address')
        return None
    except ValueError as e:
        if home['location']:
            print('{address} was not added due to non-specific asking price'.format(
                address=home['location']['partialLocation']))
        else:
            print('House was not added due to non-specific asking price')
        return None
    if scrapeMoreFeatures:
        description, featuresDict = callMoreFeatures(home, url, headers)
        descriptionKeywordsList = []
        for (keywordToExclude, keywordToInclude) in itertools.zip_longest(keywordsToExclude, keywordsToInclude, fillvalue='No keywords left'):
            if keywordToExclude in description:
                print('Keyword {kw} found in description for {house}. Excluded in scrape.'.format(kw=keywordToExclude,
                                                                                                  house=homeDict['address']))
                return None
            elif keywordToInclude in description:
                descriptionKeywordsList.append(keywordToInclude)
        homeDict['description'] = description
        if len(keywordsToInclude) == 0:
            homeDict['description_keywords'] = 'User decided not to filter keywords'
        else:
            homeDict['description_keywords'] = ", ".join(descriptionKeywordsList) if len(descriptionKeywordsList) != 0 else 'No keywords found'
    else:
        homeDict['description'] = 'User decided not to scrape'
        homeDict['description_keywords'] = 'User decided not to scrape'
        featuresDict = {}

    try:
        homeDict['city'] = home['location']['city'] if home['location']['city'] else None
        homeDict['state'] = home['location']['stateCode'] if home['location']['stateCode'] else None
        homeDict['zip'] = home['location']['zipCode'] if home['location']['zipCode'] else None
        homeDict['floor_sqft'] = home['floorSpace']['formattedDimension'] if home['floorSpace'] else None
        homeDict['lot_size'] = home['lotSize']['formattedDimension'] if home['lotSize'] else None
        if home['bedrooms']:
            if home['bedrooms']['formattedValue'].lower() == 'studio':
                homeDict['bedrooms'] = 'studio'
            else:
                homeDict['bedrooms'] = int(re.sub('[^0-9]', '', home['bedrooms']['formattedValue']))
        else:
            homeDict['bedrooms'] = None
        homeDict['bathrooms'] = re.sub('[^0-9.]', '', home['bathrooms']['formattedValue']) if home[
            'bathrooms'] else None
        homeDict['trulia_listing_id'] = home['metadata']['legacyIdForSave']
        try:
            if searchType == "FOR_SALE":
                homeDict['date_listed_or_sold'] = home['activeListing']['dateListed'].split("T")[0]
            elif searchType == "SOLD":
                homeDict['date_listed_or_sold'] = datetime.strptime(home['fullTags'][1]['formattedName'],
                                                                 '%b %d, %Y').strftime('%Y-%m-%d')
        except Exception as e:
            print('An error has occurred:{e}. Date listed/sold was unable to be scraped for {house}'.format(
                e=e, house=homeDict['address']))
            homeDict['date_listed_or_sold'] = None
        df = pd.DataFrame(home['tracking'])
        homeDict['neighborhood'] = next(iter(df.loc[df.key == 'listingNeighborhood']['value'].to_numpy()), None)
        homeDict['property_type'] = next(iter(df.loc[df.key == 'propertyType']['value'].to_numpy()), None)
        itemStringFromDict = next(iter(df.loc[df.key == 'item']['value'].to_numpy()), None)
        if itemStringFromDict is not None:
            homeDict['parking'] = re.search('Parking:(.*?);', itemStringFromDict).group(1)
            homeDict['year_built'] = re.search('Year Built:(.*?);', itemStringFromDict).group(1)
        else:
            homeDict['parking'] = None
            homeDict['year_built'] = None
        homeDict['trulia_url'] = "trulia.com" + home['url']
        if home['currentStatus']['isRecentlySold']:
            homeDict['listing_status'] = 'Sold'
        elif home['currentStatus']['isActiveForSale']:
            homeDict['listing_status'] = 'Listed For Sale'
        else:
            homeDict['listing_status'] = 'Unknown'
    except Exception as e:
        print('An error has occurred: {error}. {address} was unable to be scraped.'.format(error=e,
                                                                                           address=homeDict[
                                                                                               'address']))
        return None
    homeDict.update(featuresDict)
    if scrapeMoreFeatures:
        correctOrder = ['location', 'address', 'asking_price', 'city', 'state', 'zip', 'floor_sqft', 'lot_size',
                        'bedrooms', 'bathrooms', 'neighborhood', 'property_type', 'parking', 'year_built',
                        'year_renovated', 'condition', 'foundation', 'basement', 'structure_type', 'architecture',
                        'house_material', 'listing_status', 'date_listed_or_sold', 'trulia_url', 'trulia_listing_id',
                        'description_keywords','description']
    else:
        correctOrder = ['location', 'address', 'asking_price', 'city', 'state', 'zip', 'floor_sqft', 'lot_size',
                        'bedrooms', 'bathrooms', 'neighborhood', 'property_type', 'parking', 'year_built',
                        'listing_status', 'date_listed_or_sold', 'trulia_url', 'trulia_listing_id', 'description_keywords','description']
    homeDict = OrderedDict((key, homeDict[key]) for key in correctOrder)
    print('{house} successfully scraped'.format(house=homeDict['address']))
    return homeDict


def scrapeTrulia():
    loadedQueriesList = initializeRequest()
    url = loadedQueriesList[0]
    payload = loadedQueriesList[1]
    headers = loadedQueriesList[2]
    scrapeMoreFeatures = loadedQueriesList[3]
    searchType = loadedQueriesList[4]
    keywordsToExclude = loadedQueriesList[5]
    keywordsToInclude = loadedQueriesList[6]
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)

    jsonString = response.text
    homesDumpJson = json.loads(jsonString)
    listOfHomesRaw = homesDumpJson['data']['searchResultMap']['homes']  ### index = house index
    listOfScrapedHomes = []
    for home in listOfHomesRaw:
        homeDict = appendHomeToList(home, url, headers, scrapeMoreFeatures, searchType, keywordsToExclude,
                                    keywordsToInclude)
        if homeDict is not None:
            listOfScrapedHomes.append(homeDict)
    print("{num} listings scraped".format(num=len(listOfScrapedHomes)))
    return listOfScrapedHomes


if __name__ == "__main__":
    scrapeTrulia()

