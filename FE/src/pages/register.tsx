import React, { useState } from "react";
import Menu from "./components/Menu";
import { UserInterfaceProps } from "./interfaces/UserInterfaceProps";
import axios from "axios";

interface User {
    name: string;
    surname: string;
    email: string;
    password: string;
}

const Register: React.FC<UserInterfaceProps> = ({ backendName }) => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";
    const [users, setUsers] = useState<User[]>([]);
    const [newUser, setNewUser] = useState({ name: '', surname: '', email: '', password: '' });

    const createUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await axios.post(`${apiUrl}/api/${backendName}/register`, newUser);
            setUsers([response.data, ...users]);
            setNewUser({ name: '', surname: '', email: '', password: '' });
        } catch (error) {
            console.error("Error Creating User: ", error);
        }
    }

    return (
        <div className="bg-neomorphism w-screen h-screen">
            <Menu />
            <div className="isolate my-8">
                <div className="relative px-6 lg:px-8">
                    <img
                        src={`/logo.png`}
                        alt={`Sentinel Logo`}
                        className="w-40 h-40 mx-auto"
                    />
                    <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto">
                        <div className="w-full shadow-neo rounded-xl md:mt-0 sm:max-w-md xl:p-0">
                            <div className="p-6 space-y-4 md:space-y-6 sm:p-8">
                                <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
                                    Create your account
                                </h1>
                                <form
                                    className="space-y-4 md:space-y-6"
                                    onSubmit={createUser}
                                >
                                    <div>
                                        <input
                                            type="name"
                                            placeholder="your-cool-name"
                                            value={newUser.name}
                                            onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                                            className="bg-neomorphism border-blue-200 focus:border-blue-500 border-b-2 text-gray-900 sm:text-sm block w-full p-2.5 outline-none"  
                                        />
                                    </div>
                                    <div>
                                        <input
                                            type="name"
                                            placeholder="your-cool-surname"
                                            value={newUser.surname}
                                            onChange={(e) => setNewUser({ ...newUser, surname: e.target.value })}
                                            className="bg-neomorphism border-blue-200 focus:border-blue-500 border-b-2 text-gray-900 sm:text-sm block w-full p-2.5 outline-none"                                            
                                        />
                                    </div>
                                    <div>
                                        <input
                                            type="email"
                                            placeholder="your-cool-email"
                                            value={newUser.email}
                                            onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                                            className="bg-neomorphism border-blue-200 focus:border-blue-500 border-b-2 text-gray-900 sm:text-sm block w-full p-2.5 outline-none"
                                        />
                                    </div>
                                    <div>
                                        <input
                                            type="password"
                                            placeholder="your-super-secret-password"
                                            value={newUser.password}
                                            onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                                            className="bg-neomorphism border-blue-200 focus:border-blue-500 border-b-2 text-gray-900 sm:text-sm block w-full p-2.5 outline-none"
                                        />
                                    </div>
                                    <button
                                        type="submit"
                                        className="shadow-neo bg-gradient-to-r from-cyan-500 to-blue-500 w-full text-white font-medium rounded-xl text-sm px-5 py-2.5 text-center"
                                    >
                                        Sign up
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;
