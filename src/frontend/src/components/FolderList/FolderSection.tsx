import { Accordion, List, ThemeIcon } from '@mantine/core';
import { CheckCircleIcon } from '@phosphor-icons/react';
import { useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { ScrollToDir } from '../../appStore';
import { addRecentDir } from '../../thunk';
import classes from './FolderList.module.css';

function FolderSection({ sectionId, sectionName }: { sectionId: number, sectionName: string }) {
    const dispatch = useAppDispatch();
    const [selectedIndex, setSelectedIndex] = useState<number | null>(0);
    const folders = useAppSelector(state => state.appStore.library.Dirs);

    const handleDirClicked = (dirIndex: number, thumbViewIndex: number) => {
        dispatch(addRecentDir({ dirID: folders?.[dirIndex]?.ID ?? 0, dirIndex: dirIndex }))
        setSelectedIndex(dirIndex);
        dispatch(ScrollToDir(thumbViewIndex));
    }

    return (
        <Accordion.Item key={sectionId} value={sectionName}>
            <Accordion.Control icon={<CheckCircleIcon size={16} />}>{sectionName}</Accordion.Control>
            <Accordion.Panel>
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
                    {folders?.map((folder, fIndex) => (
                        <List.Item key={folder?.ID}
                            className={`${selectedIndex === fIndex ? classes['dir-list-item-selected'] : ''}`}
                            onClick={() => handleDirClicked(fIndex, folder?.ThumbViewIndex ?? 0)}>{folder?.Name}</List.Item>
                    ))}
                </List>

            </Accordion.Panel>
        </Accordion.Item>
    );
}
export default FolderSection;