import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import styles from "../../../../styles/Project.module.css";
import DescriptionCard from "../../../components/Cards/DescriptionCard";
import CategoryCard from "../../../components/Cards/CategoryCard";
import axios from "axios";
import MaterialsTable from "../../../components/Tables/MaterialsTable";
import ScrollContainer from "../../../components/Containers/ScrollContainer";
import { useMyUserContext } from "../../../contexts/UserContext";
import GoalsTable from "../../../components/Tables/GoalsTable";
import Loading from "../../../components/Loading/Loading";
import SimpleButton from "../../../components/Buttons/SimpleButton";
import AddReviewPopUp from "../../../components/PopUp/AddReviewPopUp";
import { AnimatePresence } from "framer-motion";
import ReviewsPopUp from "../../../components/PopUp/ReviewsPopUp";
import FeedbackTable from "../../../components/Tables/FeedbackTable";
import { set } from "date-fns";

const Project = () => {
    const [ProjectData, setProjectData] = useState(undefined);
    const [userAdminData, setUserAdminData] = useState(undefined);
    const [Materials, setMaterials] = useState(undefined);
    const [Feedback, setFeedback] = useState([]);
    const [Goals, setGoals] = useState(undefined);
    const [AdminState, setAdminState] = useState(false);
    const [NewReviewPopUp, setNewReviewPopUp] = useState(false);
    const [ReviewPopUp, setReviewPopUp] = useState(false);
    const [Language, setLanguage] = useState("en");
    const router = useRouter();
    const User = useMyUserContext();
    const { id } = router.query;

    const messages = {
        en: {
            create_text: "Created by:",
            rating_text: "Average rating:",
            add_review_text: "Add review",
            number_reviews_text: "reviews",
        },
        ro: {
            create_text: "Creat de:",
            rating_text: "Recenzie medie:",
            add_review_text: "Adauga recenzie",
            number_reviews_text: "recenzii",
        },
    };

    const getProjectData = async () => {
        try {
            const response = await axios.get(
                `${process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "")}/projects/${id}`
            );
            setProjectData(response.data);
        } catch (error) {
            console.error("Error fetching project data:", error);
        }
    };

    const getUserData = async (userID) => {
        try {
            const response = await axios.get(
                `${process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "")}/users/${userID}`
            );
            setUserAdminData(response.data);
        } catch (error) {
            console.error("Error fetching user data:", error);
        }
    };

    const getFeedback = async () => {
        try {
            const feedbackData = await Promise.all(
                ProjectData.mentor_feedback.map(async (feedbackid) => {
                    const responseM = await axios.get(
                        `${process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "")}/projects/${id}/feedback/${feedbackid}`
                    );

                    if (!responseM.data.ErrorMessage) {
                        return responseM.data;
                    } else {
                        return null;
                    }
                })
            );

            setFeedback(feedbackData.filter((feedback) => feedback != null));
        } catch (error) {
            console.error("Error fetching feedback:", error);
        }
    };

    const getMaterials = async () => {
        try {
            const materialsData = await Promise.all(
                ProjectData.materials.map(async (materialid) => {
                    const responseM = await axios.get(
                        `${process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "")}/materials/${materialid}`
                    );
                    return responseM.data;
                })
            );
            setMaterials(materialsData);
        } catch (error) {
            console.error("Error fetching materials:", error);
        }
    };

    const getGoals = async () => {
        try {
            const goalsData = await Promise.all(
                ProjectData.goals.map(async (goalid) => {
                    const responseM = await axios.get(
                        `${process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "")}/goals/${goalid}`
                    );
                    return responseM.data;
                })
            );
            setGoals(goalsData);
        } catch (error) {
            console.error("Error fetching goals:", error);
        }
    };

    useEffect(() => {
        if (id) {
            getProjectData();
        }
    }, [id]);

    useEffect(() => {
        if (ProjectData) {
            getUserData(ProjectData.createdBy);

            if (User && ProjectData.createdBy === User.id) {
                setAdminState(true);
            }

            if (ProjectData.materials) {
                getMaterials();
            }

            if (ProjectData.goals) {
                getGoals();
            }

            if (ProjectData.mentor_feedback) {
                getFeedback();
            }
        }
    }, [ProjectData, User]);

    useEffect(() => {
        if (User && User.settings) {
            setLanguage(User.settings.language);
        }
    }, [User]);

    if (!ProjectData || !id || !Materials || !userAdminData) {
        return <Loading />;
    }

    return (
        <ScrollContainer className={styles.Project} onClick={() => {}}>
            <div className={styles.TopProjectSection}>
                <div className={styles.TopProjectTextSection}>
                    <div className={styles.ProjectTitleDiv}>
                        <h1 className={styles.ProjectTitle}>
                            {ProjectData.name}
                        </h1>
                        <div className={styles.EditBtnDiv}>
                            {AdminState ? (
                                <img
                                    src="../icon_edit.svg"
                                    onClick={() =>
                                        router.push(
                                            `/Projects/${id}/EditProject`
                                        )
                                    }
                                />
                            ) : (
                                <></>
                            )}
                            {AdminState ? (
                                <img
                                    src="../icon_settings.svg"
                                    onClick={() =>
                                        router.push(`/Projects/${id}/Settings`)
                                    }
                                />
                            ) : (
                                <></>
                            )}
                        </div>
                    </div>
                    <p className={styles.ProjectDate}>
                        {ProjectData.creationDate}
                    </p>
                    <CategoryCard category={ProjectData.areaOfImplementation}>
                        {ProjectData.areaOfImplementation}
                    </CategoryCard>
                    <p className={styles.ProjectContributors}>
                       {Language=="en"?messages.en.create_text:messages.ro.create_text}{" "}
                        <span
                            onClick={() =>
                                router.push(`/Profile/${ProjectData.createdBy}`)
                            }
                        >
                            {userAdminData.name}
                        </span>
                    </p>
                    {ProjectData.settings.accept_reviews ? (
                        <div>
                            <div className={styles.ProjectReviewContainer}>
                                <p className={styles.ProjectReviewText}>
                                {Language=="en"?messages.en.rating_text:messages.ro.rating_text} <span>{ProjectData.projectReviews.average_rating}</span>
                                </p>
                                <div className={styles.StarsContainer}>
                                    <img
                                        src={ProjectData.projectReviews.average_rating>=1?"/bi_star-fill.svg":"/bi_star.svg"}
                                        className={styles.Star}
                                    />
                                    <img
                                        src={ProjectData.projectReviews.average_rating>=2?"/bi_star-fill.svg":"/bi_star.svg"}
                                        className={styles.Star}
                                    />
                                    <img
                                        src={ProjectData.projectReviews.average_rating>=3?"/bi_star-fill.svg":"/bi_star.svg"}
                                        className={styles.Star}
                                    />
                                    <img
                                        src={ProjectData.projectReviews.average_rating>=4?"/bi_star-fill.svg":"/bi_star.svg"}
                                        className={styles.Star}
                                    />
                                    <img
                                        src={ProjectData.projectReviews.average_rating>=5?"/bi_star-fill.svg":"/bi_star.svg"}
                                        className={styles.Star}
                                    />
                                </div>
                                <p className={styles.ProjectSeeReviewsText} onClick={()=>setReviewPopUp(true)}>
                                    {ProjectData.projectReviews.total_reviews}  {Language=="en"?messages.en.number_reviews_text:messages.ro.number_reviews_text}
                                </p>
                            </div>
                            <SimpleButton onClick={() => setNewReviewPopUp(true)}>
                                {Language=="en"?messages.en.add_review_text:messages.ro.add_review_text}
                            </SimpleButton>
                        </div>
                    ) : (
                        <></>
                    )}
                </div>

                <img
                    src={`${process.env.NEXT_PUBLIC_API_URL || ''}/thumbnails/${ProjectData.thumbnail}`}
                    className={styles.ProjectImage}
                />
            </div>
            <DescriptionCard className={styles.ProjectDescription} language={Language}>
                {ProjectData.description}
            </DescriptionCard>

            <FeedbackTable data={Feedback} projectID={id} refresh={()=>getProjectData()} AdminState={AdminState} userId={User?.id} language={Language}/>

            {AdminState?
            <GoalsTable
                className={styles.GoalsTable}
                data={Goals}
                ProjectId={id}
                AdminState={AdminState}
                language={Language}
                refresh={()=>getProjectData()}
                getProjectData={() => getProjectData()}
            />:<></>}

            {AdminState?
            <MaterialsTable
                className={styles.MaterialsTable}
                data={Materials}
                Projectid={id}
                AdminState={AdminState}
                language={Language}
                getProjectData={() => getProjectData()}
            />:<></>}

            <AnimatePresence exitBeforeEnter={true}>
                {NewReviewPopUp && (
                    <AddReviewPopUp close={() => setNewReviewPopUp(false)} projectID={id} refresh={()=>getProjectData()}/>
                )}
                {ReviewPopUp &&(
                    <ReviewsPopUp close={()=>setReviewPopUp(false)} reviews={ProjectData.projectReviews.reviews} language={Language}/>
                )}
            </AnimatePresence>
        </ScrollContainer>
    );
};

export default Project;
