import "bootstrap/dist/css/bootstrap.min.css"
import "./App.css"
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Auth from "./Auth"
import OurPlans from "./OurPlans";
import CountdownTimer from "./Countdown";
import ManagerScreen from "./Manager";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Auth />} />
                <Route path="/menu" element={<OurPlans/>} />
                <Route path="/countdown" element={<CountdownTimer/>} />
                <Route path="/manager" element={<ManagerScreen/>} />
                <Route path='*' element={<Navigate to='/' />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
