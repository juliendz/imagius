import { useEffect, useState } from "react";
import { LibraryService, ScanImg } from "../../bindings/julien/imagius-go/internal";
import { AspectRatio, Button, Group, Stack } from "@mantine/core";
import { useAppDispatch } from "../hooks";
import { ShowThumbsView } from "../appStore";

function ImageView({ id }: { id: number }) {
    const dispatch = useAppDispatch();
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

    const handleClickBack = () => {
        dispatch(ShowThumbsView());
    };

    return (
        <Stack
            bg="var(--mantine-color-body)"
            align="stretch"
            justify="center"
            gap="md"
        >
            <Group>
                <Button variant="default" onClick={handleClickBack}>Back</Button>
            </Group>
            <AspectRatio mx="0">
                <img
                    src={img?.AbsPath ? '/img?id=' + img?.ID : '/missing-thumb.png'}
                    alt={img?.Name ?? ""}
                    loading="lazy"
                    style={{
                        objectFit: "contain",
                    }}
                />
            </AspectRatio>
        </Stack>

    );
}

export default ImageView;   