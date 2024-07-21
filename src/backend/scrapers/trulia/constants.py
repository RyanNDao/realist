from string import Template
from dotenv import load_dotenv
import os

load_dotenv()

# Trulia uses pxvid cookie (perimeter X) to validate requests
TRULIA_HEADERS = {
    'Content-Type': 'application/json',
    'Cookie': os.getenv('TRULIA_COOKIE', '')
    ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0'
}

TRULIA_HOUSE_SCAN_DEFAULT_QUERY_VARIABLES = {
    "isSwipeableFactsEnabled": False,
    "heroImageFallbacks": [
        "STREET_VIEW",
        "SATELLITE_VIEW"
    ],
    "searchDetails": {
        "searchType": "FOR_SALE",
        "location": {
            "zips": [],
            "cities": [],
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
}

GRAPHQL_HOUSE_SCAN_PAYLOAD_TEMPLATE = {
	"operationName": "WEB_searchResultsMapQuery",
	"query": None,
	"variables": None
}


GRAPHQL_HOUSE_SCAN_QUERY = r"""query WEB_searchResultsMapQuery($searchDetails: SEARCHDETAILS_Input!, $heroImageFallbacks: [MEDIA_HeroImageFallbackTypes!], $includeOffMarket: Boolean!, $includeLocationPolygons: Boolean!, $isSPA: Boolean!, $includeNearBy: Boolean!, $isSwipeableFactsEnabled: Boolean = false) {
		searchResultMap: searchHomesByDetails(searchDetails: $searchDetails, includeNearBy: $includeNearBy) {
			...SearchResultsMapClientFragment
			__typename
		}
		offMarketHomes: searchOffMarketHomes(searchDetails: $searchDetails) @include(if: $includeOffMarket) {
			...HomeMarkerLayersContainerFragment
			...HoverCardLayerFragment
			__typename
		}
	}

	fragment SearchResultsMapClientFragment on SEARCH_Result {
	...HomeMarkerLayersContainerFragment
	...HoverCardLayerFragment
	...SearchLocationBoundaryFragment @include(if: $includeLocationPolygons)
	...SchoolSearchMarkerLayerFragment
	...TransitLayerFragment
	__typename
	}

	fragment HomeMarkerLayersContainerFragment on SEARCH_Result {
	...HomeMarkersLayerFragment
	__typename
	}

	fragment HomeMarkersLayerFragment on SEARCH_Result {
	homes {
		location {
		coordinates {
			latitude
			longitude
			__typename
		}
		__typename
		}
		url
		metadata {
		compositeId
		__typename
		}
		...HomeMarkerFragment
		__typename
	}
	nearByHomes {
		...HomeMarkerFragment
		__typename
	}
	__typename
	}

	fragment HomeMarkerFragment on HOME_Details {
	media {
		hasThreeDHome
		__typename
	}
	location {
		coordinates {
		latitude
		longitude
		__typename
		}
		__typename
	}
	displayFlags {
		enableMapPin
		__typename
	}
	price {
		calloutMarkerPrice: formattedPrice(formatType: SHORT_ABBREVIATION)
		__typename
	}
	url
	... on HOME_Property {
		activeForSaleListing {
		openHouses {
			formattedDay
			__typename
		}
		__typename
		}
		__typename
	}
	...HomeDetailsTopThirdFragment @include(if: $isSPA)
	__typename
	}

	fragment HomeDetailsTopThirdFragment on HOME_Details {
	bathrooms {
		summaryBathrooms: formattedValue(formatType: COMMON_ABBREVIATION)
		__typename
	}
	bedrooms {
		summaryBedrooms: formattedValue(formatType: COMMON_ABBREVIATION)
		__typename
	}
	floorSpace {
		formattedDimension
		__typename
	}
	location {
		city
		coordinates {
		latitude
		longitude
		__typename
		}
		neighborhoodName
		stateCode
		zipCode
		cityStateZipAddress: formattedLocation(formatType: CITY_STATE_ZIP)
		homeFormattedAddress: formattedLocation
		summaryFormattedLocation: formattedLocation(formatType: STREET_COMMUNITY_BUILDER)
		__typename
	}
	media {
		metaTagHeroImages: heroImage(fallbacks: $heroImageFallbacks) {
		url {
			desktop: custom(size: {width: 2048, height: 200})
			__typename
		}
		__typename
		}
		topThirdHeroImages: heroImage(fallbacks: $heroImageFallbacks) {
		__typename
		url {
			extraSmallSrc: custom(size: {width: 375, height: 275})
			smallSrc: custom(size: {width: 570, height: 275})
			mediumSrc: custom(size: {width: 768, height: 500})
			largeSrc: custom(size: {width: 992, height: 500})
			hiDipExtraSmallSrc: custom(size: {width: 1125, height: 825})
			hiDpiSmallSrc: custom(size: {width: 1710, height: 825})
			hiDpiMediumSrc: custom(size: {width: 2048, height: 1536})
			__typename
		}
		webpUrl: url(compression: webp) {
			extraSmallWebpSrc: custom(size: {width: 375, height: 275})
			smallWebpSrc: custom(size: {width: 570, height: 275})
			mediumWebpSrc: custom(size: {width: 768, height: 500})
			largeWebpSrc: custom(size: {width: 992, height: 500})
			hiDipExtraSmallWebpSrc: custom(size: {width: 1125, height: 825})
			hiDpiSmallWebpSrc: custom(size: {width: 1710, height: 825})
			hiDpiMediumWebpSrc: custom(size: {width: 2048, height: 1536})
			__typename
		}
		}
		totalPhotoCount
		__typename
	}
	metadata {
		compositeId
		currentListingId
		__typename
	}
	pageText {
		title
		metaDescription
		__typename
	}
	price {
		formattedPrice
		... on HOME_LastSoldPrice {
		formattedPriceDifferencePercent
        formattedSoldDate(dateFormat: "MMM D, YYYY")
		listingPrice {
			formattedPrice(formatType: SHORT_ABBREVIATION)
			__typename
		}
		priceDifferencePercent
		pricePerDimension {
			formattedDimension
			__typename
		}
		__typename
		}
		... on HOME_ForeclosureEstimatePrice {
		price
		typeDescription
		__typename
		}
		... on HOME_PriceRange {
		currencyCode
		max
		min
		__typename
		}
		... on HOME_SinglePrice {
		currencyCode
		price
		__typename
		}
		__typename
	}
	tracking {
		key
		value
		__typename
	}
	url
	... on HOME_Property {
		currentStatus {
		isOffMarket
		isRecentlySold
		isForeclosure
		isActiveForRent
		isActiveForSale
		isRecentlyRented
		label
		__typename
		}
		__typename
	}
	... on HOME_RentalCommunity {
		location {
		rentalCommunityFormattedLocation: formattedLocation(formatType: STREET_COMMUNITY_NAME)
		__typename
		}
		__typename
	}
	__typename
	}

	fragment HoverCardLayerFragment on SEARCH_Result {
	homes {
		...HomeHoverCardFragment
		__typename
	}
	nearByHomes {
		...HomeHoverCardFragment
		__typename
	}
	__typename
	}

	fragment HomeHoverCardFragment on HOME_Details {
	...HomeDetailsCardFragment
	...HomeDetailsCardHeroFragment
	...HomeDetailsCardPhotosFragment
	...HomeDetailsGroupInsightsFragment @include(if: $isSwipeableFactsEnabled)
	location {
		coordinates {
		latitude
		longitude
		__typename
		}
		__typename
	}
	displayFlags {
		enableMapPin
		showMLSLogoOnMapMarkerCard
		__typename
	}
	__typename
	}

	fragment HomeDetailsCardFragment on HOME_Details {
	__typename
	location {
		city
		stateCode
		zipCode
        neighborhoodName
		fullLocation: formattedLocation(formatType: STREET_CITY_STATE_ZIP)
		partialLocation: formattedLocation(formatType: STREET_ONLY)
		__typename
	}
	price {
		formattedPrice
		__typename
	}
	url
	tags(include: MINIMAL) {
		level
		formattedName
		icon {
		vectorImage {
			svg
			__typename
		}
		__typename
		}
		__typename
	}
	fullTags: tags {
		level
		formattedName
		icon {
		vectorImage {
			svg
			__typename
		}
		__typename
		}
		__typename
	}
	floorSpace {
		formattedDimension
		__typename
	}
	lotSize {
		... on HOME_SingleDimension {
		formattedDimension(minDecimalDigits: 2, maxDecimalDigits: 2)
		__typename
		}
		__typename
	}
	bedrooms {
		formattedValue(formatType: TWO_LETTER_ABBREVIATION)
		__typename
	}
	bathrooms {
		formattedValue(formatType: TWO_LETTER_ABBREVIATION)
		__typename
	}
	isSaveable
	preferences {
		isSaved
		isSavedByCoShopper @include(if: false)
		__typename
	}
	metadata {
		compositeId
		legacyIdForSave
		__typename
	}
	tracking {
		key
		value
		__typename
	}
	displayFlags {
		showMLSLogoOnListingCard
		addAttributionProminenceOnListCard
		__typename
	}
	... on HOME_RoomForRent {
		numberOfRoommates
		providerListingId
		__typename
	}
	... on HOME_RentalCommunity {
		activeListing {
		provider {
			summary(formatType: SHORT)
			listingSource {
			logoUrl
			__typename
			}
			__typename
		}
		__typename
		}
		location {
		communityLocation: formattedLocation(formatType: STREET_COMMUNITY_NAME)
		__typename
		}
		providerListingId
		__typename
	}
	... on HOME_Property {
		currentStatus {
		isRecentlySold
		isRecentlyRented
		isActiveForRent
		isActiveForSale
		isOffMarket
		isForeclosure
		__typename
		}
		priceChange {
		priceChangeDirection
		__typename
		}
		activeListing {
		provider {
			summary(formatType: SHORT)
			extraShortSummary: summary(formatType: EXTRA_SHORT)
			listingSource {
			logoUrl
			__typename
			}
			__typename
		}
		dateListed
		__typename
		}
		lastSold {
		provider {
			summary(formatType: SHORT)
			extraShortSummary: summary(formatType: EXTRA_SHORT)
			listingSource {
			logoUrl
			__typename
			}
			__typename
		}
		__typename
		}
		providerListingId
		__typename
	}
	... on HOME_FloorPlan {
		priceChange {
		priceChangeDirection
		__typename
		}
		provider {
		summary(formatType: SHORT)
		__typename
		}
		__typename
	}
	}

	fragment HomeDetailsCardHeroFragment on HOME_Details {
	media {
		heroImage(fallbacks: $heroImageFallbacks) {
		url {
			small
			medium
			__typename
		}
		webpUrl: url(compression: webp) {
			small
			__typename
		}
		__typename
		}
		__typename
	}
	__typename
	}

	fragment HomeDetailsCardPhotosFragment on HOME_Details {
	media {
		__typename
		heroImage(fallbacks: $heroImageFallbacks) {
		url {
			small
			medium
			__typename
		}
		webpUrl: url(compression: webp) {
			small
			medium
			__typename
		}
		__typename
		}
		photos {
		url {
			small
			medium
			__typename
		}
		webpUrl: url(compression: webp) {
			small
			medium
			__typename
		}
		__typename
		}
	}
	__typename
	}

	fragment HomeDetailsGroupInsightsFragment on HOME_Details {
	... on HOME_Property {
		groupedInsights {
		insights {
			... on HOME_FeatureInsights {
			insightTags {
				formattedName
				__typename
			}
			__typename
			}
			... on HOME_SmartInsights {
			insightTags {
				formattedName
				__typename
			}
			__typename
			}
			... on HOME_ContextualPhrases {
			phrases {
				description
				__typename
			}
			__typename
			}
			__typename
		}
		__typename
		}
		__typename
	}
	__typename
	}

	fragment SearchLocationBoundaryFragment on SEARCH_Result {
	location {
		encodedPolygon
		... on SEARCH_ResultLocationCity {
		locationId
		__typename
		}
		... on SEARCH_ResultLocationCounty {
		locationId
		__typename
		}
		... on SEARCH_ResultLocationNeighborhood {
		locationId
		__typename
		}
		... on SEARCH_ResultLocationPostalCode {
		locationId
		__typename
		}
		... on SEARCH_ResultLocationState {
		locationId
		__typename
		}
		__typename
	}
	__typename
	}

	fragment SchoolSearchMarkerLayerFragment on SEARCH_Result {
	schools {
		...SchoolMarkersLayerFragment
		__typename
	}
	__typename
	}

	fragment SchoolMarkersLayerFragment on School {
	id
	latitude
	longitude
	categories
	...SchoolHoverCardFragment
	__typename
	}

	fragment SchoolHoverCardFragment on School {
	id
	name
	gradesRange
	providerRating {
		rating
		__typename
	}
	streetAddress
	studentCount
	latitude
	longitude
	__typename
	}

	fragment TransitLayerFragment on SEARCH_Result {
	transitStations {
		stationName
		iconUrl
		coordinates {
		latitude
		longitude
		__typename
		}
		radius
		__typename
	}
	__typename
	}
""".replace('\n', '').replace('\t','    ')

GRAPHQL_DETAILED_SCRAPE_PAYLOAD_TEMPLATE = {
	"query": None,
	"variables": None
}

GRAPHQL_DETAILED_SCRAPE_QUERY_TEMPLATE = """
    query WEB_homeDetailsClientTopThirdLookUp({params}) {{
        {queryParts}
    }}

    fragment HomeDetailsDescriptionFragment on HOME_Details {{
        __typename
        description {{
            value
            formattedDateLastUpdated(dateFormat: "MMMM DD, YYYY")
            contactPhoneNumber
            additionalInfoHyperlink {{
                title
                url
            }}
            subheader
        }}
    }}

    fragment HomeDetailsFeaturesFragment on HOME_Details {{
        features {{
            title
            categories {{
                formattedName
                ... on HOME_FeatureCategoryGroup {{
                    formattedName
                    attributes {{
                        ...HomeDetailsFeatureAttributesFragment
                    }}
                    additionalNotes {{
                        ...HomeDetailsFeatureAttributesFragment
                    }}
                    categories {{
                        ... on HOME_FeatureSubCategory {{
                            formattedName
                            formattedSubtitle
                            attributes {{
                                ...HomeDetailsFeatureAttributesFragment
                            }}
                            additionalNotes {{
                                ...HomeDetailsFeatureAttributesFragment
                            }}
                        }}
                    }}
                }}
                ... on HOME_FeatureSubCategory {{
                    formattedName
                    formattedSubtitle
                    attributes {{
                        ...HomeDetailsFeatureAttributesFragment
                    }}
                    additionalNotes {{
                        ...HomeDetailsFeatureAttributesFragment
                    }}
                }}
            }}
        }}
    }}

    fragment HomeDetailsFeatureAttributesFragment on HOME_FeatureAttributeValue {{
        ... on HOME_FeatureAttributeGenericNameValue {{
            formattedName
        }}
        ... on HOME_FeatureAttributeLink {{
            formattedName
            linkURL
        }}
        formattedValue
    }}

    fragment HomeDetailsListingProviderFragment on HOME_Details {{
        ... on HOME_Property {{
            lastSold {{
                provider {{
                    disclaimer {{
                        name
                        value
                    }}
                }}
            }}
            activeListing {{
                provider {{
                    lastModified
                }}
            }}
        }}
    }}
    
    fragment HomeDetailsNeighborhoodOverviewFragment on HOME_Details {{
		surroundings {{
			...NeighborhoodCardFragment
			... on SURROUNDINGS_Neighborhood {{
				neighborhoodAttribution
				__typename
			}}
			__typename
		}}
		__typename
	}}

	fragment NeighborhoodCardFragment on SURROUNDINGS_Neighborhood {{
		name
		ndpActive
		ndpUrl
		localFacts {{
			forSaleStats {{
				min
				max
				__typename
			}}
			homesForSaleCount
			forRentStats {{
				min
				max
				__typename
			}}
			homesForRentCount
			soldHomesStats {{
				min
				max
				__typename
			}}
			soldHomesCount
			__typename
		}}
		neighborhoodSearchUrlCTA {{
			forSale
			forRent
			__typename
		}}
		__typename
	}}

    fragment HomeDetailsPriceHistoryFragment on HOME_Property {{
        titleToPriceHistory
        priceHistory {{
            __typename
            formattedDate(dateFormat: "MM/DD/YYYY")
            event
            source
            mlsLogo
            ... on HOME_PriceHistoryStandardEvent {{
                price {{
                    formattedPrice
                    formattedPriceAbb: formattedPrice(formatType: SHORT_ABBREVIATION)
                }}
                attributionSource
            }}
            ... on HOME_PriceHistoryChangeEvent {{
                price {{
                    formattedPrice
                    formattedPriceAbb: formattedPrice(formatType: SHORT_ABBREVIATION)
                }}
                priceChange {{
                    priceChangeValue {{
                        formattedPrice
                    }}
                    priceChangePercent
                    formattedPriceChangePercent
                    priceChangeDirection
                }}
            }}
            attributes {{
                key
                formattedAttribute
            }}
        }}
    }}
"""

TRULIA_DEFAULT_PAYLOAD__LEGACY = {
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