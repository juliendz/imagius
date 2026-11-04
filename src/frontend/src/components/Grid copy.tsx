// import { useVirtualizer } from "@tanstack/react-virtual";
// import { Fragment, useRef } from "react";
// import type { GetScanImgsRow } from "../../bindings/julien/imagius-go/internal";

// function GridVirtualizerFixed({ items, colcount }: { items: GetScanImgsRow[], colcount: number }) {
//     const parentRef = useRef(null);

//     const rowVirtualizer = useVirtualizer({
//         count: Math.ceil(items.length / colcount),
//         getScrollElement: () => parentRef.current,
//         estimateSize: () => 150,
//         overscan: 5,
//         gap: 35,
//     });

//     const columnVirtualizer = useVirtualizer({
//         horizontal: true,
//         count: colcount,
//         getScrollElement: () => parentRef.current,
//         estimateSize: () => 150,
//         overscan: 5,
//         gap: 35,
//     });

//     return (
//         <>
//             <div
//                 ref={parentRef}
//                 className="List"
//                 style={{
//                     height: `750px`,
//                     width: `1500px`,
//                     overflow: "auto",
//                 }}
//             >
//                 <div
//                     style={{
//                         height: `${rowVirtualizer.getTotalSize()}px`,
//                         width: `${columnVirtualizer.getTotalSize()}px`,
//                         position: "relative",
//                     }}
//                 >
//                     {rowVirtualizer.getVirtualItems().map((virtualRow) => (
//                         <Fragment key={virtualRow.key}>
//                             {columnVirtualizer.getVirtualItems().map((virtualColumn) => (
//                                 <div
//                                     key={virtualColumn.key}
//                                     style={{
//                                         position: "absolute",
//                                         top: 0,
//                                         left: 0,
//                                         width: `${virtualColumn.size}px`,
//                                         height: `${virtualRow.size}px`,
//                                         transform: `translateX(${virtualColumn.start}px) translateY(${virtualRow.start}px)`,
//                                     }}
//                                 >
//                                     <div>
//                                         <div>
//                                             <img src={'/thumbs/' + items[virtualColumn.index].ThumbPath}
//                                                 alt={items[virtualColumn.index].Name}
//                                                 height={150}
//                                             />
//                                         </div>
//                                     </div>
//                                 </div>
//                             ))}
//                         </Fragment>
//                     ))}
//                 </div>
//             </div>
//         </>
//     );
// }

// export default GridVirtualizerFixed;
