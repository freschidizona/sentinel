import React, { useEffect, useState, useRef } from "react";
import Menu from "./Menu";
import Login from "../login";
import Link from "next/link";
import client from "../client";
import { UserInterfaceProps } from "../interfaces/UserInterfaceProps";
import { io } from 'socket.io-client';
import { socket } from "../socket";

interface User {
    id: string;
    email: string;
    name: string;
    surname: string;
}

const App : React.FC<UserInterfaceProps> = ({ backendName }) => {
    // const socket = socketIO.connect('ws://localhost:4000');
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const wsUrl = 'http://localhost:4000';

    const [user, setUser] = useState<User>();
    const [isConnected, setIsConnected] = useState(socket.connected);

    const logoutUser = async () => {
        await client.post(`${apiUrl}/api/${backendName}/logout`);
        window.location.href = "/";
    };
    
    useEffect(() => {
        (async () => {
            try {
                console.log("Authenticating...");
                const resp = await client.get(`${apiUrl}/api/${backendName}/@me`);
                setUser(resp.data);
            } catch (error) {
                console.log("Not authenticated");
            }
        })();
    }, []);

    const connection = useRef(null)

    useEffect(() => {
      const socket = new WebSocket("ws://localhost:4000")
  
      // Connection opened
      socket.addEventListener("open", (event) => {
        socket.send("Connection established")
      })
  
      // Listen for messages
      socket.addEventListener("message", (event) => {
        console.log("Message from server ", event.data)
      })
  
      connection.current = ws
  
      return () => connection.close();
    }, [])


    return user != null ? (
        <div className="bg-neomorphism w-screen h-screen">
            <nav className="bg-neomorphism border-gray-200">
                <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
                    <a href="/" className="flex items-center space-x-3">
                        <img
                            src={`/logo.png`}
                            alt={`Sentinel Logo`}
                            className="w-8 h-8 mx-auto"
                        />
                        <span className="self-center text-lg font-md whitespace-nowrap">
                            Sentinel<p className="my-[-8px] text-sm text-gray-500">Be safe everytime</p>
                        </span>
                    </a>
                    <div className="flex items-center space-x-6">
                        <a
                            href="tel:5541251234"
                            className="text-sm text-gray-500"
                        >
                            (39) 392 123 1722
                        </a>
                        <p className="text-sm">
                            <span className="text-gray-600">Benvenuto</span> {user.name} {user.surname}!
                        </p>
                        <button className="text-sm text-gray-500" onClick={logoutUser}>Logout</button>
                    </div>
                </div>
            </nav>
            <div className="isolate my-8">
                <div className="relative px-6 lg:px-8">
                    <img
                        src={`/logo.png`}
                        alt={`Sentinel Logo`}
                        className="w-40 h-40 mx-auto"
                    />
                    <div className="mx-auto max-w-3xl pt-40 pb-32 sm:pt-48 sm:pb-40">
                        <div>
                            <div className="m-[-10rem]">
                                <h1 className="text-2xl font-bold tracking-tight sm:text-center sm:text-6xl">
                                    Sentinel
                                </h1>
                                <p className="mt-6 text-sm leading-8 text-gray-600 sm:text-center">
                                    Solution for industrial maintenance in
                                    complex tunnels, monitoring the position,
                                    status, and well-being of operators <br />{" "}
                                    with battery-powered devices, external IP
                                    network, and a comprehensive administrative
                                    service based on AI.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    ) : ( null );
};

export default App;
