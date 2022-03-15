import Home from "./Home.js";
import Rooms from "./Rooms.js";

import { Route, BrowserRouter as Router, Switch} from "react-router-dom";


const MainContent = () => {
    return (
        <Router>
            <Switch>
                {/* <p>sdfsdf</p> */}
                {/* <Route path="/" component={Home} />
                <Route path="/rooms" component={Rooms} /> 
                <Route path="/devices" component={Rooms} /> */}
            </Switch>
        </Router>
    )
}

export default MainContent;