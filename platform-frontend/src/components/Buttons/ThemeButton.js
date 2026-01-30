import react,{useEffect , useState} from "react";
import styles from '../../../styles/ThemeButton.module.css';
import useDarkMode from '../../hooks/useDarkMode';
import {useTheme,useThemeUpdate } from '../../contexts/ThemeContext'

const ThemeButton = (props) =>{
    const Theme = useTheme();
    const ToggleTheme = useThemeUpdate();


    return (
        <div className={styles.ThemeButton +' '+props.className} onClick={()=>ToggleTheme()}>
            {Theme?
            <img src="/bi_moon-fill.svg"/>
            :<img src="/bi_sun.svg"/>
            }
        </div>
    )
}

export default ThemeButton;