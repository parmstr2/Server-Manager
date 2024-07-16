// App.js
import React, { useEffect, useState } from 'react';
import './App.css';
import Dropdown from 'react-bootstrap/Dropdown';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import ServerStatus from './components/ServerStatus';
import CollapsibleMenu from './Collapsible.js';

function App() {
    const [games, setGames] = useState([]);
    const [serverName, setServerName] = useState("")
    const [serverIP, setServerIP] = useState("localhost")
    const [serverPort, setServerPort] = useState("")

    useEffect(() => {
        fetch('http://localhost:5000/games')
            .then(response => response.json())
            .then(data => setGames(data))
            .catch(error => console.error('Error fetching games:', error));
    }, []);

    const handleName = (event) => {
        setServerName(event.target.value)
    };

    const handleIP = (event) => {
        setServerIP(event.target.value)
    };

    const handlePort = (event) => {
        setServerPort(event.target.value)
    };

    const newServer = () => {
        let body = {"ip": serverIP, "port": serverPort}
        
        fetch('http://localhost:5000/new/minecraft/' + serverName, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Server Manager</h1>
            </header>
            <main>
                {games.map(game => (
                    <div className='serverType'>
                        <CollapsibleMenu title={game.name}>
                            <div className='new-server'>
                                <input type='text' value={serverName} placeholder='Server Name' onChange={handleName} style={{width:"10%"}}/>
                                <input type='text' value={serverIP} defaultValue='localhost' onChange={handleIP} style={{width:"10%"}}/>
                                <input type='text' value={serverPort} placeholder='Port' onChange={handlePort} style={{width:"10%"}}/>
                                {game.name === "minecraft" ? (
                                    <Dropdown>
                                        <Dropdown.Toggle variant='primary' id='dropdown-basic'>
                                            Version
                                        </Dropdown.Toggle>
                                        <Dropdown.Menu>
                                            {game.versions.map(version => {
                                                return <Dropdown.Item href={version}>{version}</Dropdown.Item>
                                            })}
                                        </Dropdown.Menu>
                                    </Dropdown>
                                ) : (
                                    <div/>
                                )}
                                <button className='create-new' onClick={newServer}>Create Server</button>
                            </div>
                            {game.servers.map(server => (
                                <ServerStatus key={game.name} serverName={server} />
                            ))}
                        </CollapsibleMenu>
                    </div>
                ))}
            </main>
        </div>
    );
}

export default App;
