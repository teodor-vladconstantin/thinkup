import React,{useEffect, useState} from "react";
import styles from "../../../styles/MaterialsTable.module.css";
import { useRouter } from "next/router";
import DefaultContainer from "../Containers/DefaultContainer";
import DefaultContainer2 from "../Containers/DefaultContainer2";
import MaterialCard from "../Cards/MaterialCard";
import NewMaterialCard from "../Cards/NewMaterialCard";
import MaterialPopUp from "../PopUp/MaterialPopUp";
import NewMaterialPopUp from "../PopUp/NewMaterialPopUp";
import { AnimatePresence } from "framer-motion";


const MaterialsTable = (props) => {
    const [OpenedMaterial,setOpenedMaterial] = useState(null);
    const [NewMaterialPopUpState,setNewMaterialPopUpState] = useState(false);
    const [OpenedMenuMaterial,setOpenedMenuMaterial]= useState(null);
    /*<div className={styles.ProjectsTableShadow}></div>*/

    const messages ={
        "en":{
            material_title:"Materials",
            no_material_text:"There are no materials on this project",
            add_material_text:"Add a new material"
        },
        "ro":{
            material_title:"Materiale",
            no_material_text:"Nu sunt materiale in acest proiect",
            add_material_text:"Adauga un nou material"
        }
    }
    
    const router = useRouter();

    if (props.data == undefined)
        return (
            <DefaultContainer className={styles.MaterialsTableContainer + " " + props.className} onClick={()=>{}}>
                <p className={styles.MaterialsTableTitle}>{props.language=="ro"?messages.ro.material_title:messages.en.material_title}</p>
                <NewMaterialCard onClick={()=>setNewMaterialPopUpState(true)}/>
            </DefaultContainer>
        );

    return (
        <DefaultContainer className={styles.MaterialsTableContainer + " " + props.className} onClick={()=>{}}>
            <p className={styles.MaterialsTableTitle}>{props.language=="ro"?messages.ro.material_title:messages.en.material_title}</p>
            {props.AdminState?<NewMaterialCard onClick={()=>setNewMaterialPopUpState(true)}>{props.language=="ro"?messages.ro.add_material_text:messages.en.add_material_text}</NewMaterialCard>:<></>}
            {props.data.length==0?<p className={styles.NoMaterialText}>{props.language=="ro"?messages.ro.no_material_text:messages.en.no_material_text}</p>:
            props.data.map((projectdata, index) => {
                return <MaterialCard title={projectdata.name} index={index} nrofmaterials={props.data.length} date={projectdata.creationDate} id={projectdata.id} key={index} onClick={()=>setOpenedMaterial(index)} refresh={()=>props.getProjectData()} MenuState={index==OpenedMenuMaterial} openMenu={()=>setOpenedMenuMaterial(index)} closeMenu={()=>setOpenedMenuMaterial(null)}/>
            })}
            
            <AnimatePresence exitBeforeEnter={true}>
            {OpenedMaterial!=null&&<MaterialPopUp title={props.data[OpenedMaterial].name} date={props.data[OpenedMaterial].creationDate} description={props.data[OpenedMaterial].description}  close={()=>setOpenedMaterial(null)}/>}
            {NewMaterialPopUpState&&<NewMaterialPopUp close={()=>setNewMaterialPopUpState(false)} addedmaterial={()=>{setNewMaterialPopUpState(false);props.getProjectData()}} Projectid={props.Projectid}/>}
            </AnimatePresence>
        </DefaultContainer>
    );
};

export default MaterialsTable;
