import React, {useEffect, useState} from "react"
import axios from "axios";
import logo from "./style/logo-no-background.png";
import "./App.css"
import { useNavigate } from "react-router-dom";


export default function (props) {
    let [authMode, setAuthMode] = useState("signin")
    let [name, setName] = useState();
    let [mail, setMail] = useState();
    let [password, setPassword] = useState();
    const [ip, setIP] = useState();
    const navigate = useNavigate();

    const getData = async () => {
        const res = await axios.get("http://192.168.0.100:9285/user_ip");
        console.log(res.data);
        setIP(res.data.ip);
    };

    useEffect(() => {
        getData();
    }, []);

    const changeAuthMode = () => {
        setAuthMode(authMode === "signin" ? "signup" : "signin")
    }
    const submitSignIn =  (event) => {
        event.preventDefault();
        axios.post('http://18.200.177.9:8080/login' , {
            "password": password,
            "email": mail,
            "company_name": "bar_test",
            "ip": ip
        })
            .then( (response) => {
                if(response.data.error) {
                    const popup = document.getElementById("myPopup");
                    popup.classList.toggle("show");
                    setTimeout(() => {popup.classList.toggle("show");}, 3000);
                }
                else
                    navigate(`/menu`, { state: { mail, ip }});
            });
    }

    const submitSignUp = (event) => {
        event.preventDefault();
         axios.post('http://18.200.177.9:8080/register' , {
            "full_name": name,
            "password": password,
            "email": mail,
             "company_name": "bar_test",
             "ip": ip
        })
             .then( (response) => {
                 if(response.data.error) {
                     const popup = document.getElementById("myPopup");
                     popup.classList.toggle("show");
                     setTimeout(() => {popup.classList.toggle("show");}, 3000);
                 }
                 else
                     navigate(`/menu`, { state: { mail,ip }});
             });
    }

    if (authMode === "signin") {
        return (

            <div className="Auth-form-container">
                <img src={logo}/>
                <form className="Auth-form" onSubmit={submitSignIn}>
                    <div className="Auth-form-content">
                        <h3 className="Auth-form-title">Sign In</h3>
                        <div className="text-center">
                            Not registered yet?{" "}
                            <span className="link-primary" onClick={changeAuthMode}>
                Sign Up
              </span>
                        </div>
                        <div className="form-group mt-3">
                            <label>Email address</label>
                            <input
                                type="email"
                                className="form-control mt-1"
                                placeholder="Enter email"
                                onChange={e => setMail(e.target.value)}
                            />
                        </div>
                        <div className="form-group mt-3">
                            <label>Password</label>
                            <input
                                type="password"
                                className="form-control mt-1"
                                placeholder="Enter password"
                                onChange={e => setPassword(e.target.value)}
                            />
                        </div>
                        <div className="d-grid gap-2 mt-3">
                            <div className="popup">
                                <span className="popuptext" id="myPopup">פרטי התחברות לא נכונים</span>
                            </div>
                            <button type="submit" className="btn btn-primary">
                                Submit
                            </button>
                        </div>
                        <p className="text-center mt-2">
                            Forgot <a href="#">password?</a>
                        </p>
                    </div>
                </form>
            </div>
        )
    }

    else return (
        <div className="Auth-form-container">
            <img src={logo}/>
            <form className="Auth-form" onSubmit={submitSignUp}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">Sign Up</h3>
                    <div className="text-center">
                        Already registered?{" "}
                        <span className="link-primary" onClick={changeAuthMode}>
              Sign In
            </span>
                    </div>
                    <div className="form-group mt-3">
                        <label>Full Name</label>
                        <input
                            type="text"
                            className="form-control mt-1"
                            placeholder="e.g Israel Israeli"
                            onChange={e => setName(e.target.value)}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Email address</label>
                        <input
                            type="email"
                            className="form-control mt-1"
                            placeholder="Email Address"
                            onChange={e => setMail(e.target.value)}//TODO
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Password</label>
                        <input
                            type="password"
                            className="form-control mt-1"
                            placeholder="Password"
                            onChange={e => setPassword(e.target.value)}
                        />
                    </div>
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary">
                            Submit
                        </button>
                        <div className="popup">
                            <span className="popuptext" id="myPopup">ססמא חלשה מידי-אותיות ומספרים מעל 8 תווים</span>
                        </div>
                    </div>
                    <p className="text-center mt-2">
                        Forgot <a href="#">password?</a>
                    </p>
                </div>
            </form>
        </div>
    )
}
