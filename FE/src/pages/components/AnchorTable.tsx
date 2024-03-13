import React from "react";

const AnchorTable = () => {
    return (
        <div className="py-12">
            <div className="max-w-sm sm:px-6 lg:px-8">
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
                                                                Status
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="h-96 overflow-y-auto">
                                                        <tr className="bg-white border-b text-gray-800">
                                                            <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                1
                                                            </td>
                                                            <td className="text-sm font-extrabold font-light px-6 py-4 whitespace-nowrap">
                                                                OFFLINE
                                                            </td>
                                                        </tr>
                                                        <tr className="bg-white border-b text-gray-800">
                                                            <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                1
                                                            </td>
                                                            <td className="text-sm font-extrabold font-light px-6 py-4 whitespace-nowrap">
                                                                OFFLINE
                                                            </td>
                                                        </tr>
                                                        <tr className="bg-white border-b text-gray-800">
                                                            <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                1
                                                            </td>
                                                            <td className="text-sm font-extrabold font-light px-6 py-4 whitespace-nowrap">
                                                                ONLINE
                                                            </td>
                                                        </tr>
                                                        <tr className="bg-white border-b text-gray-800">
                                                            <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                1
                                                            </td>
                                                            <td className="text-sm font-extrabold font-light px-6 py-4 whitespace-nowrap">
                                                                ONLINE
                                                            </td>
                                                        </tr>
                                                        <tr className="bg-white border-b text-gray-800">
                                                            <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                1
                                                            </td>
                                                            <td className="text-sm font-extrabold font-light px-6 py-4 whitespace-nowrap">
                                                                ONLINE
                                                            </td>
                                                        </tr>
                                                        <tr className="bg-white border-b text-gray-800">
                                                            <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                1
                                                            </td>
                                                            <td className="text-sm font-extrabold font-light px-6 py-4 whitespace-nowrap">
                                                                ONLINE
                                                            </td>
                                                        </tr>
                                                        <tr className="bg-white border-b text-gray-800">
                                                            <td className="uppercase text-sm font-light px-6 py-4 whitespace-nowrap">
                                                                1
                                                            </td>
                                                            <td className="text-sm font-extrabold font-light px-6 py-4 whitespace-nowrap">
                                                                ONLINE
                                                            </td>
                                                        </tr>
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
