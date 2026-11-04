
import { useVirtualizer } from "@tanstack/react-virtual";
import { ThumbRow } from "../../bindings/julien/imagius-go/internal";
import { RefObject } from "react";


export default function Grid({ rows, parentRef, colCount, colWidth, rowHeight, headerHeight, gap, onImgClick }:
    {
        rows: (ThumbRow | null)[], parentRef: RefObject<HTMLDivElement | null>, colCount: number, colWidth: number, rowHeight: number,
        headerHeight: number, gap: number, onImgClick: (id: number) => void
    }) {


    const virtualizer = useVirtualizer({
        count: rows.length,
        getScrollElement: () => parentRef.current,
        estimateSize: (index) =>
            rows[index]?.Type === "header-row"
                ? headerHeight + gap
                : rowHeight + gap,
        getItemKey: (index) => rows[index]?.ID ?? index,
        overscan: 3,
    });

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
                                {row?.Thumbs?.map((item) => (
                                    <div
                                        key={item?.ID}
                                        onClick={() => onImgClick(item?.ID ?? 0)}
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
