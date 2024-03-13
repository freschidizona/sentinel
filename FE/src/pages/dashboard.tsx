import React, { useEffect, useState, useRef } from "react";
import Menu from "./components/Menu";
import Login from "./login";
import Link from "next/link";
import client from "./client";

import LogTable from "./components/LogTable";
import AnchorTable from "./components/AnchorTable";
import NotifyTable from "./components/NotifyTable";

import { UserInterfaceProps } from "./interfaces/UserInterfaceProps";
import io from "socket.io-client";

interface User {
    id: string;
    email: string;
    name: string;
    surname: string;
}

const App: React.FC<UserInterfaceProps> = () => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";
    const [user, setUser] = useState<User>();

    const [isConnected, setIsConnected] = useState();

    useEffect(() => {
        const URL = "http://localhost:4000";
        const socket = io(URL);
        socket?.emit("message", "Hello");

        // return () => {
        //     socket?.off('connect', onConnect);
        //     socket?.off('disconnect', onDisconnect);
        // };
    }, []);

    const logoutUser = async () => {
        await client.post(`${apiUrl}/api/logout`);
        window.location.href = "/";
    };

    useEffect(() => {
        (async () => {
            try {
                console.log("Authenticating...");
                const resp = await client.get(`${apiUrl}/api/@me`);
                setUser(resp.data);
            } catch (error) {
                console.log("Not authenticated");
            }
        })();
    }, []);

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
                            Sentinel
                            <p className="my-[-8px] text-sm text-gray-500">
                                Be safe everytime
                            </p>
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
                            <span className="text-gray-600">Benvenuto</span>{" "}
                            {user.name} {user.surname}!
                        </p>
                        <button
                            className="text-sm text-gray-500"
                            onClick={logoutUser}
                        >
                            Logout
                        </button>
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
                    <div className="flex items-center justify-center px-6 py-8 mx-auto">
                        <AnchorTable />
                        <LogTable />
                        <NotifyTable />
                    </div>
                </div>
            </div>
        </div>
    ) : (
        <div className="text-3xl text-red font-bold my-8 text-center">
            Error! User is not authenticated
        </div>
    );
};

export default App;
