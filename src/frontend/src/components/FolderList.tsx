import { List, ThemeIcon } from '@mantine/core';
import { CheckCircleIcon } from '@phosphor-icons/react';
import { useEffect, useState } from 'react';
import { LibraryService, ScanDir } from '../../bindings/julien/imagius-go/internal';
import { useAppDispatch } from '../hooks';
import { ScrollToDir } from '../appStore';

function FolderList() {
    const dispatch = useAppDispatch();
    const [folders, setFolders] = useState<ScanDir[]>();
    const [selectedIndex, setSelectedIndex] = useState<number | null>(0);

    useEffect(() => {
        (async () => {
            let folders = await LibraryService.GetDirs();
            console.log(folders);
            setFolders(folders!);
        })();
    }, []);

    const handleDirClicked = (dirIndex: number) => {
        console.log('Scroll to dir index:', dirIndex);
        setSelectedIndex(dirIndex);
        dispatch(ScrollToDir(dirIndex));
    }


    return (
        <List
            spacing="3"
            size="sm"
            center
            icon={
                <ThemeIcon color="teal" size={24} radius="xl">
                    <CheckCircleIcon size={16} />
                </ThemeIcon>
            }
        >
            {folders?.map((folder, index) => (
                <List.Item key={folder.ID}
                    style={{ padding: '0px 5px' }}
                    className={`${selectedIndex === index ? 'dir-list-item-selected' : ''}`}
                    onClick={() => handleDirClicked(index)}>{folder.Name}</List.Item>
            ))}
        </List>
    );
}
export default FolderList;