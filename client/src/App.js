import React, { useState } from 'react';
import './index.css'; // This is the CSS file you'll create for styling

const InboxEagle = () => {
  const [days, setDays] = useState(7);
  // emailEvaluations contains objects with the properties: receivedAt, rating, subject, evaluatorResponse, snippet
  const [emailEvaluations, setEmailEvaluations] = useState([]);

  const handleEvaluateClick = () => {
    // Placeholder for actual evaluation logic
    console.log('Evaluating emails from the last', days, 'days');
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
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  return (
    <div className="inbox-eagle">
      <div className="header">
        <img src="eagle-logo.png" alt="Inbox Eagle Logo" />
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
        <button onClick={handleEvaluateClick}>Evaluate emails</button>
      </div>
      <table className="emails">
        <thead>
          <tr>
            <th>Received date</th>
            <th>Rating</th>
            <th>Subject</th>
            <th>Evaluation</th>
            <th>Snippet</th>
          </tr>
        </thead>
        <tbody>
          {/* list each evaluation */}
          {emailEvaluations.map((evaluation, index) => (
            <tr key={index}>
              <td>{evaluation.receivedAt ? new Date(Number(evaluation.receivedAt)).toLocaleDateString() : ''}</td>
              <td>{evaluation.rating}</td>
              <td>{evaluation.subject}</td>
              <td>{evaluation.evaluatorResponse}</td>
              <td>{evaluation.snippet}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InboxEagle;
