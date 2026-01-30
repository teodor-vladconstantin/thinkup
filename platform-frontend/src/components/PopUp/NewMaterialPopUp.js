import React, { useEffect, useState } from "react";
import styles from "../../../styles/NewMaterialPopUp.module.css";
import CancelButton from "../Buttons/CancelButton";
import AccentButton from "../Buttons/AccentButton";
import PopUpContainer from "../Containers/PopUpContainer";
import FileUploadInput from "../FormElems/FileUploadInput";
import CircleLogo from "../Circle/CircleLogo";
import { createUniqueId, getCurentDate } from "../../utils/utils";
import TextArea from "../FormElems/TextArea";
import { useMyUserContext, useMyUserUpdate } from "../../contexts/UserContext";
import TitleInputField from "../FormElems/TitleInputField";
import axios from "axios";
import File from "../Cards/File";
import ScrollContainer from "../Containers/ScrollContainer";

const NewMaterialPopUp = ({ className, close, addedmaterial, Projectid }) => {
    const [Title, setTitle] = useState("");
    const [Description, setDescription] = useState("");
    const [Date, setDate] = useState("");
    const [Files, setFiles] = useState();
    const user = useMyUserContext();

    useEffect(() => {
        setDate(getCurentDate());
    }, []);

    const createMaterial = async () => {
        const id = createUniqueId();
        let file_id_array = new Array();
        for(let i=0;i<Files.length;i++){
            file_id_array.push(createUniqueId());
        }
        console.log(file_id_array);
        const formdata = new FormData();
        //formdata.append('json',{id:id,name:Title,creationDate:Date,description:Description,createdBy:user.id,projectId:Projectid,files:fileid});
        formdata.append(
            "json",
            JSON.stringify({
                id: id,
                name: Title,
                creationDate: Date,
                description: Description,
                createdBy: user.id,
                projectId: Projectid,
                files: file_id_array,
            })
        );
        const [f] = Files
        console.log(f);

        //formdata.append('json',`{id:${id},name:${Title},creationDate:${Date},description:${Description},createdBy:${user.id},projectId:${Projectid},files:${fileid}}`);
        formdata.append("files", f);

        //const response = await axios.post(`http://127.0.0.1:5000/materials/${id}`,{id:id,name:Title,creationDate:Date,description:Description,createdBy:user.id,projectId:Projectid,files:{}});
        const response = await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL}/materials/${id}`,
            formdata
        );
        if (response.status == 200) {
            addedmaterial();
        } else {
            console.log("ERROR");
        }
        close();
    };

    const handleFileChange = (e) => {
        const f = Array.from(e.target.files);
        console.log(Array.from(e.target.files));
        console.log(f.length);

        setFiles(f);
    };

    return (
        <PopUpContainer className={styles.NewMaterialPopUp + " " + className}>
            <ScrollContainer className={styles.ScrollContainer}>
                    <div className={styles.NewMaterialPopUpTopBar}>
                        <CircleLogo
                            image="/ic_material.svg"
                            className={styles.NewMaterialCircleLogo}
                        />
                        <div>
                            <TitleInputField
                                placeholder="Set title"
                                value={Title}
                                onChange={(e) => setTitle(e.target.value)}
                            />
                            <p className={styles.NewMaterialDate}>{Date}</p>
                        </div>
                    </div>
                    <TextArea
                        className={styles.NewMaterialDescription}
                        areaTitle="Description"
                        placeholder="Write your description here..."
                        subheader="false"
                        value={Description}
                        onChange={(e) => setDescription(e.target.value)}
                        width="675"
                    />
                    <FileUploadInput
                        FileUploadTitle="Upload Files"
                        fileChange={(e) => handleFileChange(e)}
                    />

                    
                    <div className={styles.FilesContainer}>
                        {Files?.map((file,index)=>{
                            return(
                                <File name={file.name} extension="JPG" size="36KB" action="download" key={index}/>
                                //<p>{file.name}</p>
                            )
                        })}
                    </div>

                    <div className={styles.NewMaterialButtonDiv}>
                        <AccentButton text="Create" onClick={() => createMaterial()}>
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
                        <CancelButton text="Cancel" onClick={() => close()} />
                    </div>
            </ScrollContainer>
        </PopUpContainer>
    );
};
export default NewMaterialPopUp;
