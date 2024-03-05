import React, { useState, useEffect } from "react";
import axios from 'axios';

interface User {
    id: number;
    email: string;
    password: string;
}

interface UserInterfaceProps {
    backendName: string;
}

const App: React.FC<UserInterfaceProps> = ({ backendName }) => {
    // API Url
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    // Handle states of Users
    const [users, setUsers] = useState<User[]>([]);
    const [newUser, setNewUser] = useState({ email: '', password: '' });
    const [updateUser, setUpdateUser] = useState({ email: '', password: '' });

    const backgroundColors: { [key: string]: string } = {
        flask: 'bg-[#E0EAF5]',
    };

    const buttonColors: { [key: string]: string } = {
        flask: 'bg-[#E0EAF5] hover:bg-[#DEE6F0]',
    };

    const bgColor = backgroundColors[backendName as keyof typeof backgroundColors] || 'bg-gray-200';
    const btnColor = buttonColors[backendName as keyof typeof backgroundColors] || 'bg-gray-500 hover:bg-gray-600'

    // Check if User exists
    const createUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await axios.post(`${apiUrl}/api/${backendName}/register`, newUser);
            setUsers([response.data, ...users]);
            setNewUser({ email: '', password: '' });
        } catch (error) {
            console.error("Error Creating User: ", error);
        }
    }
    // Check if User exists
    const loginUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await axios.post(`${apiUrl}/api/${backendName}/login`, newUser);
        } catch (error: any) {
            if (error.response.status === 401) {
                alert("Invalid credentials");
            }
        }
    }

    // Update User
    // const handleUpdateUser = async (e: React.FormEvent<HTMLFormElement>) => {
    //     e.preventDefault();
    //     try {
    //         const response = await axios.put(`${apiUrl}/api/${backendName}/users/${updateUser.id}`, { name: updateUser.name, email: updateUser.email });
    //         setUpdateUser({ id: '', name: '', email: '', job: '' });
    //         setUsers(
    //             users.map((user) => {
    //                 if (user.id === parseInt(updateUser.id))
    //                     return { ...user, name: updateUser.name, email: updateUser.email };
    //                 return user;
    //             })
    //         );
    //     } catch (error) {
    //         console.error("Error Updating User: ", error);
    //     }
    // }

    return (
        <div className={`user-interface ${bgColor} ${backendName} w-full h-full p-4 my-4 rounded-2xl`}>
            {/* <img src={`/logo.png`} alt={`${backendName} Logo`} className="w-80 h-80 mb-6 mx-auto" /> */}
            {/* Create User */}
            <div>
                <form onSubmit={loginUser} className="flex flex-col justify-center items-center space-y-4">
                    <input 
                        placeholder="your-cool-mail ;)" 
                        value={newUser.email}
                        // onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                        className={`${bgColor} p-4 rounded-2xl shadow-neo`}
                    />
                    <input 
                        placeholder="your-super-secret-password ;)" 
                        value={newUser.password}
                        // onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                        className={`${bgColor} p-4 rounded-2xl shadow-neo`}
                    />
                    <button type="submit" className={`${bgColor} p-2 w-52 rounded-2xl shadow-neo text-gray-400 hover:shadow-inner-neo`}>Add</button>
                </form>
            </div>
        </div>
    );
};

export default App;