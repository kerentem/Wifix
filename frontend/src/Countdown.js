import React, { useEffect, useState } from 'react';
import './style/Countdown.css';
import {useNavigate} from "react-router-dom";

function CountdownTimer() {
    const navigate = useNavigate();
    const [targetTime, setTargetTime] = useState(null);
    const [countdown, setCountdown] = useState('Loading...');

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('https://example.com/target-time');
            const targetTime = new Date(await response.text());
            setTargetTime(targetTime);
        };

        fetchData();
    }, []);

    useEffect(() => {
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
