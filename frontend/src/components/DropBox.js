import {useEffect, useRef, useState} from "react";
import {useDropzone} from "react-dropzone";
import Container from 'react-bootstrap/Container'

function DropBox({onDrop, resetSelectedFile}) {
    const [imageName, setImageName] = useState('');
    const [imagePreview, setImagePreview] = useState(null)
    const inputRef = useRef(null);
    const error = 'Only .png files are allowed. Please drag and drop .png images here, or click to select';

    useEffect(() => {
        setImageName("");
        setImagePreview(null);
        inputRef.current = "";
    }, [resetSelectedFile]);

    const handleFileChange = (acceptedFiles) => {
        const file = acceptedFiles[0];
        setImageName(file ? file.name : '');
        if (file) {
            const previewURL = URL.createObjectURL(file);
            setImagePreview(previewURL);
        }
        onDrop(acceptedFiles);
    };

    const {getRootProps, getInputProps, fileRejections} = useDropzone({
        accept: {
            'image/png': ['.png'],
        },
        maxFiles: 1,
        onDrop: handleFileChange,
    });

    return (
        <>
            <section className="dropbox" id="dropbox">
                <Container {...getRootProps()}>
                    <input
                        ref={(node) => {
                            inputRef.current = node;
                            getInputProps({ref: node});
                        }}
                        id="input-image"
                        {...getInputProps()}
                    />
                    {fileRejections.length > 0 ? (
                        <p className="error">{error}</p>
                    ) : (
                        <div>
                            <p>Drag and drop .png images here, or click to select</p>
                            {imagePreview &&
                                <img src={imagePreview} className="img" onLoad={() => {
                                    URL.revokeObjectURL(imagePreview)
                                }}/>}
                            <p>{imageName}</p>
                        </div>
                    )}
                </Container>
            </section>
        </>
    );
}

export default DropBox;