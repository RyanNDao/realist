import React, { useEffect, useState } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import 'leaflet/dist/leaflet.css';
import { Box } from "@chakra-ui/react";
import { Map } from "leaflet";
import { ApiTruliaListingResponse, TruliaListingFull } from "../../../helpers/globalInterfaces";
import '../leafletMap.css'
import { returnTruliaFullAndSummaryListFromApiTruliaResponse } from "../../../helpers/common";

interface TruliaHouseMapProps {
    forSale?: ApiTruliaListingResponse[],
    forRent?: ApiTruliaListingResponse[],
    sold?: ApiTruliaListingResponse[],
    setActiveListing: (arg0: TruliaListingFull) => void,
    setIsDataModalOpen: (arg0: boolean) => void,
}


export function TruliaHouseMap({forSale, forRent, sold, setActiveListing, setIsDataModalOpen}: TruliaHouseMapProps){
    const [map, setMap] = useState<Map | null>(null);
    const [fullData, setFullData] = useState<TruliaListingFull[] | null>(null);

    useEffect(() => {
        if (map) {
           setInterval(() => {
              map.invalidateSize();
           }, 100);
        }
     }, [map]);

    useEffect(()=>{
        if (sold){
            let listingsList = returnTruliaFullAndSummaryListFromApiTruliaResponse(sold)
            setFullData(listingsList.listingsFullList)
        }
    }, [sold])
    
    return (
        <Box as="div" id="map">
            <MapContainer center={[39.9526, -75.1652]} zoom={13} scrollWheelZoom={false} ref={setMap}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {/* <Marker position={[51.505, -0.09]}>
                    <Popup>
                        A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker> */}
                {fullData?.map((listing)=>{
                    return (listing.latitude && listing.longitude) 
                    ? <Marker 
                        key={`${listing.key}`}
                        position={[listing.latitude,listing.longitude]}
                        
                        eventHandlers={{
                            click: () => {
                                setActiveListing(listing);
                                setIsDataModalOpen(true);
                            },
                        }}
                    />
                    : <></>
                })}
            </MapContainer>
        </Box>
    )
}