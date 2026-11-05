import Sidebar from "./Sidebar";
import { AppShell, Burger } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import ImageView from "./components/ImageView";
import { useAppSelector } from "./hooks";
import ThumbView from "./components/ThumbView";

import './App.css';
import { Activity } from "react";
import SlideShowView from "./components/SlideShowView";
// import { Activity, useState } from "react";

function App() {
    const currView = useAppSelector(state => state.appStore.currentView);
    const imgId = useAppSelector(state => state.appStore.imgId);
    const slideShowDirId = useAppSelector(state => state.appStore.slideShowDirId);
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
                <Activity mode={currView == 'thumbs' ? "visible" : "hidden"}>
                    <ThumbView />
                </Activity>
                {currView == 'image' && (
                    <ImageView id={imgId} />
                )}
                {currView == 'slideshow' && (
                    <SlideShowView dirId={slideShowDirId} sortBy="modified_time" startImgIdx={0} />
                )}

            </AppShell.Main>
        </AppShell>
    );
}
export default App;