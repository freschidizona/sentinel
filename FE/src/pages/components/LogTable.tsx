import React from "react";

const LogTable = () => {
    return (
        <div>
            <table className="table-auto">
                <thead>
                    <tr>
                        <th>Address</th>
                        <th>Name</th>
                        <th>Anchor</th>
                        <th>Meters</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>123:123:123:123</td>
                        <td>Malcolm Lockyer</td>
                        <td>3</td>
                        <td>10m</td>
                    </tr>
                    <tr>
                        <td>123:123:123:123</td>
                        <td>Shining Star</td>
                        <td>3</td>
                        <td>10m</td>
                    </tr>
                    <tr>
                        <td>123:123:123:123</td>
                        <td>Malcolm Lockyer</td>
                        <td>3</td>
                        <td>10m</td>
                    </tr>
                    <tr>
                        <td>123:123:123:123</td>
                        <td>Shining Star</td>
                        <td>3</td>
                        <td>10m</td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
};

export default LogTable;