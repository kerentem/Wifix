import React, { useEffect, useState } from 'react';
import axios from "axios";
import './style/Countdown.css';
import {useLocation, useNavigate} from "react-router-dom";

function CountdownTimer() {
    const navigate = useNavigate();
    const location = useLocation();

    const [targetTime, setTargetTime] = useState(1683805593);
    const [countdown, setCountdown] = useState('Loading...');



    useEffect(() => {
        const mail = location.state.mail
        const response = axios.get('http://18.200.177.9:8080/wifi_session/time_left', {
            params: {
                "email": mail ,
                "company_name": "bar_test"
            }
        })
            .then((response) => {
                if(response.data.error)
                    navigate("/menu", { mail });
            })

        const targetTime = response.data.data["end_session_time_timestamp"];
        setTargetTime(targetTime);

        console.log(targetTime)
        if (targetTime) {
            const intervalId = setInterval(() => {
                const now = new Date().getTime() / 1000;
                console.log(now)
                const timeRemaining = Math.abs(targetTime - now);
                console.log(timeRemaining)
                if (timeRemaining < 0) {
                    clearInterval(intervalId);
                    setCountdown('Countdown finished!');
                    navigate("/menu");
                } else {
                    const hours = Math.floor(timeRemaining / 3600);
                    const minutes = Math.floor((timeRemaining % 3600) / 60);
                    const seconds = Math.floor(timeRemaining % 60);

                    setCountdown(
                        <div>
                            <h1>Time left for wifi session:</h1>
                        <div id="countdown">
                            <span className="count">{hours}</span>
                            <span className="divider">:</span>
                            <span className="count">{minutes}</span>
                            <span className="divider">:</span>
                            <span className="count">{seconds}</span>
                        </div>
                        </div>
                    );
                }
            }, 1000);

            return () => clearInterval(intervalId);
        }
    }, [targetTime]);

    return <div className="timer-container">{countdown}</div>;
}

export default CountdownTimer;
