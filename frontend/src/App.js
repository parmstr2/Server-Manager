// App.js
import React, { useEffect, useState } from 'react';
import './App.css';
import ServerStatus from './components/ServerStatus';

function App() {
    const [games, setGames] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/games')
            .then(response => response.json())
            .then(data => setGames(data))
            .catch(error => console.error('Error fetching games:', error));
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>Server Manager</h1>
            </header>
            <main>
                {games.map(game => (
                    <ServerStatus key={game.name} serverName={game.name} />
                ))}
            </main>
        </div>
    );
}

export default App;
