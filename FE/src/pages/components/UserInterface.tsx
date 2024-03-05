import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

import Caption from "./Caption";
import OperatorCard from "./OperatorCard";
import { Log } from "../interfaces/LogInterface";
import { User } from "../interfaces/UserInterface";

interface UserInterfaceProps {
    backendName: string;
}

const UserInterface: React.FC<UserInterfaceProps> = ({ backendName }) => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";

    const [users, setUsers] = useState<User[]>([]);
    const [logs, setLogs] = useState<Log[]>([]);
    const [previousLogs, setPreviousLogs] = useState<Log[]>([]);
    let previousData: any;

    const createitemRef = (id_user: number) => {
        const itemRef = React.createRef();
        const log = logs.find((log) => log.id_user === id_user);
        if (log) log.ref = itemRef;
        return itemRef;
    };

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await axios.get(
                    `${apiUrl}/api/${backendName}/users`
                );
                console.log(response.data);
                setUsers(response.data.reverse());
            } catch (error) {
                console.error("Error Fetching Data: ", error);
            }
        };

        // fetchUsers();

        const fetchData = async () => {
            try {
                setPreviousLogs(previousData);
                console.log("Previous Data: ", previousData);
                const response = await axios.get(
                    `${apiUrl}/api/${backendName}/latest_logs`
                );

                previousData = response.data.reverse();
                console.log("Most Recent Data: ", response.data);
                setLogs(response.data.reverse());
            } catch (error) {
                console.error("Error Fetching Data: ", error);
            }
        };

        setInterval(() => {
            fetchData();
            fetchUsers();
        }, 5000);
    }, [backendName, apiUrl]);

    return (
        <div className="isolate my-8">
            <div className="relative px-6 lg:px-8">
                <img
                    src={`/logo.png`}
                    alt={`${backendName} Logo`}
                    className="w-40 h-40 mx-auto"
                />
                <div className="mx-auto max-w-3xl pt-20 pb-32 sm:pt-48 sm:pb-40">
                    <div>
                        <div className="m-[-10rem]">
                            <h1 className="text-2xl font-bold tracking-tight sm:text-center sm:text-6xl">
                                Sentinel
                            </h1>
                            <p className="mt-6 text-sm leading-8 text-gray-600 sm:text-center">
                                Solution for industrial maintenance in complex
                                tunnels, monitoring the position, status, and
                                well-being of operators <br /> with
                                battery-powered devices, external IP network,
                                and a comprehensive administrative service based
                                on AI.
                            </p>
                        </div>
                    </div>
                </div>
                {/* Display Users */}
                <div className="m-[-10rem]">
                    {logs.map((log) => (
                        <div
                            key={log.id}
                            className="col"
                            ref={createitemRef(log.id_user)}
                        >
                            <div
                                key={log.id_user}
                                className="flex items-center justify-between"
                            >
                                {/* Add prevCol in Interface then add from: prevCol to Col to animation */}
                                <OperatorCard
                                    log={log}
                                    username={
                                        users.find(
                                            (user) => user.id === log.id_user
                                        )?.id
                                    }
                                    type={
                                        users.find(
                                            (user) => user.id === log.id_user
                                        )?.type
                                    }
                                    prevCol={
                                        previousLogs?.find(
                                            (prev_log) =>
                                                prev_log.id_user === log.id_user
                                        )?.col ?? 0
                                    }
                                />
                            </div>
                            
                        </div>
                    ))}
                </div>
            </div>
            <Caption />
        </div>
    );
};

export default UserInterface;
