import React,{useContext , useState ,useEffect} from "react";
import useDarkMode from '../hooks/useDarkMode';

const ThemeContext  = React.createContext();
const ThemeUpdateContext  = React.createContext();

export function useTheme(){
    return useContext(ThemeContext);
}

export function useThemeUpdate(){
    return useContext(ThemeUpdateContext);
}

export function ThemeProvider({children}){
    const [darkTheme, setDarkTheme] = useDarkMode();

    useEffect(()=>{
        console.log(darkTheme);
    },[])


    const toggleTheme = () =>{
        setDarkTheme(!darkTheme);
    }

    return(
        <ThemeContext.Provider value={darkTheme}>
            <ThemeUpdateContext.Provider value={toggleTheme}>
                {children}
            </ThemeUpdateContext.Provider>
        </ThemeContext.Provider>

    )
}
