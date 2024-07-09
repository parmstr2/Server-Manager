// components/ServerStatus.js
import React, { useEffect, useState } from 'react';

function ServerStatus({ serverName }) {
    const [status, setStatus] = useState({ status: 'unknown', players: 0 });

    useEffect(() => {
        fetch(`http://localhost:5000/status/${serverName}`)
            .then(response => response.json())
            .then(data => setStatus(data))
            .catch(error => console.error(`Error fetching status for ${serverName}:`, error));
    }, [serverName]);

    const handleReboot = () => {
        fetch(`http://localhost:5000/reboot/${serverName}`, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                // Re-fetch status after reboot
                fetch(`http://localhost:5000/status/${serverName}`)
                    .then(response => response.json())
                    .then(data => setStatus(data));
            })
            .catch(error => console.error(`Error rebooting ${serverName}:`, error));
    };

    return (
        <div className="server-status">
            <h2>{serverName}</h2>
            <p>Status: {status.status}</p>
            <p>Players: {status.players}</p>
            <button onClick={handleReboot}>Reboot</button>
        </div>
    );
}

export default ServerStatus;
