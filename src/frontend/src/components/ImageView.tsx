import { useEffect, useState } from "react";
import { LibraryService, ScanImg } from "../../bindings/julien/imagius-go/internal";

function ImageView({ id }: { id: number }) {
    const [img, setImg] = useState<ScanImg | null>(null);

    useEffect(() => {
        console.log("Fetching image with id:", id);
        (async () => {
            let img = await LibraryService.GetImage(id);
            console.log(img);
            if (img !== null) {
                setImg(img)
            }
        })();
    }, []);


    return (
        <img
            src={img?.AbsPath ? '/img/' + img?.AbsPath : '/missing-thumb.png'}
            alt={img?.Name ?? ""}
            loading="lazy"
            style={{
                width: "100%",
                height: "auto",
                objectFit: "contain",
            }}
        />
    );
}

export default ImageView;   