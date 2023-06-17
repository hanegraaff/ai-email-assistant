const express = require('express');
const app = express();
const { renderToString } = require('react-dom/server');
const React = require('react');


const HelloWorld = () => {
  return React.createElement(
    'div',
    null,
    React.createElement('h1', { id: 'message' }, 'Hello, World!'),
    React.createElement(
      'button',
      {
        onClick: `document.getElementById('message').innerText = Math.random().toString(36).substring(7);`,
      },
      "Don't press me"
    )
  );
};

app.get('/', (req, res) => {
  const html = renderToString(React.createElement(HelloWorld));
  res.send(`<!DOCTYPE html>
    <html>
    <head>
        <title>Hello, World!</title>
    </head>
    <body>
        <div id="root">${html}</div>
    </body>
    </html>`);
    });

module.exports = app;