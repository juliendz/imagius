import { List, ThemeIcon } from '@mantine/core';
import { CheckCircleIcon } from '@phosphor-icons/react';
import { useState } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks';
import { ScrollToDir } from '../appStore';

function FolderList() {
    const dispatch = useAppDispatch();
    const [selectedIndex, setSelectedIndex] = useState<number | null>(0);
    const folders = useAppSelector(state => state.appStore.library.Dirs);

    const handleDirClicked = (dirIndex: number) => {
        // console.log('Scroll to dir index:', dirIndex);
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
                <List.Item key={folder?.ID}
                    style={{ padding: '0px 5px' }}
                    className={`${selectedIndex === index ? 'dir-list-item-selected' : ''}`}
                    onClick={() => handleDirClicked(folder?.ThumbViewIndex ?? 0)}>{folder?.Name}</List.Item>
            ))}
        </List>
    );
}
export default FolderList;