import React from 'react';
import Login from "./login";
import { SocketProvider } from './socket';

const Home: React.FC = () => {
    return (
        <div>
            <SocketProvider>
                <Login />
            </SocketProvider>
        </div>
    );
};

export default Home;