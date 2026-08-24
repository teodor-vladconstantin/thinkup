import React, {useState} from "react";
import styles from "../../../styles/FeedbackCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import axios from "axios";

// Remove the state declaration and setOpenedFeedback usage
const FeedbackCard = ({ className, children, date, onClick, userId, feedbackCreatorId, projectID, feedbackID, refresh, setEditFeedback }) => {
    const deleteFeedback = async (e) => {
        e.stopPropagation(); // Stop event propagation here
        const response = await axios.delete(`${process.env.NEXT_PUBLIC_API_URL}/projects/${projectID}/feedback/${feedbackID}`);
        console.log(response);
        refresh();
    };

    return (
        <DefaultContainer className={styles.FeedbackCard + " " + className} onClick={() => onClick()}>
            <p className={styles.FeedbackCardText}>{children}</p>
            <p className={styles.FeedbackCardDate}>{date}</p>
            {userId === feedbackCreatorId && 
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" className={styles.FeedbackCardDelete} onClick={(e) => deleteFeedback(e)}>
                        <path fill="currentColor" d="M9 3v1H4v2h1v13a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V6h1V4h-5V3zM7 6h10v13H7zm2 2v9h2V8zm4 0v9h2V8z"/>
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256" className={styles.FeedbackCardDot}>
                        <path fill="currentColor" d="M144 128a16 16 0 1 1-16-16a16 16 0 0 1 16 16"/>
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" className={styles.FeedbackCardEdit} onClick={(e) => { e.stopPropagation(); setEditFeedback(feedbackID); }}>
                        <path fill="currentColor" d="M5 18.08V19h.92l9.06-9.06l-.92-.92z" opacity="0.3"/>
                        <path fill="currentColor" d="M20.71 7.04a.996.996 0 0 0 0-1.41l-2.34-2.34c-.2-.2-.45-.29-.71-.29s-.51.1-.7.29l-1.83 1.83l3.75 3.75zM3 17.25V21h3.75L17.81 9.94l-3.75-3.75zM5.92 19H5v-.92l9.06-9.06l.92.92z"/>
                    </svg>
                </div>
            }
        </DefaultContainer>
    );
};


export default FeedbackCard;
