import { Flex, Select } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { TruliaDataTable } from "../table_components/TruliaDataTable/TruliaDataTable";
import { ApiTruliaListingResponse, TruliaListingFull, TruliaListingSummary } from "../../helpers/globalInterfaces";
import { TruliaDataModal } from "../TruliaDataModal/TruliaDataModal";
import { RowClickedEvent } from "ag-grid-community"

interface DataContainerProps{
    isFetching: boolean,
    rentalData?: ApiTruliaListingResponse[],
    listingsData?: ApiTruliaListingResponse[],
}


export function DataContainer({isFetching, rentalData, listingsData}: DataContainerProps) {
    
    const [tableDataType, setTableDataType ] = useState<"listings" | "rentals" | "sold">("listings");
    const [isDataModalOpen, setIsDataModalOpen] = useState(true);
    const [activeListing, setActiveListing] = useState<TruliaListingFull | undefined>(undefined)

    

    const onTableListingClick = (e: RowClickedEvent, fullListingsData: TruliaListingFull[]) => {
        let rowData = e.data as TruliaListingSummary
        let foundFullListing = fullListingsData.find((listing) => {return listing.key === rowData.key})
        if (foundFullListing){
            setIsDataModalOpen(true);
            setActiveListing(foundFullListing);
        } else {
            console.error(`Unexpected error where listing with key ${rowData?.key} was not found in listings data!`)
        }
    }

    const onSelectTableDataTypeChange = (event: any) => {
        const dataType = event.target.value;
        setTableDataType(dataType);
        console.log('Selected option:', dataType);
    }

    
    
    return (
        <Flex flexDirection="column" height="100%" justifyContent="space-between" gap="10px">
            {!isFetching &&
                <Select width="60%" value={tableDataType} onChange={onSelectTableDataTypeChange}>
                    <option value='listings'>For Sale</option>
                    <option value='rentals'>For Rent</option>
                    <option value='sold'>Sold</option>
                </Select>
            }
            {activeListing &&
                <TruliaDataModal
                    isOpen={isDataModalOpen}
                    setIsOpen={setIsDataModalOpen}
                    activeListing={activeListing}
                />
            }
            { tableDataType === "listings" &&
                <TruliaDataTable
                    isFetching={isFetching}
                    onListingClick={onTableListingClick}
                    listings={listingsData}
                />
            }
            { tableDataType === "rentals" &&
                <TruliaDataTable
                    isFetching={isFetching}
                    onListingClick={onTableListingClick}
                    listings={rentalData}
                />
            }
            { tableDataType === "sold" &&
                <div>Coming soon</div>
            }
        </Flex>
    )
}