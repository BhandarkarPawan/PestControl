import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import reportWebVitals from './reportWebVitals';

import { ApolloClient, ApolloProvider, InMemoryCache } from '@apollo/client';
import Routes from './routes';

const graphQLUri = 'http://192.168.29.170:5000/graphql';

const apolloClient = new ApolloClient({
  uri: graphQLUri,
  credentials: 'same-origin',
  cache: new InMemoryCache(),
});

ReactDOM.render(
  <ApolloProvider client={apolloClient}>
    <Routes />
  </ApolloProvider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
