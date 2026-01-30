import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import styles from "../../../styles/ReviewsPopUp.module.css";
import PopUpContainer from "../Containers/PopUpContainer";
import ScrollContainer from "../Containers/ScrollContainer";
import AccentButton from "../Buttons/AccentButton";
import CancelButton from "../Buttons/CancelButton";
import axios from "axios";

const ReviewsPopUp = ({ className, close , reviews, language}) => {
    const [Reviews,setReviews] = useState(undefined);
    const [Users,setUsers] = useState(undefined);

    const router = useRouter();

    const messages ={
        "en":{
            reviews_title:"All Reviews",
            reviews_description:"If you don&apos;t think a review is appropiate, please ",
            contact_text:"contact us"
        },
        "ro":{
            reviews_title:"Toate Recenziile",
            reviews_description:"Daca considerati ca o recenzie nu este adecvata, va rugam ",
            contact_text:"contacteaza-ne"
        }
    }

    const RouteTo = (new_route) => {
        console.log(router.pathname);
        router.push(new_route);
    };

    const getReviews = async () =>{
        Promise.all(
            reviews?.map(async (review) => {
                const responseR = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/reviews/${review}`
                )
                return responseR.data;

            })
        ).then((response) => {
            console.log(response);
            setReviews(response);
        });
    }
    

    const getUsers = async () =>{
        console.log(Reviews);

        Promise.all(
            Reviews?.map(async (review) => {
                const responseU = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/users/${review.userID}`
                );
                return responseU.data;

            })
        ).then((response) => {
            console.log(response);
            setUsers(response);
        });
    }

    useEffect(()=>{
        console.log(reviews);
        getReviews(reviews)
    },[])

    useEffect(()=>{
        if(Reviews!=undefined)
            getUsers();
    },[Reviews])

    return (
        <PopUpContainer className={styles.ReviewsPopUp + " " + className}>
            <h2>{language=="ro"?messages.ro.reviews_title:messages.en.reviews_title}</h2>
            <p>{language=="ro"?messages.ro.reviews_description:messages.en.reviews_description}<a onClick={() => RouteTo("/Contact")}><span>{language=="ro"?messages.ro.contact_text:messages.en.contact_text}</span></a>.</p>
            <ScrollContainer className={styles.ScrollContainer}>
                <div className={styles.ReviewsTable}>
                    {Users!=undefined?Reviews?.map((review,index)=>{
                        console.log(review);
                        return (
                            <div className={styles.ReviewContainer} key={index}>
                                <div className={styles.FlexRow}>
                                    <img className={styles.ReviewUserImage} src={`${process.env.NEXT_PUBLIC_API_URL}/storage/thinkup-profile-picture/${Users[index].profile_picture}${Users[index].profile_picture_extension}`}></img>
                                    <div>
                                        <p>{Users[index].name}</p>
                                        <div className={styles.ReviewsStarsContainer}>
                                            <img
                                                src={review.review_rating>=1?"/bi_star-fill.svg":"/bi_star.svg"}
                                                className={styles.Star}
                                            />
                                            <img
                                                src={review.review_rating>=2?"/bi_star-fill.svg":"/bi_star.svg"}
                                                className={styles.Star}
                                            />
                                            <img
                                                src={review.review_rating>=3?"/bi_star-fill.svg":"/bi_star.svg"}
                                                className={styles.Star}
                                            />
                                            <img
                                                src={review.review_rating>=4?"/bi_star-fill.svg":"/bi_star.svg"}
                                                className={styles.Star}
                                            />
                                            <img
                                                src={review.review_rating>=5?"/bi_star-fill.svg":"/bi_star.svg"}
                                                className={styles.Star}
                                            />
                                        </div>
                                    </div>
                                </div>
                                <p>{review.review_description}</p>
                            </div>
                        )
                    }):<></>}
                </div>
            </ScrollContainer>
            <div className={styles.endFlexRow}>
                <CancelButton text="Close" onClick={() => close()} />
            </div>
        </PopUpContainer>
    );
};
export default ReviewsPopUp;
