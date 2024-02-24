import React, { useState, useEffect } from "react";
import axios from "axios";

import Caption from "./Caption";
import OperatorCard from "./OperatorCard";

import Link from "next/link";
import { useRouter } from "next/router";


interface User {
    id: number;
    name: string;
    email: string;
    job: string;
}

interface UserInterfaceProps {
    backendName: string;
}

const UserInterface: React.FC<UserInterfaceProps> = ({ backendName }) => {
    const router = useRouter();
    // API Url
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";
    // Handle states of Users
    const [users, setUsers] = useState<User[]>([]);
    const [newUser, setNewUser] = useState({ name: "", email: "", job: "" });
    const [updateUser, setUpdateUser] = useState({
        id: "",
        name: "",
        email: "",
        job: "",
    });

    // Fetch Users
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(
                    `${apiUrl}/api/${backendName}/users`
                );
                console.log(response);
                setUsers(response.data.reverse());
            } catch (error) {
                console.error("Error Fetching Data: ", error);
            }
        };

        fetchData();
    }, [backendName, apiUrl]);

    // Create User
    const createUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await axios.post(
                `${apiUrl}/api/${backendName}/users`,
                newUser
            );
            setUsers([response.data, ...users]);
            setNewUser({ name: "", email: "", job: "" });
        } catch (error) {
            console.error("Error Creating User: ", error);
        }
    };

    // Update User
    const handleUpdateUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await axios.put(
                `${apiUrl}/api/${backendName}/users/${updateUser.id}`,
                { name: updateUser.name, email: updateUser.email }
            );
            setUpdateUser({ id: "", name: "", email: "", job: "" });
            setUsers(
                users.map((user) => {
                    if (user.id === parseInt(updateUser.id))
                        return {
                            ...user,
                            name: updateUser.name,
                            email: updateUser.email,
                        };
                    return user;
                })
            );
        } catch (error) {
            console.error("Error Updating User: ", error);
        }
    };

    // Delete User
    const deleteUser = async (userId: number) => {
        try {
            await axios.delete(`${apiUrl}/api/${backendName}/users/${userId}`);
            setUsers(users.filter((user) => user.id !== userId));
        } catch (error) {
            console.error("Error Deleting User: ", error);
        }
    };

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
                            {/* #region Wath Demo */}
                            {/* <div className="mt-8 flex gap-x-4 sm:justify-center">
                                <a href="#" className="inline-block rounded-lg bg-red-600 px-4 py-1.5 text-base font-semibold leading-7 text-white shadow-sm ring-1 ring-red-600 hover:bg-red-700 hover:ring-red-700">
                                    Watch Demo
                                    <span className="text-red-200" aria-hidden="true">&rarr;</span>
                                </a>
                            </div> */}
                            {/* #endregion */}
                            {/* #region SVG BG */}
                            {/* <div className="absolute inset-x-0 -z-10 transform-gpu overflow-hidden blur-2xl sm:top-[calc(100%-30rem)]">
                                <svg className="relative left-[calc(50%+3rem)]  max-w-none -translate-x-1/2 sm:left-[calc(50%+36rem)] sm:h-[42.375rem]" viewBox="0 0 1155 678" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path fill="url(#ecb5b0c9-546c-4772-8c71-4d3f06d544bc)" fill-opacity=".3" d="M317.219 518.975L203.852 678 0 438.341l317.219 80.634 204.172-286.402c1.307 132.337 45.083 346.658 209.733 145.248C936.936 126.058 882.053-94.234 1031.02 41.331c119.18 108.451 130.68 295.337 121.53 375.223L855 299l21.173 362.054-558.954-142.079z" />
                                    <defs>
                                        <linearGradient id="ecb5b0c9-546c-4772-8c71-4d3f06d544bc" x1="1155.49" x2="-78.208" y1=".177" y2="474.645" gradientUnits="userSpaceOnUse">
                                            <stop stop-color="#9089FC"></stop>
                                            <stop offset="1" stop-color="#FF80B5"></stop>
                                        </linearGradient>
                                    </defs>
                                </svg>
                            </div> */}
                            {/* #endregion */}
                        </div>
                    </div>
                    {/* Display Users */}
                    <div className="space-y-2">
                        {users.map((user) => (
                            <div
                                key={user.id}
                                className={`flex items-center justify-between w-64 rounded-2xl`}
                            >
                                <OperatorCard card={user} />
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UserInterface;