import { useEffect, useRef, useState } from "react";
import { LibraryService, ThumbRow, } from "../../bindings/julien/imagius-go/internal";
import Grid from "./Grid";
import { useAppDispatch } from "../hooks";
import { ShowImageView, ShowSlideshowView } from "../appStore";

const COLUMN_WIDTH = 160;
const ROW_HEIGHT = 160;
const HEADER_HEIGHT = 48;
const GAP = 12;


function ThumbView() {
    const dispatch = useAppDispatch();
    const parentRef = useRef<HTMLDivElement>(null);
    const [colCount, setColCount] = useState(1);
    const [rows, setRows] = useState<(ThumbRow | null)[]>([]);


    useEffect(() => {
        console.log(parentRef.current?.clientWidth);
        setColCount(Math.max(
            1,
            Math.floor((parentRef.current?.clientWidth ?? 900) / (COLUMN_WIDTH + GAP)),
        ));
        console.log((parentRef.current?.clientWidth ?? 900) / (COLUMN_WIDTH + GAP));
    }, []);

    useEffect(() => {
        console.log((parentRef.current?.clientWidth ?? 900) / (COLUMN_WIDTH + GAP), colCount);
        (async () => {

            let imgs = await LibraryService.GetImages(colCount);
            console.log(imgs);
            if (imgs !== null) {
                setRows(imgs);
            }
        })();
    }, [colCount]);

    const handleImageClick = (id: number) => {
        dispatch(ShowImageView(id));
    }

    const handleSlideShowClick = (dirId: number, startIdx: number) => {
        dispatch(ShowSlideshowView({ dirId, startIdx }));
    }

    return (
        <div
            ref={parentRef}
            style={{
                height: 750,
                width: "100%",
                overflow: "auto",
            }}
        >
            <Grid rows={rows} colCount={colCount} parentRef={parentRef} colWidth={COLUMN_WIDTH} rowHeight={ROW_HEIGHT} headerHeight={HEADER_HEIGHT} gap={GAP}
                onImgClick={handleImageClick} onSlideShowClick={handleSlideShowClick} />
        </div>
    );
}
export default ThumbView;