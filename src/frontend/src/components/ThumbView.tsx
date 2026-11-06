import { useEffect, useRef, useState } from "react";
import Grid from "./Grid";
import { useAppDispatch, useAppSelector } from "../hooks";
import { ShowImageView, ShowSlideshowView } from "../appStore";
import { getLibrary } from "../thunk";

const COLUMN_WIDTH = 160;
const ROW_HEIGHT = 160;
const HEADER_HEIGHT = 48;
const GAP = 12;


function ThumbView() {
    const dispatch = useAppDispatch();
    const parentRef = useRef<HTMLDivElement>(null);
    const [colCount, setColCount] = useState(1);
    const thumbRows = useAppSelector(state => state.appStore.library.Thumbs);


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
            dispatch(await getLibrary());
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
            <Grid rows={thumbRows ? thumbRows : []} colCount={colCount} parentRef={parentRef} colWidth={COLUMN_WIDTH} rowHeight={ROW_HEIGHT} headerHeight={HEADER_HEIGHT} gap={GAP}
                onImgClick={handleImageClick} onSlideShowClick={handleSlideShowClick} />
        </div>
    );
}
export default ThumbView;