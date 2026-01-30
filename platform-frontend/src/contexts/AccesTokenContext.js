import React,{useContext , useState ,useEffect} from "react";
import useAccesToken from '../hooks/useAccesToken';

const AccesTokenContext  = React.createContext();

export function useAccesTokenContext(){
    return useContext(AccesTokenContext);
}


export function AccesTokenProvider({children}){
    const AccesToken = useAccesToken();

    return(
        <AccesTokenContext.Provider value={AccesToken}>
                {children}
        </AccesTokenContext.Provider>

    )
}

