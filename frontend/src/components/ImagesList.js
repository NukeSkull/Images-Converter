import {Container, ListGroup} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import {useEffect} from "react";

import ImageDownload from "./ImageDownload";
import {fetchImages, memoizedImagesSelector} from "../features/images/imagesSlice";

function ImagesList() {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(fetchImages());
    }, []);

    const images = useSelector(memoizedImagesSelector);

    if (!images || images.length === 0) {
        return <p>No images uploaded. Start by uploading a .png image</p>
    }

    return (
        <ListGroup id="images-list">
            {images.map((image) => (
                <ListGroup.Item key={image.id}
                                variant={image.status === "SUCCESS" ? "success" : "danger"}>
                    <Container className="d-inline-flex w-33">
                        <p>{image.image_name}</p>
                    </Container>
                    <Container className="d-inline-flex w-33 justify-content-center">
                        <p>{image.status}</p>
                    </Container>
                    <Container className="d-inline-flex w-33 justify-content-end">
                        <ImageDownload imageId={image.id} imageName={image.image_name}
                                       status={image.status}/>
                    </Container>
                </ListGroup.Item>
            ))}
        </ListGroup>
    );
}

export default ImagesList;