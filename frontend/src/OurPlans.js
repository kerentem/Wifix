import React from "react";
import "./OurPlans.css"
const plans = [
    {
        id: 1,
        name: "Basic Plan",
        price: "9.99₪",
        features: ["50 mb/hour", "24/7 support"],
    },
    {
        id: 2,
        name: "Pro Plan",
        price: "19.99₪",
        features: ["100 mb/hour", "24/7 support"],
    },
    {
        id: 3,
        name: "Premium Plan",
        price: "29.99₪",
        features: ["200 mb/hour", "24/7 support"],
    },
];

const OurPlans = () => {
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
                        <button>Select Plan</button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default OurPlans;