import React, { useRef, useEffect, useState } from "react";
import { Log } from "../interfaces/LogInterface";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

const OperatorCard: React.FC<{ log: Log }> = ({ log }) => {
    const MAX_COLS = 12;
    const [screenWidth, setScreenWidth] = useState(window.innerWidth);

    const mapValue = (value: number, minValue: number, maxValue: number, minNewRange: number, maxNewRange: number) => {
        const percentage = (value - minValue) / (maxValue - minValue);
        const valueInNewRange = percentage * (maxNewRange - minNewRange) + minNewRange;
        return valueInNewRange;
    };

    useEffect(() => {
        const updateScreenWidth = () => {
          setScreenWidth(window.innerWidth);
        };
    
        window.addEventListener('resize', updateScreenWidth);
    
        return () => {
          window.removeEventListener('resize', updateScreenWidth);
        };
    }, []);

    useGSAP(
        () => {
            gsap.to(".box", {
                x: mapValue(log.col, 0, MAX_COLS, 0, screenWidth),
            });
        },
        { scope: log.ref }
    );

    return (
        <div className={`p-2`}>
            <div ref={log.ref} className="app">
                <div className="box">
                    <svg
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
                    </svg>
                    <span>
                        {log.id_user} : {log.col} : {log.strength} : {log.BPM}
                    </span>
                </div>
            </div>

            {/* <h1 className="text-base font-sm leading-7 tracking-tight text-gray-800">{Operator.name}</h1>
            <p className="text-sm font-sm leading-6 text-gray-500">{Log.col}</p> */}
        </div>
    );
}

export default OperatorCard;
