import { useEffect, useRef, useState } from "react";
import { LibraryService } from "../../bindings/julien/imagius-go/internal";
import { ImageDecorator } from "react-viewer/lib/ViewerProps";
import PhotoSwipe from "photoswipe";

function SlideShowView({ dirId, sortBy, startImgIdx, onClose }: { dirId: number, sortBy: string, startImgIdx: number, onClose: () => void }) {
    const lightboxRef = useRef<PhotoSwipe | null>(null);
    const [imgs, setImgs] = useState<ImageDecorator[]>([]);

    console.log("SlideShowView with startImgIdx:", startImgIdx);

    useEffect(() => {
        (async () => {
            let resp = await LibraryService.GetSlideShowImages(dirId, sortBy);
            if (resp !== null && resp.length > 0) {
                setImgs(resp as ImageDecorator[])
            }
        })();
    }, []);

    useEffect(() => {
        if (imgs.length > 0) {
            console.log("SlideShowView updated with startImgIdx:", startImgIdx);
            const options = {
                dataSource: imgs,
                index: startImgIdx,
                wheelToZoom: true
            };
            lightboxRef.current = new PhotoSwipe(options);
            lightboxRef.current.on('destroy', () => {
                onClose();
            });
            lightboxRef.current.init();
        }

        //cleanup
        return () => {
            if (lightboxRef.current) {
                // Force-close the active UI modal if it's currently open
                if (lightboxRef.current.pswp) {
                    lightboxRef.current.pswp.destroy();
                }
                // Unbind all global resize, keyboard, and window event listeners
                lightboxRef.current.destroy();
                lightboxRef.current = null;
            }
        };
    }, [imgs]);


    return null;
}

export default SlideShowView;   