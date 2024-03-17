import React, { createContext } from 'react';
import { io, Socket } from 'socket.io-client';
import Login from "./login";

const socket = io('http://localhost:3000'), SocketContext = createContext<Socket>(socket);
socket.on('Connect', () => console.log('connected to socket'));

const Home: React.FC = () => {
    return (
        <div>
            <Login />
        </div>
    );
};

const SocketProvider = ({ children }: any) => {
    return (
        <SocketContext.Provider value={socket}>{children}</SocketContext.Provider>
    );
};
export { SocketContext, SocketProvider };

export default Home;