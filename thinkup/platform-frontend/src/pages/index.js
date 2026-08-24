import react from "react";
import Head from "next/head";
import Image from "next/image";
import { useEffect, useState } from "react";
import styles from "../../styles/Home.module.css";
import ProjectCard from "../components/Cards/ProjectCard";
import ProjectsTable from "../components/Tables/ProjectsTable";
import axios from "axios";
import { useUser } from "@auth0/nextjs-auth0";
import { useRouter } from "next/router";
import { useMyUserContext, useMyUserUpdate } from "../contexts/UserContext";
import SearchBar from "../components/FormElems/SearchBar";
import FilterComponent from "../components/FormElems/FilterComponent.js";
import Loading from "../components/Loading/Loading";
import { useAccesTokenContext } from "../contexts/AccesTokenContext";
import UsersTable from "../components/Tables/UsersTable";

const Home = () => {
    const router = useRouter();
    const [UsersData, setUsersData] = useState();
    const [ProjectsData, setProjectsData] = useState();
    const [SearchValue, setSearchValue] = useState("");
    const [SearchType, setSearchType] = useState(true);
    const [FilterValue, setFilterValue] = useState("Filter");
    const [Language, setLanguage] = useState("en");
    const User = useMyUserContext();
    const AccesToken = useAccesTokenContext();
    const AreaOfImplementationOptions = new Array(
        "Civic Education",
        "Ecological",
        "STEM"
    );

    const messages = {
        en: {
            search_projects_text: "Search projects",
            search_users_text: "Search users",

        },
        ro: {
            search_projects_text: "Caută proiecte",
            search_users_text: "Caută utilizatori",
        },
    };

    const getAllProjects = async () => {
        let response;
        if (FilterValue == "Filter")
            response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/projects`);
        else
            response = await axios.get(
                `${process.env.NEXT_PUBLIC_API_URL}/projects?filter=${FilterValue}`
            );
        console.log(response.data.projects);
        setProjectsData(response.data.projects);
    };

    const searchForProjects = async () => {
        if (SearchValue == "") {
            getAllProjects();
            return;
        }
        const response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/projects/search/${SearchValue}`
        );
        setProjectsData(response.data.projects);
    };

    const getAllUsers = async () => {
        let response;
        response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/users`
        );
        setUsersData(response.data.users.Items);
    };

    const searchForUsers = async () => {
        /*if (SearchValue == "") {
            getAllUsers();
            return;
        }*/
        const response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/users?username=${SearchValue}`
        );
        setUsersData(response.data.users.Items);
        console.log(response);
    };

    

    const StartSearch = () =>{
        if(SearchType)
            searchForProjects();
        else
            searchForUsers();
    }

    useEffect(()=>{
        if(SearchType)
            getAllProjects();
        else
            getAllUsers();
    },[SearchType])

    useEffect(() => {
        getAllProjects();
    }, [FilterValue]);

    useEffect(() => {
        if (User != undefined && User.settings != undefined)
            setLanguage(User.settings.language);
    }, [User]);

    /*useEffect(() => {
        console.log(AccesToken);
    }, [AccesToken]);*/

    return (
        <div className={styles.Home}>
            <Head>
                <title>ThinkUp Academy</title>
                <meta name="description" content="Platfoma ThinkUp" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <div className={styles.HomeTopBar}>
                <FilterComponent
                    value={FilterValue}
                    setValue={(e) => setFilterValue(e)}
                    options={AreaOfImplementationOptions}
                />
                <SearchBar
                    search_type={SearchType?"projects":"users"}
                    changeSearchType={()=>setSearchType(!SearchType)}
                    search_value={SearchValue}
                    Placeholder={(()=>{
                        if(SearchType)
                            if(Language == "ro")
                                return messages.ro.search_projects_text;
                            else
                                return messages.en.search_projects_text;
                        else
                            if(Language == "ro")
                                return messages.ro.search_users_text;
                            else
                                return messages.en.search_users_text;
                    })()}
                    changeValue={(e) => setSearchValue(e.target.value)}
                    onsearch={() => StartSearch()}
                />
            </div>
            {SearchType?
            <ProjectsTable data={ProjectsData} />
            :
            <UsersTable data={UsersData}/>
            }
        </div>
    );
};

export default Home;
