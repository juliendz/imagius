import { Accordion, List, ThemeIcon } from '@mantine/core';
import { CheckCircleIcon, PlusIcon } from '@phosphor-icons/react';
import { useState } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks';
import { ScrollToDir } from '../appStore';
import classes from '../css/FolderList.module.css';

function FolderList() {
    const dispatch = useAppDispatch();
    const [selectedIndex, setSelectedIndex] = useState<number | null>(0);
    const folders = useAppSelector(state => state.appStore.library.Dirs);

    const handleDirClicked = (dirIndex: number, thumbViewIndex: number) => {
        // console.log('Scroll to dir index:', dirIndex);
        setSelectedIndex(dirIndex);
        dispatch(ScrollToDir(thumbViewIndex));
    }

    const sections = [{ ID: 2, Name: 'Folders' }];

    const sectionItems = sections.map((section, index) => {
        if (section.ID == 2) {

            return (
                <Accordion.Item key={section.ID} value={section.Name}>
                    <Accordion.Control icon={<CheckCircleIcon size={16} />}>{section.Name}</Accordion.Control>
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
        return null;
    });

    return (
        <Accordion
            defaultValue={sections[0]?.Name}
            classNames={{ chevron: classes.chevron }}
            chevron={<PlusIcon className={classes.icon} />}
            order={3}
        >
            {sectionItems}
        </Accordion>

    );
}
export default FolderList;