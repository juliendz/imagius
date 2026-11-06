import { Accordion, List, ThemeIcon } from '@mantine/core';
import { CheckCircleIcon } from '@phosphor-icons/react';
import { useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { ScrollToDir } from '../../appStore';
import classes from './FolderList.module.css';

function RecentSection({ sectionId, sectionName }: { sectionId: number, sectionName: string }) {
    const dispatch = useAppDispatch();
    const [selectedIndex, setSelectedIndex] = useState<number | null>(0);
    const recentDirs = useAppSelector(state => state.appStore.library.Recent);

    const handleDirClicked = (dirIndex: number, thumbViewIndex: number) => {
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
                    {recentDirs?.map((recentDir, rIndex) => (
                        <List.Item key={recentDir?.ID}
                            className={`${selectedIndex === rIndex ? classes['dir-list-item-selected'] : ''}`}
                            onClick={() => handleDirClicked(rIndex, recentDir?.ThumbViewIndex ?? 0)}>{recentDir?.Name}</List.Item>
                    ))}
                </List>
            </Accordion.Panel>
        </Accordion.Item>

    );
}
export default RecentSection;