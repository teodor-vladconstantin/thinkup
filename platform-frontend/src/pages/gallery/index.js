import React, { useState, useEffect } from "react";
import Head from "next/head";
import axios from "axios";
import styles from "../../../styles/Gallery.module.css";
import ScrollContainer from "../../components/Containers/ScrollContainer";

const Gallery = () => {
    const [Projects, setProjects] = useState(undefined);
    const [Error, setError] = useState("");

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const response = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_URL}/projects`
                );
                setProjects(response.data.projects || []);
            } catch (err) {
                console.log(err);
                setError("Nu am putut încărca galeria. Încearcă din nou mai târziu.");
                setProjects([]);
            }
        };
        fetchProjects();
    }, []);

    const projectsWithPhotos = (Projects || []).filter(
        (project) => project.photos && project.photos.length > 0
    );

    return (
        <ScrollContainer className={styles.Gallery}>
            <Head>
                <title>Galerie - ThinkUp Academy</title>
                <meta name="description" content="Galerie foto cu proiectele elevilor" />
            </Head>
            <h1 className={styles.GalleryTitle}>Galerie</h1>

            {Error && <p className={styles.GalleryMessage}>{Error}</p>}

            {!Error && Projects === undefined && (
                <p className={styles.GalleryMessage}>Se încarcă...</p>
            )}

            {!Error && Projects !== undefined && projectsWithPhotos.length === 0 && (
                <p className={styles.GalleryMessage}>Nicio poză încă</p>
            )}

            {projectsWithPhotos.map((project) => (
                <div key={project.id} className={styles.ProjectSection}>
                    <h2 className={styles.ProjectSectionTitle}>{project.name}</h2>
                    <div className={styles.PhotosGrid}>
                        {project.photos.map((photoUrl, index) => (
                            <div key={index} className={styles.PhotoThumb}>
                                <img src={photoUrl} alt={`${project.name} - poza ${index + 1}`} />
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </ScrollContainer>
    );
};

export default Gallery;
