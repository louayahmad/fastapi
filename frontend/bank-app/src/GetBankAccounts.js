import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const GetBankAccounts = () => {
  const [bankAccounts, setBankAccounts] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const getUserBankAccounts = async () => {
      setError(null);

      const token = localStorage.getItem("token");

      try {
        const response = await fetch(
          "http://localhost:8000/get-all-user-accounts",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }

        const data = await response.json();
        setBankAccounts(data.accounts);
      } catch (error) {
        setError(error.message);
      }
    };

    getUserBankAccounts();
  }, []);

  const goToDepositPage = () => {
    navigate("/");
  };

  return (
    <div>
      <h2>Your Bank Accounts</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {bankAccounts.map((account, index) => (
          <li
            key={`${account.account_number}_${account.account_type}_${index}`}
          >
            <strong>Account Number:</strong> {account.account_number}
            <br />
            <strong>Account Type:</strong> {account.account_type}
            <br />
            <strong>Balance:</strong> {account.balance}
            <br />
            <strong>Account Owner:</strong> {account.account_owner_first_name}{" "}
            {account.account_owner_last_name}
            <br />
          </li>
        ))}
      </ul>
      <form onSubmit={goToDepositPage}>
        <button type="submit">Deposit Funds</button>
      </form>
    </div>
  );
};

export default GetBankAccounts;
