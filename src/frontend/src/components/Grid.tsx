
import { useVirtualizer } from "@tanstack/react-virtual";
import { ThumbRow } from "../../bindings/julien/imagius-go/internal";
import { RefObject } from "react";

// const ITEMS = Array.from({ length: 10000 }, (_, i) => ({
//     id: i,
//     title: `Thumbnail ${i + 1}`,
//     image: `https://picsum.photos/seed/${i}/300/200`,
// }));

// const COLUMNS = 7;
// const COLUMN_WIDTH = 180;
// const ROW_HEIGHT = 160;
// const HEADER_HEIGHT = 48;
// const GAP = 12;

// type GridRow =
//     | {
//         type: "header";
//         id: stringconst COLUMNS = 7;
//         title: string;
//     }
//     | {
//         type: "images";
//         id: string;
//         items: typeof ITEMS;
//     };

// function createRows(): GridRow[] {
//     const rows: GridRow[] = [];
//     const sectionSize = 30;

//     for (let i = 0; i < ITEMS.length; i += sectionSize) {
//         rows.push({
//             type: "header",
//             id: `header-${i}`,
//             title: `Section ${i / sectionSize + 1}`,
//         });

//         const sectionItems = ITEMS.slice(i, i + sectionSize);

//         for (let j = 0; j < sectionItems.length; j += COLUMNS) {
//             rows.push({
//                 type: "images",
//                 id: `images-${i}-${j}`,
//                 items: sectionItems.slice(j, j + COLUMNS),
//             });
//         }
//     }

//     return rows;
// }

// const rows = createRows();

export default function Grid({ rows, parentRef, colCount, colWidth, rowHeight, headerHeight, gap }:
    { rows: (ThumbRow | null)[], parentRef: RefObject<HTMLDivElement | null>, colCount: number, colWidth: number, rowHeight: number, headerHeight: number, gap: number }) {


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
