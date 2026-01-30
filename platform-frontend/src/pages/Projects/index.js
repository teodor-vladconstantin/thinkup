import react, { useState, useEffect } from "react";
import styles from "../../../styles/Projects.module.css";
import user_styles from "../../../styles/MyProfile.module.css";
import ProjectsTable from "../../components/Tables/ProjectsTable";
import { useMyUserContext, useMyUserUpdate } from "../../contexts/UserContext";
import ScrollContainer from "../../components/Containers/ScrollContainer";
import axios from 'axios';

const Projects = () => {
    const User = useMyUserContext();

    const [Data, setData] = useState();


    const getUserProjects = async () =>{
        if(User==undefined || User.id==undefined) return new Array();
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/user_projects/${User.id}`);
        console.log(response);
        return response.data.projects;
    }

    useEffect(async() => {
        /*const DataArray = new Array({
            addcard: true,
        });*/
        const DataArray = await getUserProjects();
        DataArray.unshift({addcard: true,});
        setData(DataArray);
    }, []);

    if (User == undefined)
    return (
        <ScrollContainer className={user_styles.noUser}>
            <h1>No user logged in.</h1>
            <p>Please register or log in to see your projects.</p>
        </ScrollContainer>
    );

    return (
        <div className={styles.ProjectsContainer}>
            <ProjectsTable data={Data} />
        </div>
    );
};

export default Projects;
