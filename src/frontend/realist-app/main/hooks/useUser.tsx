import React, { createContext, useContext, useState } from 'react';
import { ApiSuccessResponse, UserData } from '../helpers/globalInterfaces';
import makeRequest from '../helpers/apiHelper';

interface UserContextType {
    user?: UserData;
    login: (username: string, password: string) => Promise<ApiSuccessResponse>;
    logout: () => void;
}

const UserContext = createContext<UserContextType | null>(null);

export const UserProvider = ({children}) => {
    const [user, setUser] = useState<UserData | undefined>(undefined);

    const login = async (username: string, password: string) => {
        let data: ApiSuccessResponse = await makeRequest('api/user/authenticate', 'POST', {}, {}, {username, password})
        setUser(data.data)
        return data;
        // on error here, it will propagate upwards
    }

    const logout = () => {
        setUser(undefined);
    }

    return (
        <UserContext.Provider value={{ user, login, logout }}>
            {children}
        </UserContext.Provider>
    );
}

export const useUser = (): UserContextType => {
    const context = useContext(UserContext);
    if (context === null) {
        throw new Error("useUser must be used within a UserProvider");
    }
    return context;
};