export class ApiError extends Error {
    error: string;
    status: number;
    success: boolean;

    constructor(message: string, status: number){
        super(message);
        this.success = false;
        this.error = message;
        this.status = status;
    }
}


const makeRequest = async (
    endpoint: string, 
    method: string, 
    headers: Record<string, string> = {},
    params?: Record<string, string | number>,
    requestBody?: Map<string, any>
): Promise<any> => {
    try {
        let requestUrl = new URL(endpoint, window.location.origin);
        if (params) {
            Object.keys(params).forEach(key => requestUrl.searchParams.append(key, params[key].toString()));
        }

        const hasData: boolean = ((method === "POST" || method === "PUT") && !!requestBody)

        const requestDetails: Object = {
            method: method,
            headers: hasData ? {...headers, 'Content-Type': 'application/json'} : headers,
            body: hasData? JSON.stringify(requestBody) : undefined,
            credentials: 'include',
        }

        const response = await fetch(requestUrl.toString(), requestDetails)

        if (!response.ok) {
            const body = JSON.parse(await response.text());
            if (Object.prototype.hasOwnProperty.call(body, 'error') && body.error) {
                throw new ApiError(body.error, response.status);
            } else {
                throw new ApiError(`HTTP Error: ${JSON.stringify(body)}`, response.status);
            }
        }

        const responseJson = await response.json();
        if (Object.prototype.hasOwnProperty.call(responseJson, 'success') && Object.prototype.hasOwnProperty.call(responseJson, 'data') && responseJson.success) {
            return responseJson.data;
        } else {
            throw new ApiError(`${responseJson.message}`, 500);
        }
    } catch (error: any) {
        let errorToThrow: Error = error;
        if (!(error instanceof ApiError)){
            errorToThrow = new ApiError(`An error occurred while making a request: ${error.message}`, 500)
        }
        console.error(`The following error has occurred while making request: "${errorToThrow.message}"`)
        throw errorToThrow
    }
}


export default makeRequest 

