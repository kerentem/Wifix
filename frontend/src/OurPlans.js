import React, {useEffect, useState} from "react";
import "./style/OurPlans.css"
import {useNavigate, useLocation} from "react-router-dom";
import axios from "axios";


let plans;

const OurPlans = () => {
    const [ip, setIP] = useState();
    const navigate = useNavigate();
    const location = useLocation();

    const getData = async () => {
        const res = await axios.get("http://192.168.0.100:9285/user_ip");
        console.log(res.data);
        setIP(res.data.ip);
        const basic_price = await axios.get("http://192.168.0.100:9285/price?plan=basic");
        const premium_price = await axios.get("http://192.168.0.100:9285/price?plan=premium")
        const business_price = await axios.get("http://192.168.0.100:9285/price?plan=business");
        plans = [
    {
        id: 1,
        name: "Basic Plan",
        price: basic_price,
        minutes: 10,
        features: ["50 mb/hour", "24/7 support"],
    },
    {
        id: 2,
        name: "Premium Plan",
        price: premium_price,
        minutes: 30,
        features: ["100 mb/hour", "24/7 support"],
    },
    {
        id: 3,
        name: "Business Plan",
        price: business_price,
        minutes: 60,
        features: ["200 mb/hour", "24/7 support"],
    },
];
    };


    useEffect(() => {
        getData();
    }, []);

    const handleClick = async (param) => {

        const confirmed = window.confirm('Are you sure you want to proceed?');
        const mail = location.state.mail;

        if (confirmed) {
            console.log(ip)
            axios.post('http://18.200.177.9:8080/wifi_session/start', {
                 "email": mail,
                 "end_time_in_min": plans[param - 1].minutes,
                 "price": plans[param - 1].price,
                 "ip": ip,
                 "company_name": "bar_test"
             })
                .then( (response) => {
                    navigate("/countdown", { state: { mail }})
                });
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
                        <button onClick={async () => await handleClick(plan.id)}>Select Plan</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default OurPlans;