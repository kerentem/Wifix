import React, { useEffect, useState } from 'react';
import axios from "axios";
import './style/Countdown.css';
import {useLocation, useNavigate} from "react-router-dom";

function CountdownTimer() {
    const navigate = useNavigate();
    const location = useLocation();

    const [targetTime, setTargetTime] = useState(null);
    const [countdown, setCountdown] = useState('Loading...');

    useEffect(() => {
        const fetchData = async () => {
            const response = await axios.get('http://18.200.177.9:8080/wifi_session/time_left', {
                params: {
                    "email": location.state.mail,
                    "company_name": "bar_test"
                }
            });
            const targetTime = new Date(response.data["end_session_time_timestamp"]);
            setTargetTime(targetTime);
        };

        fetchData();
    }, []);

    useEffect(() => {
        console.log(targetTime)
        if (targetTime) {
            const intervalId = setInterval(() => {
                const now = new Date();
                const timeRemaining = targetTime - now;

                if (timeRemaining < 0) {
                    clearInterval(intervalId);
                    setCountdown('Countdown finished!');
                    navigate("/menu");
                } else {
                    const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

                    setCountdown(
                        <div>
                            <h1>Time left for wifi session:</h1>
                        <div id="countdown">
                            <span className="count">{days}</span>
                            <span className="divider">:</span>
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
