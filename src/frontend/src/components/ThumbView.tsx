import { useEffect, useState } from "react";
import { GetScanImgsRow, LibraryService, } from "../../bindings/julien/imagius-go/internal";
import Grid from "./Grid";




function ThumbView() {
    const [thumbs, setThumbs] = useState<GetScanImgsRow[]>([]);

    useEffect(() => {
        (async () => {
            let imgs = await LibraryService.GetImages();
            console.log(imgs);
            setThumbs(imgs!);
        })();
    }, []);

    return (
        <div>
            <Grid items={thumbs!} />
        </div>
    );
}
export default ThumbView;