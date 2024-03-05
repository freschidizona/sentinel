import React, { useRef, useEffect, useState } from "react";

import { Log } from "../interfaces/LogInterface";
import { User } from "../interfaces/UserInterface";

import gsap from "gsap";
import { useGSAP } from "@gsap/react";

const OperatorCard: React.FC<{
    log: Log;
    username: any;
    type: any;
    prevCol: any;
}> = ({ log, username, prevCol }) => {
    const MAX_COLS = 12;
    const [screenWidth, setScreenWidth] = useState(window.innerWidth);

    const mapValue = (
        value: number,
        minValue: number,
        maxValue: number,
        minNewRange: number,
        maxNewRange: number
    ) => {
        const percentage = (value - minValue) / (maxValue - minValue);
        const valueInNewRange =
            percentage * (maxNewRange - minNewRange) + minNewRange;
        return valueInNewRange;
    };

    useEffect(() => {
        const updateScreenWidth = () => {
            setScreenWidth(window.innerWidth);
        };

        window.addEventListener("resize", updateScreenWidth);

        return () => {
            window.removeEventListener("resize", updateScreenWidth);
        };
    }, []);

    useGSAP(
        () => {
            gsap.fromTo(
                ".box",
                { x: mapValue(prevCol, 0, MAX_COLS, 100, screenWidth - 100) },
                { x: mapValue(log.col, 0, MAX_COLS, 100, screenWidth - 100) }
            );
        },
        { scope: log.ref }
    );

    const updateType = async (userId: number) => {
        // try {
            
        //     await axios.update(`${apiUrl}/api/${backendName}/users/${userId}`);
        //     setUsers(users.filter((user) => user.id !== userId));
        // } catch (error) {
        //     console.error("Error Updating Type: ", error);
        // }
    }

    return (
        <div className={`p-2`}>
            <div ref={log.ref} className="app">
                <div className="box flex flex-col items-center">
                    <h1 className="text-xs font-sm tracking-tight text-gray-400 py-2">
                        {username}
                    </h1>
                    <div className="flex justify-center justify-between items-center">
                        <span className="relative flex h-3 w-3">
                            <span
                                className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                                    log.type === 0
                                        ? "bg-green-400"
                                        : "bg-red-400"
                                }`}
                            ></span>
                            <span
                                className={`relative inline-flex rounded-full h-3 w-3 ${
                                    log.type === 0
                                        ? "bg-green-500"
                                        : "bg-red-500"
                                }`}
                            ></span>
                        </span>
                    </div>
                    <h1 className="text-xs font-sm tracking-tight text-gray-500 py-2 animate-pulse">
                        COL : {log.col} BPM : {log.bpm}, TEMP : {log.temp}
                    </h1>
                    <button
                        onClick={() => updateType(username)}
                        className={`bg-blue-500 text-xs hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-xl ${
                            log.type === 0 ? "hidden" : ""
                        }`}
                    >
                        ACK
                    </button>
                </div>
            </div>
        </div>
    );
};

export default OperatorCard;
