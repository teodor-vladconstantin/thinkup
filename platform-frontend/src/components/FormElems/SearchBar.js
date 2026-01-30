import react, { useEffect, useState } from "react";
import styles from "../../../styles/SearchBar.module.css";

const SearchBar = (props) => {
    const handleSubmit = (e) => {
        e.preventDefault();
        props.onsearch();
    };

    const handleKeyPress = (e) => {
        //it triggers by pressing the enter key
        if (e.charCode === 13) {
            handleSubmit(e);
        }
    };

    return (
        <div className={styles.SearchBar + " " + props.className}>
            {props.search_type==undefined?<></>:<img
                className={styles.SearchTypeBtn}
                src={props.search_type=="projects"?"/folder_icon.svg":"/user_icon.svg"}
                onClick={() => props.changeSearchType()}/>}
            <input
                className={styles.SearchBarInput}
                placeholder={props.Placeholder}
                value={props.search_value}
                onChange={(e) => props.changeValue(e)}
                onKeyPress={handleKeyPress}
            />
            <img
                className={styles.SearchBarBtn}
                src="/icon_search.svg"
                onClick={() => props.onsearch()}
            />
        </div>
    );
};

export default SearchBar;
