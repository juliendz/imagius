import { useEffect, useState } from "react";
import { useAppDispatch } from "../hooks";
import { ShowThumbsView } from "../appStore";
import Viewer from "react-viewer";
import { LibraryService } from "../../bindings/julien/imagius-go/internal";
import { ImageDecorator } from "react-viewer/lib/ViewerProps";

function SlideShowView({ dirId, sortBy, startImgIdx }: { dirId: number, sortBy: string, startImgIdx: number }) {
    const dispatch = useAppDispatch();
    const [imgs, setImgs] = useState<ImageDecorator[]>([]);

    useEffect(() => {
        (async () => {
            let imgs = await LibraryService.GetSlideShowImages(dirId, sortBy);
            console.log(imgs);
            if (imgs !== null && imgs.length > 0) {
                setImgs(imgs as ImageDecorator[])
            }
        })();
    }, []);

    const handleClose = () => {
        dispatch(ShowThumbsView());
    };

    return (
        <Viewer
            visible={true}
            onClose={() => { handleClose() }}
            images={imgs}
            activeIndex={startImgIdx}
        />

    );
}

export default SlideShowView;   