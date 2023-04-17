import React from "react";
import "./style/OurPlans.css"
import {useNavigate, useLocation} from "react-router-dom";
import axios from "axios";

const plans = [
    {
        id: 1,
        name: "Basic Plan",
        price: "9.99₪",
        minutes: 10,
        features: ["50 mb/hour", "24/7 support"],
    },
    {
        id: 2,
        name: "Pro Plan",
        price: "19.99₪",
        minutes: 30,
        features: ["100 mb/hour", "24/7 support"],
    },
    {
        id: 3,
        name: "Premium Plan",
        price: "29.99₪",
        minutes: 60,
        features: ["200 mb/hour", "24/7 support"],
    },
];

const OurPlans = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const handleClick = (param) => {
        const confirmed = window.confirm('Are you sure you want to proceed?');


        if (confirmed) {
            axios.post('http://18.200.177.9:8080/wifi_session/start' , {
                "email": location.state.mail,
                "end_time_in_min": plans[param+1].minutes,

            })
            navigate("/countdown")
        }

    };
    return (
        <div className="plans-container">
            <h1>Our Plans</h1>
            <div className="plan-cards">
                {plans.map((plan) => (
                    <div className="plan-card" key={plan.id}>
                        <h2>{plan.name}</h2>
                        <h3>{plan.price}</h3>
                        <ul>
                            {plan.features.map((feature, index) => (
                                <li key={index}>{feature}</li>
                            ))}
                        </ul>
                        <button onClick={() => handleClick(plan.id)}>Select Plan</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default OurPlans;