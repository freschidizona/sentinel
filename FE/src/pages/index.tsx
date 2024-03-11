import React from "react";
import App from "./components/App";

const Home: React.FC = () => {
    return (
        <div>
            <App backendName="flask" />
        </div>
    );
}

export default Home;

// import React, { useState, useEffect } from "react";
// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
// import App from "./components/App";
// import dynamic from 'next/dynamic';

// const isBrowser = typeof window === "object";
// const e = dynamic(
//     () => import('./components/App'),
//     { ssr: false }
//   )
  

// function Home() {
//     if (typeof window !== "undefined") {
//         return (
//             <div>
//                 <Router>
//                     <Switch>
//                         <Route path="/" component={e} />
//                         {/* <PrivateRoute path="/dashboard" component={Dashboard} /> */}
//                     </Switch>
//                 </Router>
//             </div>
//         )
//     }
// }
// export default Home;
