// import { useRef } from "react";
// import { useVirtualizer } from "@tanstack/react-virtual";
// import { GetScanImgsRow } from "../../bindings/julien/imagius-go/internal";

// // const ITEMS = Array.from({ length: 10000 }, (_, i) => ({
// //     id: i,
// //     title: `Thumbnail ${i + 1}`,
// //     image: `https://picsum.photos/seed/${i}/300/200`,
// // }));

// const COLUMN_WIDTH = 150;
// const ROW_HEIGHT = 150;
// const GAP = 12;

// export default function Grid({ items }: { items: GetScanImgsRow[] }) {
//     const parentRef = useRef<HTMLDivElement>(null);

//     const columns = Math.max(
//         1,
//         Math.floor((parentRef.current?.clientWidth ?? 900) / (COLUMN_WIDTH + GAP)),
//     );

//     const rowCount = Math.ceil(items.length / columns);

//     const rowVirtualizer = useVirtualizer({
//         count: rowCount,
//         getScrollElement: () => parentRef.current,
//         estimateSize: () => ROW_HEIGHT + GAP,
//         overscan: 3,
//     });

//     return (
//         <div
//             ref={parentRef}
//             style={{
//                 height: 750,
//                 width: "100%",
//                 overflow: "auto",
//             }}
//         >
//             <div
//                 style={{
//                     height: rowVirtualizer.getTotalSize(),
//                     position: "relative",
//                     width: "100%",
//                 }}
//             >
//                 {rowVirtualizer.getVirtualItems().map((row) => (
//                     <div
//                         key={row.key}
//                         style={{
//                             position: "absolute",
//                             top: 0,
//                             left: 0,
//                             width: "100%",
//                             height: ROW_HEIGHT,
//                             transform: `translateY(${row.start}px)`,
//                             display: "grid",
//                             gridTemplateColumns: `repeat(${columns}, ${COLUMN_WIDTH}px)`,
//                             gap: GAP,
//                         }}
//                     >
//                         {Array.from({ length: columns }, (_, col) => {
//                             const index = row.index * columns + col;
//                             const item = items[index];

//                             if (!item) return null;

//                             return (
//                                 <div
//                                     key={item.Key}
//                                     style={{
//                                         height: ROW_HEIGHT,
//                                         overflow: "hidden",
//                                         borderRadius: 8,
//                                         background: "#eee",
//                                     }}
//                                 >
//                                     <img
//                                         src={'/thumbs/' + item.ThumbPath}
//                                         alt={item.Name}
//                                         loading="lazy"
//                                         style={{
//                                             width: "100%",
//                                             height: 120,
//                                             objectFit: "contain",
//                                         }}
//                                     />
//                                     <div style={{ padding: 6 }}>{item.Name}</div>
//                                 </div>
//                             );
//                         })}
//                     </div>
//                 ))}
//             </div>
//         </div>
//     );
// }