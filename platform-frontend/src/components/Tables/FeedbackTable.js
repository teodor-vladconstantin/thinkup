import React, { useEffect, useState } from "react";
import styles from "../../../styles/FeedbackTable.module.css";
import FeedbackCard from "../Cards/FeedbackCard";
import { AnimatePresence } from "framer-motion";
import FeedbackPopUp from "../PopUp/FeedbackPopUp";
import CircleAddButton from "../Buttons/CircleAddButton";
import NewFeedbackPopUp from "../PopUp/NewFeedbackPopUp";
import EditFeedbackPopUp from "../PopUp/EditFeedbackPopUp";


const FeedbackTable = (props) => {

    const [ShownFeedbackCards,setShownFeedbackCards] = useState(3);
    const [OpenedFeedback,setOpenedFeedback] = useState(null);
    const [NewFeedbackPopUpState,setNewFeedbackPopUpState] = useState(false);
    const [editingFeedbackID, setEditingFeedbackID] = useState(null);

    const messages ={
        "en":{
            no_feedback_text:"There is no feedback for this project.",
        },
        "ro":{
            no_feedback_text:"Nu exista feedback pentru acest proiect.",
        }
    }

    const handleViewMore = () => {
        setShownFeedbackCards(shownFeedbackCards + 3);
      };
    
      const handleViewLess = () => {
        setShownFeedbackCards(3);
      };

    if(props.data ==undefined)
        return (<></>);
    return (
        <div className={styles.FeedbackTable}>
            <div className={styles.FeedbackTopBar}>
                <div className={styles.FeedbackHeader}>
                    <p className={styles.FeedbackTitle}>Feedback</p>
                    { ShownFeedbackCards > 3 && <p className={styles.FeedbackMore} onClick={() => {setShownFeedbackCards(ShownFeedbackCards - 3)}}>View less</p>}
                    {props.data.length > ShownFeedbackCards && <p className={styles.FeedbackMore} onClick={() => { setShownFeedbackCards(ShownFeedbackCards + 3)}}>
                        View more
                    </p>}

                </div>
                {!props.AdminState && <CircleAddButton className={styles.AddFeedbackButton} onClick={()=>setNewFeedbackPopUpState(true)}/>}
            </div>
            <div className={styles.FeedbackGrid}>
                {props.data.length !== 0 ? 
                    [].concat(
                        // Feedback created by the current user
                        props.data.filter(feedback => feedback.mentor_id === props.userId),
                        // Feedback created by others
                        props.data.filter(feedback => feedback.mentor_id !== props.userId)
                    )
                    .slice(0, ShownFeedbackCards)
                    .map((feedbackData, index) => {
                        return (
                            <FeedbackCard 
                                key={index} 
                                date={feedbackData.date} 
                                onClick={() => setOpenedFeedback(index)} 
                                userId={props.userId} 
                                feedbackCreatorId={feedbackData.mentor_id} 
                                projectID={props.projectID} 
                                feedbackID={feedbackData.id} 
                                refresh={props.refresh}
                                setEditFeedback={setEditingFeedbackID}
                            >
                                {feedbackData.feedback_txt}
                            </FeedbackCard>
                        );
                    }) 
                    : 
                    <div className={styles.NoFeedbackText}>
                        {props.language === "ro" ? messages.ro.no_feedback_text : messages.en.no_feedback_text}
                    </div>
                }
            </div>

            <AnimatePresence exitBeforeEnter={true}>
            {editingFeedbackID != null &&
                <EditFeedbackPopUp 
                    text={props.data.find(feedback => feedback.id === editingFeedbackID).feedback_txt} 
                    close={() => setEditingFeedbackID(null)} 
                    mentor_id={props.data.find(feedback => feedback.id === editingFeedbackID).mentor_id}
                    feedbackID={editingFeedbackID}
                    projectID={props.projectID}
                    refresh={props.refresh}
                />
            }
                {OpenedFeedback!=null&&<FeedbackPopUp text={props.data[OpenedFeedback].feedback_txt} date={props.data[OpenedFeedback].date} close={()=>setOpenedFeedback(null)} mentor_id={props.data[OpenedFeedback].mentor_id}/>}    
                {NewFeedbackPopUpState&&<NewFeedbackPopUp close={()=>setNewFeedbackPopUpState(false)} projectID={props.projectID} refresh={props.refresh}/>}
            </AnimatePresence>
        </div>
    );
};

export default FeedbackTable;
