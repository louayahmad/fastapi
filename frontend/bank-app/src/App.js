import React from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import GetBankAccounts from "./GetBankAccounts";
import Login from "./Login";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/protected" element={<GetBankAccounts />} />
      </Routes>
    </Router>
  );
};

export default App;
