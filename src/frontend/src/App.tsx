import Sidebar from "./Sidebar";
import { AppShell, Burger } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import ImageView from "./components/ImageView";
import { useAppSelector } from "./hooks";
import ThumbView from "./components/ThumbView";

import './App.css';
import { Activity } from "react";
// import { Activity, useState } from "react";

function App() {
    const showThumbView = useAppSelector(state => state.appStore.showThumbView);
    const showImageView = useAppSelector(state => state.appStore.showImageView);
    const imgId = useAppSelector(state => state.appStore.imgId);
    const [opened, { toggle }] = useDisclosure();


    return (
        <AppShell
            padding="md"
            header={{ height: 60 }}
            navbar={{
                width: 300,
                breakpoint: 'sm',
                collapsed: { mobile: !opened },
            }}
        >
            <AppShell.Header>
                <Burger
                    opened={opened}
                    onClick={toggle}
                    hiddenFrom="sm"
                    size="sm"
                />

                <div>Logo</div>
            </AppShell.Header>

            <AppShell.Navbar>
                <Sidebar />
            </AppShell.Navbar>

            <AppShell.Main>
                <Activity mode={showThumbView ? "visible" : "hidden"}>
                    <ThumbView />
                </Activity>
                {showImageView && (
                    <ImageView id={imgId} />
                )}

            </AppShell.Main>
        </AppShell>
    );
}
export default App;