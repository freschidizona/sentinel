import React, { useState } from "react";
import Menu from "./components/Menu";
import { UserInterfaceProps } from "./interfaces/UserInterfaceProps";
import axios from "axios";
import client from "./client";

// interface Admin {
//     email: string;
//     password: string;
// }

// Elimina UserInterfaceProps ed utilizza Interfaccia per email e password

const Login = () => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    // const [admin, setAdmin] = useState<Admin>();
  
    const logInUser = async () => {
      console.log(email, password);
  
      try {
        const resp = await client.post(`${apiUrl}/api/login`, {
            email,
            password,
        });
        window.location.href = "/dashboard";
      } catch (error: any) {
            console.log(error);
      }
    };
  

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
                                    Sign in to your account
                                </h1>
                                <form
                                    className="space-y-4 md:space-y-6"
                                    action="#"
                                >
                                    <div>
                                        <input
                                            type="email"
                                            name="email"
                                            id="email"
                                            className="bg-neomorphism border-blue-200 focus:border-blue-500 border-b-2 text-gray-900 sm:text-sm block w-full p-2.5 outline-none"
                                            placeholder="your-cool-email"
                                            onChange={(e) => setEmail(e.target.value)}
                                        />
                                    </div>
                                    <div>
                                        <input
                                            type="password"
                                            name="password"
                                            id="password"
                                            placeholder="your-super-secret-password"
                                            className="bg-neomorphism border-blue-200 focus:border-blue-500 border-b-2 text-gray-900 sm:text-sm block w-full p-2.5 outline-none"
                                            onChange={(e) => setPassword(e.target.value)}
                                        />
                                    </div>
                                    <button
                                        type="button"
                                        className="shadow-neo bg-gradient-to-r from-cyan-500 to-blue-500 w-full text-white font-medium rounded-xl text-sm px-5 py-2.5 text-center"
                                        onClick={() => logInUser()}
                                    >
                                        Sign in
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

export default Login;
