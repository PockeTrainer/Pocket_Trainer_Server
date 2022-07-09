import React, { Component, useEffect, useState} from 'react';
import { Link, useHistory } from 'react-router-dom';
import '../../css/Login/LoginPage.css';
import axios from "axios";
//import KaKaoLogin from 'react-kakao-login';

import { NAVER_AUTH_URL } from "./OAuth/naver";
import { KAKAO_AUTH_URL } from "./OAuth/kakao";

// const CLIENT_ID = "16b2ce1818782e53daf08293f620d814"
// const REDIRECT_URI = "http://127.0.0.1:3000"
// const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code`;

function LoginPage()  {

    const history = useHistory();

    let [id, changeId] = useState();
    let [password, changePassword] = useState();
    // let [code, changeCode] = useState(null);

    let server_url = 'http://ec2-15-164-217-95.ap-northeast-2.compute.amazonaws.com:8000'
    //let server_url = 'http://127.0.0.1:8000'

    //changeCode(new URL(window.location.href).searchParams.get("code"));
    const code = new URL(window.location.href).searchParams.get("code")
    const state = new URL(window.location.href).searchParams.get("state")

    useEffect(() => {
        //네이버 로그인
        if (code != null & state != null) {
            console.log('naver')
            axios.get(`http://127.0.0.1:8000/user/naver/login/${code}/${state}`)
                .then(res => {
                    console.log(res)
                })
                .catch(err => console.log(err))
        }
        //카카오 로그인
        else if (code != null) {
            console.log('kakao')
            axios.get(`http://127.0.0.1:8000/user/kakao/login/${code}`)
                .then(res => {
                    console.log(res)
                })
                .catch(err => console.log(err))
        }
    })
    

    const LogInBTNClick = (e) => {
        e.preventDefault();
        axios.post(`${server_url}/api/user/login`, {
            id : id,
            password : password
        })
        .then(res => {
            console.log(res.data);
            console.log(res.data.Token);
            axios.defaults.headers.common['Authorization'] = `token ${res.data.Token}`
            //sessionStorage.setItem("isAuthorized", "true");
            console.log(res.data.User.id);
            sessionStorage.setItem("user_id", res.data.User.id);
            history.push('/OnBoarding/BodyInfoPage');
        })
        .catch(err =>
            console.log(err.response.data)
        )

    }
    //http://127.0.0.1:8000/api/user/kakao/login
    // const kakaoLoginBTNClick = (e) => {
    //     e.preventDefault();
    //     axios.get(`https://kauth.kakao.com/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=code`)
    //         .then(res => {
    //             console.log(res.data);
    //         })
    //         .catch(err => 
    //             console.log(err.response.data)
    //         )

        
    // }
    // const [name, setName] = useState();

    // useEffect(() => {
    //     fetch("http://127.0.0.1:8000/api/user/")
    //         .then(res => {
    //             return res.json();
    //         })
    //         .then(data => {
    //             console.log(data[0].title)
    //             setName(data[0].title);
    //         });
    // }, []);

    // axios.post("http://127.0.0.1:8000/api/workout/pushUp/2")
    // .then(res => {
    //     console.log(res.data)
    // })
    // .catch(err => 
    //     console.log(err)
    // )


    return (
    <div className="LoginPage">
        <div className="GNB">로그인</div>

        <div className="mainsource">
            <div className="form">
                <form action="" >
                    <label htmlFor="id">아이디</label>
                    <input type="text" name="id" id="id" onChange={(e) => {
                        changeId(e.target.value);
                    }}/>
                    
                    <label htmlFor="pw">비밀번호</label>
                    <input type="password" name="pw" id="pw" onChange={(e) => {
                        changePassword(e.target.value);
                    }}/>
                    
                    <button onClick={LogInBTNClick}>로그인</button>
                    {/* <KaKaoLogin
                        token={'15c5be885755bb8706b92097f4bf3049'}
                        onSuccess={(data) => {
                            console.log("로그인성공", data);
                        }} 
                        onFail={(err) => {
                          console.log("로그인실패", err);
                        }}
                        onLogout={() => {
                          console.log("로그아웃");
                        }}
                    ></KaKaoLogin> */}
                    <a href={NAVER_AUTH_URL}>네이버 로그인</a>
                    <a href={KAKAO_AUTH_URL}>카카오 로그인</a>
                </form>
            </div>

            <div className="changePage">
                <div className="upLine">
                    <Link to="/Login/IdSearchPage">아이디 찾기</Link>
                    <Link to="/Login/PwSearchPage">비밀번호 찾기</Link>
                </div>
                <div className="downLine">
                    <Link to="/Login/SignUpPage">회원가입</Link>
                </div>
            </div>
        </div>

        <div className="buttons">
            <Link to="/OnBoarding/BodyInfoPage"><button>onBoarding 이동</button></Link>
            <Link to="/Main/MainPage"><button>main 이동</button></Link>
            <Link to="/History/HistoryPage"><button>history 이동</button></Link>
            <Link to="/MyPage/CheckPwPage"><button>mypage 이동</button></Link>
        </div>

    </div>
    );
}

export default LoginPage;