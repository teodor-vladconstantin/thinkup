
import React,{useContext , useState, useEffect } from "react";
import { useUser } from "@auth0/nextjs-auth0";
import { useRouter } from "next/router";
import useMyUser from "../hooks/useMyUser";

const MyUserContext  = React.createContext();
const MyUserUpdateContext  = React.createContext();

export function useMyUserContext(){
    return useContext(MyUserContext);

}export function useMyUserUpdate(){
    return useContext(MyUserUpdateContext);
}

export function MyUserProvider({children}){
    const [User,setUser] = useMyUser();

    const updateUser = (data)=>{
        setUser(data)
    }


    return(
        <MyUserContext.Provider value={User}>
            <MyUserUpdateContext.Provider value={updateUser}>
                {children}
            </MyUserUpdateContext.Provider>
        </MyUserContext.Provider>

    )
}
