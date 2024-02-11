import React, { useState } from 'react';
import './index.css'; // This is the CSS file you'll create for styling

const InboxEagle = () => {
  const [days, setDays] = useState(7);

  const handleEvaluateClick = () => {
    // Placeholder for actual evaluation logic
    console.log('Evaluating emails from the last', days, 'days');
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
          </tr>
        </thead>
        <tbody>
          {/* Placeholder for email rows */}
          <tr>
            <td>1/1/2024</td>
            <td>8.0</td>
            <td>Please send us an 843 test</td>
            <td>This message seems important as it demands a response</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default InboxEagle;
