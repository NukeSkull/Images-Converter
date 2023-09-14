import React, {useEffect, useState} from "react";
import {Button, Container, Form} from "react-bootstrap";
import {ToastContainer} from 'react-toastify';
import 'bootstrap/dist/css/bootstrap.min.css';
import {useDispatch} from "react-redux";

import ImagesList from "./components/ImagesList";
import DropBox from "./components/DropBox";
import {postImage} from "./features/images/imagesSlice"

import "./App.css";

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [formSubmitted, setFormSubmitted] = useState(false);
    const dispatch = useDispatch();

    const handleFileChange = (acceptedFiles) => {
        setSelectedFile(acceptedFiles[0]);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        setFormSubmitted(true);

        if (selectedFile) {
            const formData = new FormData();
            formData.append("png_image", selectedFile);

            dispatch(postImage(formData))
        }
    };

    useEffect(() => {
        if (formSubmitted) {
            setFormSubmitted(false);
        }
    }, [formSubmitted]);

    return (
        <div className="App">
            <Container>
                <Form role="form " id="upload-form" onSubmit={handleSubmit}
                      encType="multipart/form-data">
                    <DropBox onDrop={handleFileChange}
                             resetSelectedFile={formSubmitted}/>
                    <Button id="upload-btn" type="submit"
                            disabled={!selectedFile}>Upload</Button>
                </Form>
            </Container>
            <Container>
                <ImagesList/>
            </Container>
            <ToastContainer
                position="top-center"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                theme="dark"
            />
        </div>
    );
}

export default App;