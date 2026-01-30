import React, { useState } from "react";
import Head from "next/head";
import styles from "../../../styles/NewProject.module.css";
import InputField from "../../components/FormElems/InputField";
import SelectField from "../../components/FormElems/SelectField";
import TextArea from "../../components/FormElems/TextArea";
import AccentButton from "../../components/Buttons/AccentButton";
import CancelButton from "../../components/Buttons/CancelButton";
import { useRouter } from "next/router";
import { useMyUserContext, useMyUserUpdate } from "../../contexts/UserContext";
import { getCurentDate, createUniqueId, verifyText } from "../../utils/utils";
import axios from "axios";
import ScrollContainer from "../../components/Containers/ScrollContainer";

const NewProject = () => {
    const [ProjectName, setProjectName] = useState("");
    const [token, setToken] = useState("");
    const [Description, setDescription] = useState("");
    const [AreaOfImplementation, setAreaOfImplementation] = useState("Select");
    const [value, setFilterValue] = useState("Select");
    const router = useRouter();
    const user = useMyUserContext();

    const AreaOfImplementationOptions = new Array(
        "Civic Education",
        "Ecological",
        "STEM"
    );

    const CreateProject = async () => {
        const id = createUniqueId();
        const date = getCurentDate();
        if (
            !verifyText(ProjectName, 50) ||
            !verifyText(Description, 700) ||
            AreaOfImplementation == "0"
        )
            return;
        try {
            const response = await axios.post(
                `${process.env.NEXT_PUBLIC_API_URL}/projects/${id}?project_token=${token}`,
                {
                    id: id,
                    name: ProjectName,
                    area_of_implementation: AreaOfImplementation,
                    creation_date: date,
                    description: Description,
                    created_by: user.id,
                }
            );
            if (response.status == 200) {
                router.push("/");
            } else {
                console.log("ERROR");
            }
        } catch (err) {
            console.log(err);
            document.querySelector(".errorProject").style.display = "block";
        }
    };

    return (
        <ScrollContainer className={styles.Contact} onClick={() => {}}>
            <Head>
                <title>ThinkUp Academy</title>
                <meta name="description" content="Platfoma ThinkUp" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <h1>Create a new project</h1>
            <div className={styles.error + " errorProject"}>
                Invalid token! Please ask your mentor for a valid token.
            </div>
            <InputField
                InputTitle="Token"
                width="675"
                value={token}
                onChange={(e) => setToken(e.target.value)}
            />
            <InputField
                InputTitle="Project Name"
                width="675"
                value={ProjectName}
                onChange={(e) => setProjectName(e.target.value)}
            />
            {/* <SelectField
                value={AreaOfImplementation}
                setValue={(e) => {
                    setFilterValue(e);
                }}
                onChange={(e) => setAreaOfImplementation(e.target.value)}
                options={AreaOfImplementationOptions}
            /> */}
            <SelectField
                selectTitle="Area Of Implementation"
                width="250"
                value={AreaOfImplementation}
                setValue={(e) => {
                    setAreaOfImplementation(e);
                }}
                onChange={(e) => setAreaOfImplementation(e.target.value)}
                options={AreaOfImplementationOptions}
            />
            <TextArea
                areaTitle="Project Description"
                placeholder="Write your project description here..."
                subheader="true"
                subheaderText="You will be able to change this later on the project page."
                width="675"
                value={Description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <div className={styles.btnDiv}>
                <AccentButton text="Create" onClick={() => CreateProject()}>
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
                <CancelButton text="Cancel" onClick={() => router.push("/")} />
            </div>
        </ScrollContainer>
    );
};

export default NewProject;
