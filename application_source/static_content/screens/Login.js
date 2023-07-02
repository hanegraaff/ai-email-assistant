import React, { useState, useEffect } from 'react';
import { View, Text, Linking, TouchableOpacity, StyleSheet, TextInput } from 'react-native';

const Login = () => {
  const [result, setResult] = useState('');
  const [banner, setBanner] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const callApi = async () => {
    const response = await fetch('https://api-prod.hal-9001.com/test-data');
    const data = await response.json();
    setResult(JSON.stringify(data, null, 2));
  }

  useEffect(() => {
    const messages = ["Beware", "Go Away", "You shouldn't be here", "System Failure", "Don't do this", "It's all your fault", "You will regret it"];
    const bannerMessage = messages[Math.floor(Math.random() * messages.length)];
    setBanner(bannerMessage);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.banner} onPress={callApi}>{banner}</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Username"
        placeholderTextColor="rgba(120, 0, 0, 1)"
        value={username}
        onChangeText={setUsername}
      />
      
      <TextInput
        style={styles.input}
        placeholder="Password"
        placeholderTextColor="rgba(120, 0, 0, 1)"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <View style={styles.googleLogin}>
        <TouchableOpacity onPress={() => Linking.openURL('https://accounts.google.com/o/oauth2/v2/auth?client_id=CLIENT_ID&redirect_uri=https://localhost:80&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile&access_type=offline&prompt=consent')}>
          <Text style={styles.link}>Google Login</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.results}>{result}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'black',
  },
  banner: {
    fontSize: 50,
    color: 'rgba(120, 0, 0, 0.3)', // Darker color
    textAlign: 'center',
    fontFamily: 'Futura-CondensedExtraBold',
  },
  input: {
    width: '10%',
    height: 30, // narrow height
    borderColor: 'rgba(120, 0, 0, 1)',
    borderWidth: 1,
    borderRadius: 10,
    color: 'rgba(120, 0, 0, 1)',
    textAlign: 'center',
    marginBottom: 10,
    fontFamily: 'Futura-CondensedExtraBold',
  },
  link: {
    color: 'rgba(120, 0, 0, 1)',
    textDecorationLine: 'none',
    margin: 10,
    textAlign: 'center',
  },
  googleLogin: {
    marginTop: 20,
  },
  results: {
    marginTop: 20,
    color: 'white',
    textAlign: 'center',
  }
});

export default Login;
