import React, { useEffect, useState, useContext } from "react";
import { SocketContext } from "../socket";

export interface Anchor {
    id: number;
    status: number;
}

const AnchorTable = () => {
    const socket = useContext(SocketContext);
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";
    const [anchors, setAnchors] = useState<Anchor[]>([]);
    const [data, setData] = useState([]);

    useEffect(() => {
        socket?.emit("anchors");
        socket?.on("anchorsEvent", (res: any) => {
            setAnchors(JSON.parse(res).reverse());
        });
    }, [setAnchors]);

    return (
        <div className="py-12">
            <div className="max-w-lg sm:px-6 lg:px-8">
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
                                                                Index
                                                            </th>
                                                            <th
                                                                scope="col"
                                                                className="text-md px-6 py-4 text-left"
                                                            >
                                                                Meters
                                                            </th>
                                                            <th
                                                                scope="col"
                                                                className="text-md px-6 py-4 text-left"
                                                            >
                                                                Status
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="h-96 overflow-y-auto">
                                                        {anchors?.map(
                                                            (anchor) => (
                                                                <tr
                                                                    key={
                                                                        anchor.id
                                                                    }
                                                                    className="bg-white border-b text-gray-800"
                                                                >
                                                                    <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                        {
                                                                            anchor.id
                                                                        }
                                                                    </td>
                                                                    <td className="text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                        {
                                                                            anchor.id * 20 + " m"
                                                                        }
                                                                    </td>
                                                                    <td className="text-sm font-extrabold font-light px-6 py-4 whitespace-nowrap">
                                                                        {anchor.status ==
                                                                        0
                                                                            ? <span className="relative flex h-3 w-3">
                                                                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                                                                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                                                                            </span>
                                                                            : <span className="relative flex h-3 w-3">
                                                                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                                                                                <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                                                                            </span>
                                                                        }
                                                                    </td>
                                                                </tr>
                                                            )
                                                        )}
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

export default AnchorTable;
