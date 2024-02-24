import React from "react";

interface Card {
    id: number;
    name: string;
    email: string;
    job: string;
}

const CardComponent: React.FC<{ card: Card }> = ({ card }) => {
    return (
        <div className="p-2">
            <h1 className="text-base font-sm leading-7 tracking-tight text-gray-800">{card.name}</h1>
            <p className="text-sm font-sm leading-6 text-gray-500">{card.job}</p>
        </div>
    );
};

export default CardComponent;