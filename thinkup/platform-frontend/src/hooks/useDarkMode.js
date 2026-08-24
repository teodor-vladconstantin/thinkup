import react,{useState,useEffect} from "react";

const useDarkMode = () =>{
    const [darkTheme, setDarkTheme] = useState(undefined);

    useEffect(() => {
        if (darkTheme !== undefined) {
          if (darkTheme) {
            // Set value of  darkmode to dark
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
          } else {
            // Set value of  darkmode to light
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
          }
        }
      }, [darkTheme]);
    
      useEffect(() => {
        // Set initial mode
        setDarkTheme(localStorage.getItem('theme') === 'dark');
      }, []);

    return [darkTheme, setDarkTheme];
}

export default useDarkMode;
