import React, { useEffect, useState, useContext } from "react";
import { SocketContext } from "../socket";
import axios from "axios";

export interface Notify {
    id: number;
    worker_addr: string;
    type: number;
}

const NotifyTable = () => {
    const socket = useContext(SocketContext);
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";
    const [notify, setNotify] = useState<Notify[]>([]);
    const [data, setData] = useState([]);

    useEffect(() => {
        socket?.emit("notify");
        socket?.on("notifyEvent", (res: any) => {
            setNotify(res.data.reverse());
            socket?.emit("notify");
        });
    }, [setNotify]);




    // const [markerPos, setMarkerPos] = useState({
    //     longitude:8.5455940,latitude:47.3977421
    // })
    // const updateData=(data: Notify[])=>{
    //     setNotify(prevProps =>{
    //         return {...prevProps, data}
    //     });
    //     console.log("Data Updated");
    // }
    // useEffect(()=>{
    //     // socket?.emit("notify");
    //     socket.on("notifyEvent",(socketData)=>{
    //         updateData(socketData)
    //     })
    // },[])

    // useEffect(()=>{
    //    console.log(notify)
    // },[notify])









    const ackWorker = async (id: number, workerId: string) => {
        try {
            await axios.post(`${apiUrl}/api/ack`, { type: 2, worker_addr: workerId, id: id });
            setNotify(notify.filter((e) => e.id !== id));
        } catch (error) {
            console.error("Error sending ACK to Worker: ", error);
        }
    }

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
                                                                Notify
                                                            </th>
                                                            <th
                                                                scope="col"
                                                                className="text-md px-6 py-4 text-left"
                                                            >
                                                                
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="h-96 overflow-y-auto">
                                                        {notify?.map(
                                                            (e) => (
                                                                <tr
                                                                    key={
                                                                        e.id
                                                                    }
                                                                    className="bg-white border-b text-gray-800"
                                                                >
                                                                    <td className="text-xs font-extrabold font-light py-4 whitespace-nowrap">
                                                                        {
                                                                        e.type == 1
                                                                            ? e.worker_addr + " " + e.id + " NEEDS HELP 🚑"
                                                                            : e.worker_addr + " " + e.id + " IS DEAD 💀" }
                                                                    </td>
                                                                    <td className="uppercase text-xs font-light px-6 py-4 whitespace-nowrap">
                                                                        <button onClick={() => ackWorker(e.id, e.worker_addr)} className={`w-24 h-16 mr-2 text-blue-600 font-bold rounded-2xl hover:text-blue-400`}>ACK</button>
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

export default NotifyTable;
