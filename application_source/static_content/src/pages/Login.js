import React, { useState, useEffect } from 'react';
import '../App.css';
import { CognitoUser, AuthenticationDetails, CognitoUserPool } from 'amazon-cognito-identity-js';

const poolData = {
    UserPoolId: 'us-east-1_E2R4JQcVO',
    ClientId: '1ganb7hdr06q3l2uu5nrk9kj18'
};
const userPool = new CognitoUserPool(poolData);

const LoginPage = () => {
    const [result, setResult] = useState('');
    const [banner, setBanner] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [newPasswordRequired, setNewPasswordRequired] = useState(false);
    const [cognitoUser, setCognitoUser] = useState(null);

    const callApi = async () => {
        setResult('')
        var authenticationData = {
            Username: username,
            Password: password,
        };
        var authenticationDetails = new AuthenticationDetails(authenticationData);
        var userData = {
            Username: username,
            Pool: userPool,
        };

        var user = new CognitoUser(userData);
        setCognitoUser(user);
        user.authenticateUser(authenticationDetails, {
            onSuccess: function (result) {
                var accessToken = result.getAccessToken().getJwtToken();
                setResult(JSON.stringify(result, null, 2));
                setNewPasswordRequired(false);
            },
            onFailure: function (err) {
                if (err.code === 'PasswordResetRequiredException') {
                    setNewPasswordRequired(true);
                    setResult("Your password has expired. Please set a new password.");
                } else {
                    setResult(err.message);
                }
            },

            newPasswordRequired: function (userAttributes, requiredAttributes) {
                // Prompt the user for a new password
                setNewPasswordRequired(true);
            }

        });
    }

    const changePassword = async () => {
        if (!cognitoUser || !newPassword) {
            return;
        }
        setNewPasswordRequired(false);

        cognitoUser.completeNewPasswordChallenge(newPassword, [], {
            onSuccess: function (result) {
                setResult('Password has been changed successfully.');
            },
            onFailure: function (err) {
                setResult(err.message);
            }
        });
    };


    useEffect(() => {
        const messages = ["Beware", "Go Away", "You shouldn't be here", "System Failure", "Don't do this", "It's all your fault", "You will regret it"];
        const bannerMessage = messages[Math.floor(Math.random() * messages.length)];
        setBanner(bannerMessage);
    }, []);

    return (
        <div className="container">
            <div className="banner" onClick={callApi}>{banner}</div>

            <input
                className="input"
                placeholder="Username"
                style={{ color: 'rgba(120, 0, 0, 1)' }}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <input
                className="input"
                placeholder="Password"
                style={{ color: 'rgba(120, 0, 0, 1)' }}
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            {newPasswordRequired && (
                <>
                    <input
                        className="input"
                        placeholder="New Password"
                        style={{ color: 'rgba(120, 0, 0, 1)' }}
                        type="password"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                    />
                    <button className="change-password-button" onClick={changePassword}>Change Password</button>
                </>
            )}

            <div className="results">{result}</div>
        </div>
    );
}

export default LoginPage;