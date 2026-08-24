import React, { useState, useEffect } from "react";
import styles from "../../../styles/ActivityCard.module.css";
import DefaultContainer from "../Containers/DefaultContainer";
import FilterComponent from "../../components/FormElems/FilterComponent.js";
import axios from "axios";

const ActivityCard = (props) => {
    const [FilterValue, setFilterValue] = useState("Select");
    const options = new Array("Civic Education", "Ecological", "STEM");
    const [Data, setData] = useState();
    const today  = new Date();
    const year = today.getFullYear();
    const currentMonth = today.getMonth(); // 0-indexed, January is 0
    const currentDayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);

    const getActivityCurrent = async () => {
        const response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/users/useractivity/currentyear/${props.user_id}`
        );
        console.log("activity", response.data);
        setData(response.data);
    };
    useEffect(() => {
        getActivityCurrent();
    }, []);

    useEffect(() => {
        setActivity();
    }, [Data]);

    function setActivity() {
        if (Data === undefined) return;

        let k = 1;
        for(let i = 1; i <= 12; i++){
            let month = '0';
            if(i >= 10)
                month = i.toString();
            else
                month = month + i.toString();

            let month_length = 30;
            if(i % 2 === 1)
                month_length = 31;
            if(i === 2)
                month_length = 28;

            for(let j = 1; j <= month_length; j++){
                let day = '0';
                if(j >= 10)
                    day = j.toString();
                else
                    day = day + j.toString();

                let date = year + '-' + month + '-' + day;

                const str = ".activity-day-" + k;
                const el = document.querySelector(str);
                const hover_date = document.createElement('p');
                hover_date.classList.add(styles.HoverDate);
                hover_date.innerHTML = date;
                el.appendChild(hover_date);

                if(Data[date] !== undefined){
                    el.style.backgroundColor = "var(--color-accent-primary)";
                }

                k++;   
            }
        }
        console.log(k);
    }

    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const recentMonths = [...months.slice(currentMonth), ...months.slice(0, currentMonth)];

    const daysInYear = Array.from(Array(365).keys());
    const recentDays = [...daysInYear.slice(currentDayOfYear), ...daysInYear.slice(0, currentDayOfYear)];

    return (
        <DefaultContainer
            className={styles.ActivityCard + " " + props.className}
            onClick={() => {}}
        >
            <div className={styles.flexDiv}>
                <p className={styles.Title}>Activity</p>
            </div>

            <div className={styles.flexStart}>
                {recentMonths.map((month, index) => (
                    <p key={index}>{month}</p>
                ))}
                <p style={{ opacity: "0" }}>J</p>
            </div>
            
            <div className={styles.GridContainer + " " + "grid-container"}>
                {
                    recentDays.map((index) => {
                        const dayOfYear = index + 1;
                        return <div className={styles.ActivitySquare + ` activity-day-${dayOfYear}`} key={index} />
                    })
                }
            </div>
        </DefaultContainer>
    );
};
export default ActivityCard;
