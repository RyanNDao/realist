export function convertToMap(data: Object): Map<string, any> {
    const map = new Map<string, any>();
    Object.keys(data).forEach(key => {
        map.set(key, data[key]);
    });
    return map;
}