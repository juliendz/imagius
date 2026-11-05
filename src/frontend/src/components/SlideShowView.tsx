import { useEffect, useState } from "react";
import { useAppDispatch } from "../hooks";
import { ShowThumbsView } from "../appStore";
import Viewer from "react-viewer";
import { LibraryService } from "../../bindings/julien/imagius-go/internal";
import { ImageDecorator } from "react-viewer/lib/ViewerProps";

function SlideShowView({ dirId, sortBy, startImgIdx }: { dirId: number, sortBy: string, startImgIdx: number }) {
    const dispatch = useAppDispatch();
    const [imgs, setImgs] = useState<ImageDecorator[]>([]);

    console.log(imgs, startImgIdx);
    useEffect(() => {
        (async () => {
            let resp = await LibraryService.GetSlideShowImages(dirId, sortBy);
            if (resp !== null && resp.length > 0) {
                setImgs(resp as ImageDecorator[])
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
            drag={false}
        />

    );
}

export default SlideShowView;   