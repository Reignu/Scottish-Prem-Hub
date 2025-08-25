import './App.css';
import {useEffect} from "react";
import { Route, Routes } from "react-router-dom";

function App() {
    useEffect(() => {
        document.title = "PremierHub Zone"
    }, []);
    return (
        <>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Home />} />
                </Route>
            </Routes>
        </>

    );
}

export default App;
