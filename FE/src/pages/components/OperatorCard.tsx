import React, { useRef, useEffect, useState } from "react";

import { Log } from "../interfaces/LogInterface";
import { User } from "../interfaces/UserInterface";

import gsap from "gsap";
import { useGSAP } from "@gsap/react";

const OperatorCard: React.FC<{ log: Log; username: any; prevCol: any }> = ({
    log,
    username,
    prevCol,
}) => {
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
                {x: mapValue(prevCol, 0, MAX_COLS, 100, screenWidth - 100)}, 
                {x: mapValue(log.col, 0, MAX_COLS, 100, screenWidth - 100)}
            );
        },
        { scope: log.ref }
    );

    return (
        <div className={`p-2`}>
            <div ref={log.ref} className="app">
                <div className="box flex flex-col items-center">
                    <h1 className="text-sm font-sm tracking-tight text-gray-800 py-2">
                        {username}
                    </h1>
                    <div className="flex justify-center justify-between items-center">
                        <span className="relative flex h-3 w-3">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-3 w-3 bg-sky-500"></span>
                        </span>
                        {/* <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            strokeWidth={1.5}
                            stroke="currentColor"
                            className="w-6 h-6"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z"
                            />
                        </svg> */}
                    </div>
                    <h1 className="text-sm font-sm tracking-tight text-gray-500 py-2 animate-pulse">
                        {log.bpm}
                    </h1>
                    
                </div>
            </div>
        </div>
    );
};

export default OperatorCard;
