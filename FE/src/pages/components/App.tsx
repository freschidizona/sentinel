import React from "react";
import Menu from "./Menu";

const App: React.FC = () => {
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
                    <div className="mx-auto max-w-3xl pt-40 pb-32 sm:pt-48 sm:pb-40">
                        <div>
                            <div className="m-[-10rem]">
                                <h1 className="text-2xl font-bold tracking-tight sm:text-center sm:text-6xl">
                                    Sentinel
                                </h1>
                                <p className="mt-6 text-sm leading-8 text-gray-600 sm:text-center">
                                    Solution for industrial maintenance in
                                    complex tunnels, monitoring the position,
                                    status, and well-being of operators <br />{" "}
                                    with battery-powered devices, external IP
                                    network, and a comprehensive administrative
                                    service based on AI.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div className="mx-auto max-w-3xl my-[-10px]">
                        <div>
                            <div>
                                <h1 className="text-xl font-bold tracking-tight text-center">
                                    How to start?
                                </h1>
                                <p className="mt-6 text-sm leading-8 text-gray-600 sm:text-center">
                                    Solution for industrial maintenance in
                                    complex tunnels, monitoring the position,
                                    status, and well-being of operators <br />{" "}
                                    with battery-powered devices, external IP
                                    network, and a comprehensive administrative
                                    service based on AI.
                                </p>
                                <div className="mt-10 flex items-center justify-center gap-x-6">
                                    <code className="text-xs inline-flex text-left items-center space-x-4 bg-gray-800 text-white rounded-2xl p-4 pl-6">
                                        <span className="flex gap-4">
                                            <span className="shrink-0 text-gray-500">
                                                $
                                            </span>
                                            <span className="flex-1">
                                                <span>
                                                    docker compose build
                                                </span>
                                            </span>
                                        </span>
                                        <svg
                                            className="shrink-0 h-5 w-5 transition text-gray-500 group-hover:text-white"
                                            xmlns="http://www.w3.org/2000/svg"
                                            viewBox="0 0 20 20"
                                            fill="currentColor"
                                            aria-hidden="true"
                                        >
                                            <path d="M8 2a1 1 0 000 2h2a1 1 0 100-2H8z"></path>
                                            <path d="M3 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v6h-4.586l1.293-1.293a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L10.414 13H15v3a2 2 0 01-2 2H5a2 2 0 01-2-2V5zM15 11h2a1 1 0 110 2h-2v-2z"></path>
                                        </svg>
                                    </code>
                                    <code className="text-xs inline-flex text-left items-center space-x-4 bg-gray-800 text-white rounded-2xl p-4 pl-6">
                                        <span className="flex gap-4">
                                            <span className="shrink-0 text-gray-500">
                                                $
                                            </span>
                                            <span className="flex-1">
                                                <span className="text-yellow-500">
                                                    docker compose up
                                                </span>
                                            </span>
                                        </span>
                                        <svg
                                            className="shrink-0 h-5 w-5 transition text-gray-500 group-hover:text-white"
                                            xmlns="http://www.w3.org/2000/svg"
                                            viewBox="0 0 20 20"
                                            fill="currentColor"
                                            aria-hidden="true"
                                        >
                                            <path d="M8 2a1 1 0 000 2h2a1 1 0 100-2H8z"></path>
                                            <path d="M3 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v6h-4.586l1.293-1.293a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L10.414 13H15v3a2 2 0 01-2 2H5a2 2 0 01-2-2V5zM15 11h2a1 1 0 110 2h-2v-2z"></path>
                                        </svg>
                                    </code>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default App;
