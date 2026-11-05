import { List, ThemeIcon } from '@mantine/core';
import { CheckCircleIcon } from '@phosphor-icons/react';
import { useEffect, useState } from 'react';
import { LibraryService, ScanDir } from '../../bindings/julien/imagius-go/internal';
import { useAppDispatch } from '../hooks';
import { ScrollToDir } from '../appStore';

function FolderList() {
    const dispatch = useAppDispatch();
    const [folders, setFolders] = useState<ScanDir[]>();

    useEffect(() => {
        (async () => {
            let folders = await LibraryService.GetDirs();
            console.log(folders);
            setFolders(folders!);
        })();
    }, []);

    const handleDirClicked = (dirIndex: number) => {
        console.log('Scroll to dir index:', dirIndex);
        dispatch(ScrollToDir(dirIndex));
    }


    return (
        <List
            spacing="xs"
            size="sm"
            center
            icon={
                <ThemeIcon color="teal" size={24} radius="xl">
                    <CheckCircleIcon size={16} />
                </ThemeIcon>
            }
        >
            {folders?.map((folder, index) => (
                <List.Item key={folder.ID} onClick={() => handleDirClicked(index)}>{folder.Name}</List.Item>
            ))}
        </List>
    );
}
export default FolderList;