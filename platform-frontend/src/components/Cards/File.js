import styles from "../../../styles/File.module.css";
import axios from "axios";
import react, { useEffect, useState } from "react";

const File = (props) => {

    const [isFavorite, setFavorite] = useState(props.isFavorite || false);

    useEffect(() => {
        // If isFavorite is explicitly passed as a prop, use it
        if (props.isFavorite !== undefined) {
            setFavorite(props.isFavorite);
        } else {
            // Otherwise, fetch from API
            fetchData();
        }
    }, [props.isFavorite])

    const fetchData = async() => {
        if (props.user_id === undefined) {
            console.warn("User ID is undefined. Cannot perform toggle.");
            return;
        }

        try {
            const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/users/favFiles/${props.user_id}`);
            const favouriteFilesArray = response.data.fav_files || response.data || [];

            const isFavorited = Array.isArray(favouriteFilesArray) && favouriteFilesArray.includes(props.id);
            setFavorite(isFavorited);
        } catch(error) {
            console.log("Error fetching favorite status: ", error);
            setFavorite(false);
        }
    }

    const handleToggle = async () => {
        if (props.user_id == undefined) return () => {}; 

        try {
            const formdata = new FormData();
            formdata.append(
                "json",
                JSON.stringify({
                    userId: props.user_id,
                })
            );

            // Store the current state before changing it
            const wasNotFavorite = isFavorite == false;
            
            // Update UI optimistically
            setFavorite(!isFavorite);

            // URL encode the file ID to handle special characters
            const encodedFileId = encodeURIComponent(props.id);

            // Make the server request based on the PREVIOUS state
            if (wasNotFavorite) {
                await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/users/favFiles/${encodedFileId}`, formdata);
                console.log(`Added file ${props.id} to favorites`);
            }
            else {
                await axios.delete(`${process.env.NEXT_PUBLIC_API_URL}/users/favFiles/${encodedFileId}`, {data: formdata});
                console.log(`Removed file ${props.id} from favorites`);
            }
            
            // Call the parent callback after server confirms
            if (props.onToggleFavorite) {
                // Small delay to ensure server has processed the request
                setTimeout(() => {
                    props.onToggleFavorite();
                }, 150);
            }
        } catch(error) {
            console.log("Error toggling favorite: ", error);
            // Revert the optimistic update on error
            setFavorite(!isFavorite);
        }
    }

    const showFavoriteIcon = () => {
        if (isFavorite === false) {
            return (
                <a onClick={() => handleToggle()}>
                    <svg 
                        width="24" 
                        height="24" 
                        viewBox="0 0 24 24" 
                        fill="none"
                        className={styles.heartIcon}
                        xmlns="http://www.w3.org/2000/svg">
                        <path 
                            d="M16.6875 3.1875C14.7188 3.1875 13.0069 4.07531 12 5.56313C10.9931 4.07531 9.28125 3.1875 7.3125 3.1875C5.82119 3.18924 4.39146 3.78243 3.33694 4.83694C2.28243 5.89146 1.68924 7.32119 1.6875 8.8125C1.6875 11.55 3.39375 14.3991 6.75937 17.2791C8.30161 18.5932 9.96751 19.7549 11.7338 20.7478C11.8156 20.7918 11.9071 20.8148 12 20.8148C12.0929 20.8148 12.1844 20.7918 12.2662 20.7478C14.0325 19.7549 15.6984 18.5932 17.2406 17.2791C20.6062 14.3991 22.3125 11.55 22.3125 8.8125C22.3108 7.32119 21.7176 5.89146 20.6631 4.83694C19.6085 3.78243 18.1788 3.18924 16.6875 3.1875ZM12 19.6041C10.4616 18.7163 2.8125 14.0363 2.8125 8.8125C2.81374 7.61941 3.28825 6.47553 4.13189 5.63189C4.97553 4.78825 6.11941 4.31374 7.3125 4.3125C9.21375 4.3125 10.8103 5.32781 11.4797 6.96281C11.5221 7.06598 11.5942 7.15422 11.6868 7.21632C11.7795 7.27842 11.8885 7.31158 12 7.31158C12.1115 7.31158 12.2205 7.27842 12.3132 7.21632C12.4058 7.15422 12.4779 7.06598 12.5203 6.96281C13.1897 5.32781 14.7862 4.3125 16.6875 4.3125C17.8806 4.31374 19.0245 4.78825 19.8681 5.63189C20.7118 6.47553 21.1863 7.61941 21.1875 8.8125C21.1875 14.0363 13.5384 18.7163 12 19.6041Z" 
                            fill="#D8D7FF"/>
                    </svg>
                </a>
            );
        }
        else {
            return (
                <a onClick={() => handleToggle()}>
                    <svg 
                        width="24" 
                        height="24" 
                        viewBox="0 0 24 24" 
                        fill="none" 
                        className={styles.heartIcon}
                        xmlns="http://www.w3.org/2000/svg">
                        <path 
                            d="M22.5 8.8125C22.5 15.375 12.7697 20.6869 12.3553 20.9062C12.2461 20.965 12.124 20.9958 12 20.9958C11.876 20.9958 11.7539 20.965 11.6447 20.9062C11.2303 20.6869 1.5 15.375 1.5 8.8125C1.50174 7.27146 2.11468 5.79404 3.20436 4.70436C4.29404 3.61468 5.77146 3.00174 7.3125 3C9.24844 3 10.9434 3.8325 12 5.23969C13.0566 3.8325 14.7516 3 16.6875 3C18.2285 3.00174 19.706 3.61468 20.7956 4.70436C21.8853 5.79404 22.4983 7.27146 22.5 8.8125Z" 
                            fill="#D8D7FF"
                        />
                    </svg>
                </a>
            );
         }
    }

    const showDownloadIcon = () => {
        if (props.action == "download") {
            return (
                <a href={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/open-school/download/${props.id}?extension=${props.extension.toLowerCase()}`} download>
                    <svg
                        width="30"
                        height="30"
                        viewBox="0 0 21 21"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M0.65625 12.9937C0.830298 12.9937 0.997218 13.0628 1.12029 13.1859C1.24336 13.3089 1.3125 13.4759 1.3125 13.6499V16.9312C1.3125 17.2792 1.45078 17.6131 1.69692 17.8592C1.94306 18.1054 2.2769 18.2437 2.625 18.2437H18.375C18.7231 18.2437 19.0569 18.1054 19.3031 17.8592C19.5492 17.6131 19.6875 17.2792 19.6875 16.9312V13.6499C19.6875 13.4759 19.7566 13.3089 19.8797 13.1859C20.0028 13.0628 20.1697 12.9937 20.3438 12.9937C20.5178 12.9937 20.6847 13.0628 20.8078 13.1859C20.9309 13.3089 21 13.4759 21 13.6499V16.9312C21 17.6273 20.7234 18.295 20.2312 18.7873C19.7389 19.2796 19.0712 19.5562 18.375 19.5562H2.625C1.92881 19.5562 1.26113 19.2796 0.768845 18.7873C0.276562 18.295 0 17.6273 0 16.9312V13.6499C0 13.4759 0.0691404 13.3089 0.192211 13.1859C0.315282 13.0628 0.482202 12.9937 0.65625 12.9937Z"
                            fill="#D8D7FF"
                            className="hoverPath"
                        />
                        <path
                            d="M10.0354 15.5584C10.0963 15.6195 10.1688 15.668 10.2485 15.7011C10.3282 15.7341 10.4137 15.7512 10.5 15.7512C10.5863 15.7512 10.6718 15.7341 10.7515 15.7011C10.8313 15.668 10.9037 15.6195 10.9646 15.5584L14.9021 11.6209C15.0254 11.4976 15.0946 11.3305 15.0946 11.1562C15.0946 10.982 15.0254 10.8149 14.9021 10.6916C14.7789 10.5684 14.6118 10.4992 14.4375 10.4992C14.2632 10.4992 14.0961 10.5684 13.9729 10.6916L11.1563 13.5096V1.96875C11.1563 1.7947 11.0871 1.62778 10.964 1.50471C10.841 1.38164 10.6741 1.3125 10.5 1.3125C10.326 1.3125 10.159 1.38164 10.036 1.50471C9.9129 1.62778 9.84376 1.7947 9.84376 1.96875V13.5096L7.02713 10.6916C6.9039 10.5684 6.73677 10.4992 6.56251 10.4992C6.38824 10.4992 6.22111 10.5684 6.09788 10.6916C5.97465 10.8149 5.90543 10.982 5.90543 11.1562C5.90543 11.3305 5.97465 11.4976 6.09788 11.6209L10.0354 15.5584Z"
                            fill="#D8D7FF"
                            className="hoverPath"
                        />
                    </svg>
                </a>
            );
        }
        else {
            return (
                <svg
                    width="30"
                    height="30"
                    viewBox="0 0 21 21"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        d="M19.6875 19.6875L1.3125 1.3125M1.3125 19.6875L19.6875 1.3125L1.3125 19.6875Z"
                        stroke="#D8D7FF"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="hoverPath"
                    />
                </svg>
            );
        }
    }

    return (
        <>
            <div className={styles.Container}>
                <div
                    className={
                        styles.ExtensionDiv + " " + styles[props.extension]
                    }
                >
                    <p>{props.extension}</p>
                </div>
                <div className={styles.InfoDiv + " " + props.id}>
                    <div className={styles.Info}>
                        <h5>
                            {props.name.length > 12
                                ? props.name.substring(0, 12) + "..."
                                : props.name}
                        </h5>
                        <h6>{props.size}</h6>
                    </div>
                    <div className={styles.Action}>
                        {showFavoriteIcon()}
                        {showDownloadIcon()}
                    </div>
                </div>
            </div>
        </>
    );
};
export default File;
