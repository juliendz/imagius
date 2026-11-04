import Sidebar from "./Sidebar";
import { AppShell, Burger } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
// import ThumbView from "./components/ThumbView";

import './App.css';
// import { Activity, useState } from "react";
import ImageView from "./components/ImageView";

function App() {
    const [opened, { toggle }] = useDisclosure();
    // const [showThumbView, setShowThumbView] = useState<boolean>(false);
    // const [showImgView, setShowImgView] = useState<boolean>(true);
    // const [imgId, setImgId] = useState<number>(0);

    // const viewImage = (id: number) => {
    //     setImgId(id);
    //     setShowThumbView(false);
    //     setShowImgView(true);
    // };

    // const viewThumbs = () => {
    //     setImgId(0)
    //     setShowThumbView(true);
    //     setShowImgView(false);
    // };

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
                {/* <Activity mode={showThumbView ? "visible" : "hidden"}>
                    <ThumbView />
                </Activity> */}
                {/* {showImgView && ( */}
                <ImageView id={20} />
                {/* )} */}

            </AppShell.Main>
        </AppShell>
    );
}
export default App;