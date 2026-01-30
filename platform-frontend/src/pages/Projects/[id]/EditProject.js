import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import styles from "../../../../styles/EditProject.module.css";
import InputField from "../../../components/FormElems/InputField";
import ImageInput from "../../../components/FormElems/ImageInput";
import TextArea from "../../../components/FormElems/TextArea";
import AccentButton from "../../../components/Buttons/AccentButton";
import CancelButton from "../../../components/Buttons/CancelButton";
import SelectField from "../../../components/FormElems/SelectField";
import ScrollContainer from "../../../components/Containers/ScrollContainer";
import { verifyText, createUniqueId } from "../../../utils/utils";
import axios from "axios";
import FormData from "form-data";

const EditProject = () => {
    const router = useRouter();
    const { id } = router.query;
    const [ProjectTitle, setProjectTitle] = useState("");
    const [ProjectDescription, setProjectDescription] = useState("");
    const [File, setFile] = useState(null);
    const [AreaOfImplementation, setAreaOfImplementation] = useState("Select");

    const getProjectData = async () => {
        const response = await axios.get(
            `${process.env.NEXT_PUBLIC_API_URL}/projects/${id}`
        );
        console.log(response);
        setProjectTitle(response.data.name);
        setProjectDescription(response.data.description);
        setAreaOfImplementation(response.data.areaOfImplementation)
        // switch (response.data.areaOfImplementation) {
        //     case "Civic Education":
        //         setAreaOfImplementation(1);
        //         break;
        //     case "Ecological":
        //         setAreaOfImplementation(2);
        //         break;
        //     case "STEM":
        //         setAreaOfImplementation(3);
        //         break;
        //     default:
        //         break;
        // }
    };

    useEffect(() => {
        getProjectData();
        console.log(id);
    }, [id]);

    const AreaOfImplementationOptions = new Array(
        "Civic Education",
        "Ecological",
        "STEM"
    );

    const handleFileChange = (e) => {
        const [f] = e.target.files;
        setFile(f);
    };

    const EditProject = async () => {
        if (
            !verifyText(ProjectTitle, 20) ||
            !verifyText(ProjectDescription, 200)
        )
            return;

        const formdata = new FormData();

        const imageId = createUniqueId();

        formdata.append(
            "json",
            JSON.stringify({
                name: ProjectTitle,
                description: ProjectDescription,
                thumbnail: imageId,
                created_by: "106863809771378515645",
                areaOfImplementation: AreaOfImplementation,
            })
        );

        formdata.append("file", File);

        const response = await axios.put(
            `${process.env.NEXT_PUBLIC_API_URL}/projects/${id}`,
            formdata
        );
        if (response.status == 200) {
            console.log("Evrica");
            router.back();
        } else {
            console.log("ERROR");
        }
    };

    return (
        <ScrollContainer>
            <div className={styles.EditProject}>
                <h1 className={styles.EditProjectTitle}>Edit Project</h1>
                <InputField
                    InputTitle="Project Title"
                    width="675"
                    value={ProjectTitle}
                    onChange={(e) => setProjectTitle(e.target.value)}
                    placeholder="Set title"
                />
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
                <ImageInput
                    setSelectedFile={(file) => handleFileChange(file)}
                />
                <TextArea
                    areaTitle="Description"
                    placeholder="Write your description here..."
                    subheader="false"
                    className={styles.EditUserDescription}
                    value={ProjectDescription}
                    onChange={(e) => setProjectDescription(e.target.value)}
                    width="675"
                />
                <div className={styles.EditProjectButtonDiv}>
                    <AccentButton text="Save" onClick={() => EditProject()}>
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
                    <CancelButton text="Cancel" onClick={() => router.back()} />
                </div>
            </div>
        </ScrollContainer>
    );
};

export default EditProject;
