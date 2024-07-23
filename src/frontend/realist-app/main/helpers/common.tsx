import { format } from 'date-fns';
import { toZonedTime } from 'date-fns-tz';

export function convertToMap(data: Object): Map<string, any> {
    const map = new Map<string, any>();
    Object.keys(data).forEach(key => {
        map.set(key, data[key]);
    });
    return map;
}

export function formatDbDate(dateString: string, timezone: string  = 'GMT'){ 
    let dateObject = new Date(dateString)
    const dateInTimezone = toZonedTime(dateObject, timezone);
    return format(dateInTimezone, 'yyyy-MM-dd');
}

export function formatCamelCase(inputString: string){
    const spaced = inputString.replace(/([A-Z])/g, ' $1').trim();
    return spaced.charAt(0).toUpperCase() + spaced.slice(1);
}

export function formatNumberToMoney(inputNumber: number){
    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
    });
    return formatter.format(inputNumber);
}