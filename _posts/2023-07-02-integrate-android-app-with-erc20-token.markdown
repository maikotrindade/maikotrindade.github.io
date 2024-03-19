---
published: false
title: Integrate your Android app with a ERC20 smart contract
layout: post
---

Ethereum is a decentralized, open-source blockchain platform that enables the creation of smart contracts and decentralized applications (dApps). ERC20 is a standard for fungible tokens on the Ethereum blockchain. In this blog post, I will guide you through the process of creating a GraphQL(it could Rest too 🤷) app that connects with Ethereum networking to communicate with ERC20 tokens.

**Step 1: Setting up the Development Environment**
Before we begin, make sure you have the following tools installed:
Node.js and npm (Node Package Manager)
A code editor or IDE (Integrated Development Environment) such as Visual Studio Code or IntelliJ IDEA
A web3 library for JavaScript, such as Web3.js or ethers.js

**Step 2: Creating a GraphQL Schema**
A GraphQL schema is a definition of the types of data that can be queried and the relationships between them. To create a GraphQL schema for our app, we will use the GraphQL schema language.

```
`type Query {
  token(id: ID!): Token
}

type Token {
  id: ID!
  name: String!
  symbol: String!
  totalSupply: Int!
  balanceOf(address: String!): Int!
}`
```

In this schema, we have defined a Query type that has a single field called token. The token field takes an id argument of type ID!, which means that it is a required field. The token field returns a Token type, which has several fields: id, name, symbol, totalSupply, and balanceOf. The balanceOf field takes an address argument of type `String!`, which means that it is a required field.

**Step 3: Creating a GraphQL Resolver**
A GraphQL resolver is a function that is called when a query is executed. The resolver is responsible for fetching the data for the query and returning it in the correct format. To create a GraphQL resolver for our app, we will use the graphql-tools library.

```
const { graphqlHTTP } = require('express-graphql');
const { buildSchema } = require('graphql');

const schema = buildSchema(`
  type Query {
    token(id: ID!): Token
  }

  type Token {
    id: ID!
    name: String!
    symbol: String!
    totalSupply: Int!
    balanceOf(address: String!): Int!
  }
`);

const rootValue = {
  token: async (parent, { id }) => {
    const token = await getToken(id);
    return token;
  },
};

const app = express();
app.use('/graphql', graphqlHTTP({
  schema: schema,
  rootValue: rootValue,
  graphiql: true,
}));

app.listen(4000, () => {
  console.log('GraphQL server running on port 4000');
});
```
In this code, we have defined a schema object that contains our GraphQL schema. We have also defined a rootValue object that contains the resolver functions for our schema. The token resolver function takes an id argument and returns a Token object.

**Step 4: Connecting to Ethereum Networking**
To connect to the Ethereum network, we will use the web3 library.
const Web3 = require('web3');

const web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'));

In this code, we have created a new Web3 object and passed it a HttpProvider object that connects to the Ethereum mainnet through Infura/Alchemy.

**Step 5: Querying ERC20 Tokens**
To query ERC20 tokens, we will use the web3.eth.getToken method.
const token = await web3.eth.getToken(tokenAddress);

In this code, we have called the getToken method on the web3.eth object and passed it the address of the ERC20 token we want to query.

**Step 6: Returning the Token Data**
Once we have queried the ERC20 token, we can return the data to the client.
```
return {
  id: token.id,
  name: token.name,
  symbol: token.symbol,
  totalSupply: token.totalSupply,
  balanceOf: token.balanceOf,
};
```
In this code, we have returned an object that contains the id, name, symbol, totalSupply, and balanceOf fields of the ERC20 token.

**Conclusion**
In this blog post, we have covered the basics of creating a GraphQL app that connects with Ethereum networking to communicate with ERC20 tokens. We have learned how to create a GraphQL schema, create a GraphQL resolver, connect to Ethereum networking, query ERC20 tokens, and return the token data to the client. With this knowledge, you can build your own GraphQL app that interacts with the Ethereum blockchain.
