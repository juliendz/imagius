
import { useVirtualizer } from "@tanstack/react-virtual";
import { ThumbRow } from "../../bindings/julien/imagius-go/internal";
import { RefObject, useEffect, useState } from "react";
import { ActionIcon } from "@mantine/core";
import { PlayIcon } from "@phosphor-icons/react";
import { useAppSelector } from "../hooks";


export default function Grid({ rows, parentRef, colCount, colWidth, rowHeight, headerHeight, gap, onImgClick, onSlideShowClick }:
    {
        rows: (ThumbRow | null)[], parentRef: RefObject<HTMLDivElement | null>, colCount: number, colWidth: number, rowHeight: number,
        headerHeight: number, gap: number, onImgClick: (id: number) => void, onSlideShowClick: (dirId: number, startIdx: number) => void
    }) {
    const currDirIndex = useAppSelector(state => state.appStore.currDirIndex);
    const triggerScroll = useAppSelector(state => state.appStore.triggerScroll);
    const [selectedThumbIndex, setSelectedThumbIndex] = useState<number>(0);


    const virtualizer = useVirtualizer({
        count: rows.length,
        getScrollElement: () => parentRef.current,
        estimateSize: (index) => {
            if (rows[index]?.Type === "header-row") {
                return headerHeight + gap;
            }
            let rowCount = (rows[index]?.Thumbs?.length ?? 0) / colCount;
            return rowHeight * Math.ceil(rowCount ?? 0) + gap;
        },
        getItemKey: (index) => rows[index]?.ID ?? index,
        overscan: 3,
    });


    useEffect(() => {
        if (virtualizer && currDirIndex !== null) {
            console.log('ScrollToIndex:', currDirIndex);
            virtualizer.scrollToIndex(currDirIndex, { align: "start", behavior: "smooth" });
        }
    }, [currDirIndex, triggerScroll]);


    return (
        <div
            style={{
                height: virtualizer.getTotalSize(),
                position: "relative",
                width: "100%",
            }}
        >
            {virtualizer.getVirtualItems().map((virtualRow) => {
                const row = rows[virtualRow.index];
                // console.log(virtualRow, row);

                return (
                    <div
                        key={row?.Key ?? virtualRow.key}
                        style={{
                            position: "absolute",
                            top: 0,
                            left: 0,
                            width: "100%",
                            height:
                                row?.Type === "header-row"
                                    ? headerHeight + gap
                                    : rowHeight + gap,
                            transform: `translateY(${virtualRow.start}px)`,
                        }}
                    >
                        {row?.Type === "header-row" ? (
                            <div
                                style={{
                                    height: headerHeight,
                                    display: "flex",
                                    alignItems: "center",
                                    padding: "0 12px",
                                    fontWeight: "bold",
                                    background: "#ddd",
                                    borderRadius: 6,
                                }}
                            >
                                {row?.Name}
                                <ActionIcon variant="filled" aria-label="Settings" onClick={() => onSlideShowClick(row?.ID ?? 0, selectedThumbIndex)}>
                                    <PlayIcon style={{ width: '70%', height: '70%' }} />
                                </ActionIcon>
                            </div>
                        ) : (
                            <div
                                style={{
                                    display: "grid",
                                    gridTemplateColumns:
                                        `repeat(${colCount}, ${colWidth}px)`,
                                    gap: gap,
                                }}
                            >
                                {row?.Thumbs?.map((item, index) => (
                                    <div
                                        key={item?.ID}
                                        onDoubleClick={() => onImgClick(item?.ID ?? 0)}
                                        onClick={() => setSelectedThumbIndex(index)}
                                        className={selectedThumbIndex === index ? "thumb-active" : ""}
                                        style={{
                                            height: rowHeight,
                                            background: "#eee",
                                            borderRadius: 8,
                                            overflow: "hidden",
                                        }}
                                    >
                                        <img
                                            src={item?.ThumbPath ? '/thumbs/' + item?.ThumbPath : '/missing-thumb.png'}
                                            alt={item?.Name}
                                            loading="lazy"
                                            className="thumb-fade-effect"
                                            style={{
                                                width: "100%",
                                                height: rowHeight,
                                                objectFit: "contain",
                                            }}
                                        />
                                        <div style={{ padding: 6 }}>
                                            {item?.Name}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                );
            })}
        </div>
    );
}
