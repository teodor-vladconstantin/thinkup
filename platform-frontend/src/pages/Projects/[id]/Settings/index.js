import React,{useState,useEffect} from "react";
import { useRouter } from "next/router";
import styles from "../../../../../styles/SettingsProject.module.css";
import DeleteButton from "../../../../components/Buttons/DeleteButton";
import AccentButton from "../../../../components/Buttons/AccentButton";
import CancelButton from "../../../../components/Buttons/CancelButton";
import Toggle from "../../../../components/FormElems/Toggle";
import axios from "axios";
import AdminListTable from "../../../../components/Tables/AdminListTable";
import Loading from "../../../../components/Loading/Loading";
import ScrollContainer from "../../../../components/Containers/ScrollContainer";
import AddAdminPopUp from "../../../../components/PopUp/AddAdminPopUp";
import { AnimatePresence } from "framer-motion";

const SettingsProject = () =>{
    const [ProjectData, setProjectData] = useState(undefined);
    const [AllowReviews,setAllowReviews]= useState(true);
    const [NewAdminPopUp,setNewAdminPopUp]= useState(false);
    const router = useRouter();
    const { id } = router.query;



    const getProjectData = async () => {
        const response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/projects/${id}`
        );
        console.log(response.data);
        setProjectData(response.data);
        if(response.data.settings.accept_reviews)
            setAllowReviews(true);
        else
            setAllowReviews(false);
    };

    useEffect(() => {
        getProjectData();
    }, [id]);




    const DeleteProject = async ()=>{
        const response = await axios.delete(`${process.env.NEXT_PUBLIC_API_URL}/projects/${id}`);
        if(response.status==200){
            router.push('/');
        }
        else{
            console.log("ERROR");
        }
    }

    const saveChanges = async ()=>{
        const response = await axios.put(`${process.env.NEXT_PUBLIC_API_URL}/projects/${id}/accept_reviews/${AllowReviews?1:0}`);
        if(response.status==200){
            router.back();
        }
        else{
            console.log("ERROR");
        }

    }

    if(ProjectData == undefined) return <Loading></Loading>

    return (
        <ScrollContainer>
            <div className={styles.Settings}>
                <h1 className={styles.SettingsTitle}>Settings Project</h1>
                <div className={styles.ReviewsContainer}>
                    <p>Allow reviews: {AllowReviews?"yes":"no"}</p>
                    <Toggle value={AllowReviews} change={()=>setAllowReviews(!AllowReviews)}></Toggle>
                </div>
                <AdminListTable adminlist={ProjectData.adminList} openPopUp={()=>setNewAdminPopUp(true)} project_id={id} refresh={()=>getProjectData()}/>


                <DeleteButton text="Delete Project" onClick={()=>DeleteProject()}/>

                <div className={styles.SettingsButtonDiv}>
                        <AccentButton text="Save Changes" onClick={() => saveChanges()}>
                            <svg
                                width="21"
                                height="22"
                                viewBox="0 0 21 22"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fillRule="evenodd"
                                    clipRule="evenodd"
                                    d="M1.3125 10.9999C1.3125 10.8259 1.38164 10.6589 1.50471 10.5359C1.62778 10.4128 1.7947 10.3437 1.96875 10.3437H17.4471L13.3166 6.21453C13.1934 6.0913 13.1242 5.92417 13.1242 5.7499C13.1242 5.57564 13.1934 5.40851 13.3166 5.28528C13.4399 5.16205 13.607 5.09283 13.7812 5.09283C13.9555 5.09283 14.1226 5.16205 14.2459 5.28528L19.4959 10.5353C19.557 10.5962 19.6055 10.6687 19.6386 10.7484C19.6716 10.8281 19.6887 10.9136 19.6887 10.9999C19.6887 11.0862 19.6716 11.1717 19.6386 11.2514C19.6055 11.3312 19.557 11.4036 19.4959 11.4645L14.2459 16.7145C14.1226 16.8378 13.9555 16.907 13.7812 16.907C13.607 16.907 13.4399 16.8378 13.3166 16.7145C13.1934 16.5913 13.1242 16.4242 13.1242 16.2499C13.1242 16.0756 13.1934 15.9085 13.3166 15.7853L17.4471 11.6562H1.96875C1.7947 11.6562 1.62778 11.587 1.50471 11.4639C1.38164 11.3409 1.3125 11.174 1.3125 10.9999Z"
                                    fill="#888888"
                                />
                            </svg>
                        </AccentButton>
                        <CancelButton text="Cancel" onClick={()=>router.back()}/>
                </div>
                <AnimatePresence exitBeforeEnter={true}>
                {NewAdminPopUp && (
                    <AddAdminPopUp close={()=>setNewAdminPopUp(false)} id={id} refresh={()=>getProjectData()}></AddAdminPopUp>
                )}
                </AnimatePresence>

            </div>
        </ScrollContainer>
    )
}

export default SettingsProject;