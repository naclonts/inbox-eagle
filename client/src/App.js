import React, { useState } from 'react';
import { ClipLoader } from 'react-spinners';

import './index.css';

const InboxEagle = () => {
  const [days, setDays] = useState(2);
  const [emailEvaluations, setEmailEvaluations] = useState([]);
  const [isLoadingEmailEvaluations, setIsLoadingEmailEvaluations] = useState(false);

  const handleEvaluateClick = () => {
    // Placeholder for actual evaluation logic
    console.log('Evaluating emails from the last', days, 'days');
    setIsLoadingEmailEvaluations(true);
    fetch('http://localhost:5020/get-email-evaluations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ numDaysToInclude: days })
      })
      .then(response => response.json())
      .then(data => {
        console.log('Received email evaluations:', data);
        setEmailEvaluations(data.evaluations);
        setIsLoadingEmailEvaluations(false);
      })
      .catch(error => {
        console.error('Error:', error);
        setIsLoadingEmailEvaluations(false);
      });
  };

  return (
    <div className="inbox-eagle">
      <div className="header">
        <img src="eagle-logo.png" alt="Inbox Eagle Logo" className="logo-image" />
        <h1>Inbox Eagle</h1>
      </div>
      <div className="filter">
        <label htmlFor="days">Include last N days:</label>
        <input
          type="number"
          id="days"
          value={days}
          onChange={(e) => setDays(e.target.value)}
        />
        <button onClick={handleEvaluateClick} disabled={isLoadingEmailEvaluations}>
          Evaluate emails
        </button>
      </div>
      {
        isLoadingEmailEvaluations
          ? (
            <div className="loading">
              <ClipLoader color={'#000'} loading={true} size={150} />
              <p>Evaluating emails...</p>
            </div>
          )
          : (
            emailEvaluations.length === 0
            ? <p></p>
            : <table className="emails">
              <thead>
                <tr>
                  <th>Rating</th>
                  <th>Received date</th>
                  <th>From</th>
                  <th>Subject</th>
                  <th>Snippet</th>
                  <th>Evaluation</th>
                </tr>
              </thead>
              <tbody>
                {/* list each evaluation */}
                {emailEvaluations.map((evaluation, index) => (
                  <tr key={index}>
                    <td>{evaluation.rating}</td>
                    <td>{evaluation.receivedAt ? new Date(Number(evaluation.receivedAt)).toLocaleDateString() : ''}</td>
                    <td>{(evaluation.from || '').split('<')[0].trim()}</td>
                    <td>{evaluation.subject}</td>
                    <td>{evaluation.snippet}</td>
                    <td>{evaluation.evaluatorResponse}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )
      }
    </div>
  );
};

export default InboxEagle;
