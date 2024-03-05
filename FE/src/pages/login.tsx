import React from "react";
import Menu from "./components/Menu";
import { UserInterfaceProps } from "./interfaces/UserInterfaceProps";

const Login: React.FC<UserInterfaceProps> = ({ backendName }) => {
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
                                        />
                                    </div>
                                    <div>
                                        <input
                                            type="password"
                                            name="password"
                                            id="password"
                                            placeholder="your-super-secret-password"
                                            className="bg-neomorphism border-blue-200 focus:border-blue-500 border-b-2 text-gray-900 sm:text-sm block w-full p-2.5 outline-none"
                                        />
                                    </div>
                                    <button
                                        type="submit"
                                        className="shadow-neo bg-gradient-to-r from-cyan-500 to-blue-500 w-full text-white font-medium rounded-xl text-sm px-5 py-2.5 text-center"
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
