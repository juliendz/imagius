import { useVirtualizer } from "@tanstack/react-virtual";
import { Fragment, useRef } from "react";
import type { GetScanImgsRow } from "../../bindings/julien/imagius-go/internal";

function GridVirtualizerFixed({ items }: { items: GetScanImgsRow[] }) {
    const parentRef = useRef(null);

    const rowVirtualizer = useVirtualizer({
        count: items.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 150,
        overscan: 5,
        gap: 35,
    });

    const columnVirtualizer = useVirtualizer({
        horizontal: true,
        count: 8,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 150,
        overscan: 5,
        gap: 35,
    });

    return (
        <>
            <div
                ref={parentRef}
                className="List"
                style={{
                    height: `750px`,
                    width: `1500px`,
                    overflow: "auto",
                }}
            >
                <div
                    style={{
                        height: `${rowVirtualizer.getTotalSize()}px`,
                        width: `${columnVirtualizer.getTotalSize()}px`,
                        position: "relative",
                    }}
                >
                    {rowVirtualizer.getVirtualItems().map((virtualRow) => (
                        <Fragment key={virtualRow.key}>
                            {columnVirtualizer.getVirtualItems().map((virtualColumn) => (
                                <div
                                    key={virtualColumn.key}
                                    style={{
                                        position: "absolute",
                                        top: 0,
                                        left: 0,
                                        width: `${virtualColumn.size}px`,
                                        height: `${virtualRow.size}px`,
                                        transform: `translateX(${virtualColumn.start}px) translateY(${virtualRow.start}px)`,
                                    }}
                                >
                                    <div>
                                        {virtualRow.index % 5 == 0 ? (
                                            <div>
                                                <span>HEADER {virtualRow.index}</span>
                                            </div>
                                        ) : (
                                            <div>
                                                <img
                                                    src={'/thumbs/' + items[virtualRow.index].ThumbPath}
                                                    alt="test"
                                                    height={150}
                                                />
                                            </div>
                                        )}
                                        {/* Cell {virtualRow.index}, {virtualColumn.index} */}
                                    </div>
                                </div>
                            ))}
                        </Fragment>
                    ))}
                </div>
            </div>
        </>
    );
}

export default GridVirtualizerFixed;
