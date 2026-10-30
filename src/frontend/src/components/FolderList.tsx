import { List, ThemeIcon } from '@mantine/core';
import { CheckCircleIcon } from '@phosphor-icons/react';
import { useEffect, useState } from 'react';
import { LibraryService, ScanDir } from '../../bindings/julien/imagius-go/internal';

function FolderList() {

    const [folders, setFolders] = useState<ScanDir[]>();

    useEffect(() => {
        (async () => {
            let folders = await LibraryService.GetDirs();
            console.log(folders);
            setFolders(folders!);
        })();
    }, []);


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
            {folders?.map((folder) => (
                <List.Item key={folder.ID}>{folder.Name}</List.Item>
            ))}
        </List>
    );
}
export default FolderList;