import react, { useEffect, useState } from "react";
import Head from "next/head";
import styles from "../../../styles/OpenSchool.module.css";
import SearchBar from "../../components/FormElems/SearchBar";
import File from "../../components/Cards/File";
import { useRouter } from "next/router";
import ScrollContainer from "../../components/Containers/ScrollContainer";
import axios from "axios";
import { useMyUserContext } from "../../contexts/UserContext";
import AccentButton from "../../components/Buttons/AccentButton";

const OpenSchool = () => {
    const [SearchValue, setSearchValue] = useState("");
    const [DocumentFiles,setDocumentFiles] = useState([]);
    const [ImageFiles,setImageFiles] = useState([]);
    const [EtcFiles,setEtcFiles] = useState([]);
    const [FilterValue,setFilterValue] = useState("File Types");
    const [AllFiles,setAllFiles] = useState([]);
    const [Language,setLanguage] = useState("en");
    const [FavoriteFiles,setFavouriteFiles] = useState([]);

    const documents_per_page = 6;

    const[ShownDocumentFiles,setShownDocumentFiles] = useState(documents_per_page);
    const[ShownImageFiles,setShownImageFiles] = useState(documents_per_page);
    const[ShownEtcFiles,setShownsEtcFiles] = useState(documents_per_page);

    const User = useMyUserContext();

    const router = useRouter();


    const RouteTo = (new_route) => {
        console.log(router.pathname);
        router.push(new_route);
    };


    const messages ={
        "en":{
            search_text:"Search documents",
            description:"Here you can find the documents available for everyone.",
            file_types:"File Types",
            most_viewed:"Most Viewed",
            favourites: "Favourites",
            newest:"Newest",
            oldest:"Oldest",
            more_text:"View more",
            main_text:"If you’d like something new, feel free to mail us. We’ll take it into consideration."
        },
        "ro":{
            search_text:"Caută documente",
            description:"Aici puteti gasi documente accesibile tuturor.",
            file_types:"Tipuri de fisier",
            most_viewed:"Cele mai vizualizate",
            favourites: "Favorite",
            newest:"Cele mai noi",
            oldest:"Cele mai vechi",
            more_text:"Mai mult",
            main_text:"Daca ati dori ceva nou, va rugam sa ne scrieti un mail. Va vom lua in considerare."
        }
    }


    const getFilesWithExtension = async (array,extension) =>{
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/openSchool/search/byFiletype/${extension}`);
        response.data.file.forEach(file=>{
            array.push(file);  
        })
        return array;
    }


    const getFilesByFileType = async () =>{
        let DocumentArray = await getFilesWithExtension([],'pdf');
        DocumentArray = await getFilesWithExtension(DocumentArray,'doc');
        DocumentArray = await getFilesWithExtension(DocumentArray,'docx');
        setDocumentFiles(DocumentArray);

        let ImageArray = await getFilesWithExtension([],'jpg')
        ImageArray = await getFilesWithExtension(ImageArray,'jpeg');
        ImageArray = await getFilesWithExtension(ImageArray,'png');
        ImageArray = await getFilesWithExtension(ImageArray,'psd');
        ImageArray = await getFilesWithExtension(ImageArray,'gif');
        ImageArray = await getFilesWithExtension(ImageArray,'mp4');
        ImageArray = await getFilesWithExtension(ImageArray,'mov');
        setImageFiles(ImageArray);

        let EtcArray = await getFilesWithExtension([],'etc');
        setEtcFiles(EtcArray);
    }


    const getAllFiles = async (filter) =>{
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/openSchool/search/${filter}`);
        console.log(response.data);
        setAllFiles(response.data.sorted);
    }

    const getFilesByTime = async (filter)=>{
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/openSchool/search/byTime/${filter}`);
        console.log(response.data.sorted[0]);
        setAllFiles(response.data.sorted[0]);
    }

    const getFavouriteFiles = async ()=>{
        if (User == undefined) {
            console.log("User ID is undefined. Cannot show favorite files.");
            setAllFiles([]);
            return;
        }

        try {
            console.log("Fetching favorite files for user:", User.id);
            
            // Get favorite file IDs from user
            const favResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/users/favFiles/${User.id}`);
            console.log("Favorite IDs response:", favResponse.data);
            
            let favouriteFilesArray = favResponse.data.fav_files || favResponse.data || [];
            
            // Remove duplicates from the favorites array
            favouriteFilesArray = [...new Set(favouriteFilesArray)];
            console.log("Favorite file IDs (without duplicates):", favouriteFilesArray);
            
            if (Array.isArray(favouriteFilesArray) && favouriteFilesArray.length > 0) {
                // Get all files and filter by favorites
                const allFilesResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/openSchool/search/mostPopular`);
                console.log("All files response:", allFilesResponse.data);
                
                const allFiles = allFilesResponse.data.sorted || [];
                const favoriteFiles = allFiles.filter(file => favouriteFilesArray.includes(file.id));
                console.log("Filtered favorite files:", favoriteFiles);
                
                setAllFiles(favoriteFiles);
            } else {
                console.log("No favorite files found");
                setAllFiles([]);
            }
        } catch (error) {
            console.log("Error fetching favorite files:", error);
            setAllFiles([]);
        }
    }
    

    useEffect(async()=>{
        switch(FilterValue){
            case "File Types":
                getFilesByFileType();
                break;
            case "Most Viewed":
                getAllFiles("mostPopular");
                break;
            case "Newest":
                getFilesByTime("desc");
                break;
            case "Oldest":
                getFilesByTime("asc");
                break;
            case "Favourite":
                getFavouriteFiles();
                break;
        }


    },[FilterValue]);


    const searchForProjects = async () =>{
        if(SearchValue=="") {getAllFiles("mostPopular"); return}
        const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/openSchool/search/${SearchValue}`);
        console.log(response.data.file);
        setFilterValue("Search");
        setAllFiles(response.data.file)

    }


    useEffect(()=>{
        if(User!=undefined && User.settings!=undefined)
            setLanguage(User.settings.language);
        

    },[User])

    return (
        <ScrollContainer className={styles.Container}>
            <div className={styles.OpenSchoolHeader}>
                <Head>
                    <title>ThinkUp Academy</title>
                    <meta name="description" content="Platfoma ThinkUp" />
                    <link rel="icon" href="/favicon.ico" />
                </Head>
                <h1>Open School</h1>
                <h4>{Language=="ro"?messages.ro.description:messages.en.description}</h4>
                <div className={styles.navbar}>
                    <div>
                        <ul>
                            <li>
                                <a onClick={()=>setFilterValue("File Types")} className={FilterValue=="File Types"?styles.active:''}>
                                    {Language=="ro"?messages.ro.file_types:messages.en.file_types}
                                </a>
                            </li>
                            <li>
                                <a onClick={()=>setFilterValue("Most Viewed")} className={FilterValue=="Most Viewed"?styles.active:''}>
                                    {Language=="ro"?messages.ro.most_viewed:messages.en.most_viewed}</a>
                            </li>
                            <li>
                                <a onClick={()=>setFilterValue("Favourite")} className={FilterValue=="Favourite"?styles.active:''}>
                                {Language=="ro"?messages.ro.favourites:messages.en.favourites}</a>
                            </li>
                            <li>
                                <a onClick={()=>setFilterValue("Newest")} className={FilterValue=="Newest"?styles.active:''}>
                                    {Language=="ro"?messages.ro.newest:messages.en.newest}</a>
                            </li>
                            <li>
                                <a onClick={()=>setFilterValue("Oldest")} className={FilterValue=="Oldest"?styles.active:''}>
                                    {Language=="ro"?messages.ro.oldest:messages.en.oldest}</a>
                            </li>
                            
                        </ul>
                    </div>
                    <SearchBar
                        Placeholder={Language=="ro"?messages.ro.search_text:messages.en.search_text}
                        search_value={SearchValue}
                        changeValue={(e) => setSearchValue(e.target.value)}
                        onsearch={() => searchForProjects()}
                    />
                </div>
            </div>

            {FilterValue=="File Types"?
            <ScrollContainer className={styles.OpenSchool_ScrollContainer}>
                <div className={styles.DocGroup}>
                    <div className={styles.DocHeaders}>
                        <h3>PDFs &amp; Docs</h3>
                        {DocumentFiles.length<=documents_per_page?<></>:<a onClick={() => setShownDocumentFiles(ShownDocumentFiles+documents_per_page)}>{Language=="ro"?messages.ro.more_text:messages.en.more_text}</a>}
                    </div>

                    <div className={styles.FilesLine}>
                    {
                        DocumentFiles.slice(0, ShownDocumentFiles)?.map((filedata, index) => {
                            // Check if User is defined and the condition is met
                            if (User === undefined && !filedata.public) {
                                return null; // Skip rendering this file
                            }
                            // Render the File component for valid files
                            return (
                                <File key={index} name={filedata.search_term} id={filedata.id} extension={filedata.extension.toUpperCase().substring(1)} size="36KB" action="download" user_id={User?.id}></File>
                            );
                        })
                    }
                    </div>
                </div>

                <div className={styles.DocGroup}>
                    <div className={styles.DocHeaders}>
                        <h3>Videos &amp; Images</h3>
                        {ImageFiles.length<=documents_per_page?<></>:<a onClick={() => setShownImageFiles(ShownImageFiles+documents_per_page)}>{Language=="ro"?messages.ro.more_text:messages.en.more_text}</a>}
                    </div>
                    <div className={styles.FilesLine}>
                    {
                        ImageFiles.slice(0, ShownImageFiles)?.map((filedata, index) => {
                            // Check if User is defined and the condition is met
                            if (User === undefined && !filedata.public) {
                                return null; // Skip rendering this file
                            }
                            // Render the File component for valid files
                            return (
                                <File key={index} name={filedata.search_term} id={filedata.id} extension={filedata.extension.toUpperCase().substring(1)} size="36KB" action="download" user_id={User?.id}></File>
                            );
                        })
                    }
                    </div>
                </div>

                <div className={styles.DocGroup}>
                    <div className={styles.DocHeaders}>
                        <h3>Other Files</h3>
                        {EtcFiles.length<=documents_per_page?<></>:<a onClick={() => setShownsEtcFiles(ShownEtcFiles+documents_per_page)}>{Language=="ro"?messages.ro.more_text:messages.en.more_text}</a>}
                    </div>
                    <div className={styles.FilesLine}>
                    {
                        EtcFiles.slice(0, ShownEtcFiles)?.map((filedata, index) => {
                            // Check if User is defined and the condition is met
                            if (User === undefined && !filedata.public) {
                                return null; // Skip rendering this file
                            }

                            // Render the File component for valid files
                            return (
                                <File key={index} name={filedata.search_term} id={filedata.id} extension={filedata.extension.toUpperCase().substring(1)} size="36KB" action="download" user_id={User?.id}></File>
                            );
                        })
                    }
                    </div>
                </div>
            </ScrollContainer>:<></>}


            {FilterValue=="Most Viewed"||FilterValue=="Newest"||FilterValue=="Oldest"||FilterValue=="Search"||FilterValue=="Favourite"?
            <ScrollContainer className={styles.OpenSchool_ScrollContainer}>
                <div className={styles.FilesLine}>
                    {

                        AllFiles?.filter((filedata)=>{
                            if(filedata.extension==undefined)
                                return false;
                            if(User==undefined && !filedata.public)
                                return false;
                            return true;
                        }).map((filedata,index)=>{
                            return <File 
                                key={index} 
                                name={filedata.search_term} 
                                id={filedata.id} 
                                extension={filedata.extension.toUpperCase().substring(1)} 
                                size="36KB" 
                                action="download" 
                                user_id={User?.id}
                                {...(FilterValue=="Favourite" && { 
                                    isFavorite: true,
                                    onToggleFavorite: () => getFavouriteFiles()
                                })}
                            ></File>
                        })
                    }

                </div>

            </ScrollContainer>:<></>}


            <div className={styles.NoteDiv}>
                <svg
                    width="25"
                    height="25"
                    viewBox="0 0 25 25"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        d="M20.3125 20.3125H4.6875V4.6875H12.5V3.125H4.6875C4.27323 3.12541 3.87604 3.29017 3.5831 3.5831C3.29017 3.87604 3.12541 4.27323 3.125 4.6875V20.3125C3.12541 20.7268 3.29017 21.124 3.5831 21.4169C3.87604 21.7098 4.27323 21.8746 4.6875 21.875H20.3125C20.7268 21.8746 21.124 21.7098 21.4169 21.4169C21.7098 21.124 21.8746 20.7268 21.875 20.3125V12.5H20.3125V20.3125Z"
                        fill="#888888"
                    />
                    <path
                        d="M20.3125 20.3125H4.6875V4.6875H12.5V3.125H4.6875C4.27323 3.12541 3.87604 3.29017 3.5831 3.5831C3.29017 3.87604 3.12541 4.27323 3.125 4.6875V20.3125C3.12541 20.7268 3.29017 21.124 3.5831 21.4169C3.87604 21.7098 4.27323 21.8746 4.6875 21.875H20.3125C20.7268 21.8746 21.124 21.7098 21.4169 21.4169C21.7098 21.124 21.8746 20.7268 21.875 20.3125V12.5H20.3125V20.3125Z"
                        fill="#888888"
                    />
                    <path
                        d="M20.3125 4.6875V1.5625H18.75V4.6875H15.625V6.25H18.75V9.375H20.3125V6.25H23.4375V4.6875H20.3125Z"
                        fill="#888888"
                    />
                </svg>

                <h4 className={styles.note}>
                    If you’d like something new, feel free to{" "}
                    <span>
                        <a onClick={() => RouteTo("/Contact")}>mail us</a>
                    </span>
                    . We’ll take it into consideration.{" "}
                </h4>
            </div>
        </ScrollContainer>
    );
};
export default OpenSchool;
