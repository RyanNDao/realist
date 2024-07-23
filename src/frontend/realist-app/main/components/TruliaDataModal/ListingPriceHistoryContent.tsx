import React from "react";
import { PriceHistory } from "../../helpers/globalInterfaces";

interface ListingPriceHistoryContentProps{
    priceHistory: PriceHistory[]
}

export function ListingPriceHistoryContent({priceHistory}: ListingPriceHistoryContentProps) {
    return (

        <> {JSON.stringify(priceHistory)}
        TO BE BEAUTIFIED!</>
    )
}