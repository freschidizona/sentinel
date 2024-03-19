import React, { useEffect, useState, useContext } from "react";
import { SocketContext } from "../socket";

export interface Log {
    id: number;
    worker_addr: string;
    anchor_id: string;
    bpm: number;
    temp: number;
    chol: number;
    sug: number;
}

const LogTable = () => {
    const socket = useContext(SocketContext);
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";
    const [logs, setLogs] = useState<Log[]>([]);

    // useEffect(() => {
    //     socket?.emit("latestLogs");
    //     socket?.on("latestLogsEvent", (res: any) => {
    //         setLogs(res.data.reverse());
    //         // socket?.emit("latestLogs");
    //     });
    // }, [setLogs]); // <- Should i put something in []?

    useEffect(() => {
        console.log("Log Component");
        console.log(socket);

        socket?.emit("latestLogs");
        socket?.on("latestLogsEvent", (res: any) => {
            setLogs(JSON.parse(res).reverse());
        });
    }, [setLogs]);

    return (
        <div className="py-12">
            <div className="max-w-2xl sm:px-6 lg:px-8">
                <div className="bg-white overflow-hidden rounded-2xl py-4 px-4">
                    <div className="address">
                        <div className="item mb-2 md:flex md:flex-wrap md:justify-between">
                            <div className="container w-full px-4 sm:px-8">
                                <div className="flex flex-col">
                                    <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
                                        <div className="py-2 inline-block w-full sm:px-6 lg:px-8">
                                            <div className="table-wrp block max-h-96">
                                                <table className="w-full">
                                                    <thead className="bg-white text-xs text-gray-500 font-medium uppercase bg-gray-50 border-b sticky top-0">
                                                        <tr>
                                                            <th
                                                                scope="col"
                                                                className="text-md px-6 py-4 text-left"
                                                            >
                                                                Address
                                                            </th>
                                                            <th
                                                                scope="col"
                                                                className="text-md px-6 py-4 text-left"
                                                            >
                                                                Anchor
                                                            </th>
                                                            <th
                                                                scope="col"
                                                                className="text-md px-6 py-4 text-left"
                                                            >
                                                                BPM
                                                            </th>
                                                            <th
                                                                scope="col"
                                                                className="text-md px-6 py-4 text-left"
                                                            >
                                                                Temp
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="h-96 overflow-y-auto">
                                                        {logs?.map((log) => (
                                                            <tr
                                                                key={log.id}
                                                                className="bg-white border-b text-gray-800"
                                                            >
                                                                <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                    {log.worker_addr + " " + log.id}
                                                                </td>
                                                                <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                    {
                                                                        log.anchor_id
                                                                    }
                                                                </td>
                                                                <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                    {log.bpm}
                                                                </td>
                                                                <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                    {log.temp}
                                                                </td>
                                                            </tr>
                                                        ))}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LogTable;
