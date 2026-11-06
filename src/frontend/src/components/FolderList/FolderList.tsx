import { Accordion } from '@mantine/core';
import { PlusIcon } from '@phosphor-icons/react';
import classes from './FolderList.module.css';
import RecentSection from './RecentSection';
import FolderSection from './FolderSection';

function FolderList() {

    const sections = [{ ID: 1, Name: 'Recent' }, { ID: 2, Name: 'Folders' }];

    const sectionItems = sections.map((section, index) => {
        if (section.ID == 1) {
            return (
                <RecentSection sectionId={section.ID} sectionName={section.Name} />
            );
        }
        if (section.ID == 2) {

            return (
                <FolderSection sectionId={section.ID} sectionName={section.Name} />
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