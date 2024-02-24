import React from "react";

const Caption = () => {
    return (
        <figcaption className="mt-10">
            <div className="mt-4 flex items-center justify-center space-x-3 text-base">
                <div className="text-white">
                    <span className="font-sm">Made with ♥ by </span>
                    <span className="font-semibold">Giuseppe Pitruzzella</span>
                </div>                    
            </div>
        </figcaption>
    );
};

export default Caption;