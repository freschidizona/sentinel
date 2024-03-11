import React from "react";
import Link from "next/link";

const Menu = () => {
    return (
        <div>
            <nav className="bg-neomorphism border-gray-200">
                <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
                    <a href="/" className="flex items-center space-x-3">
                        <img
                            src={`/logo.png`}
                            alt={`Sentinel Logo`}
                            className="w-8 h-8 mx-auto"
                        />
                        <span className="self-center text-lg font-mono whitespace-nowrap dark:text-white">
                            Sentinel<p className="my-[-8px] text-sm text-gray-500">Be safe everytime</p>
                        </span>
                    </a>
                    <div className="flex items-center space-x-6">
                        <a
                            href="tel:5541251234"
                            className="text-sm text-gray-500 dark:text-white"
                        >
                            (39) 392 123 1722
                        </a>
                        <Link
                            className="text-sm text-blue-600 dark:text-blue-500"
                            href="/login"
                        >
                            Login
                        </Link>
                        <Link
                            className="text-sm text-blue-600 dark:text-blue-500"
                            href="/register"
                        >
                            Register
                        </Link>
                    </div>
                </div>
            </nav>
            <nav className="bg-neomorphism">
                <div className="max-w-screen-xl px-4 py-3 mx-auto">
                    <div className="flex items-center">
                        <ul className="flex flex-row font-medium mt-0 space-x-8 text-sm">
                            <li>
                                <a
                                    href="#"
                                    className="text-gray-900 dark:text-white hover:text-gray-700"
                                >
                                    Employees
                                </a>
                            </li>
                            <li>
                                <a
                                    href="#"
                                    className="text-gray-900 dark:text-white hover:text-gray-700"
                                >
                                    Installation
                                </a>
                            </li>
                            <li>
                                <a
                                    href="#"
                                    className="text-gray-900 dark:text-white hover:text-gray-700"
                                >
                                    Company
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Menu;
