//import { Button } from 'reactstrap';
//import React from 'react';
const Button = window.Reactstrap.Button;

const Collapse = window.Reactstrap.Collapse;
const Navbar = window.Reactstrap.Navbar;
const NavbarBrand = window.Reactstrap.NavbarBrand;
const Nav = window.Reactstrap.Nav;
const NavItem = window.Reactstrap.NavItem;
const NavLink = window.Reactstrap.NavLink;


const Router = window.ReactRouterDOM.BrowserRouter;
const Route = window.ReactRouterDOM.Route;
const ReactMarkdown = window.ReactMarkdown;

const Form = window.Reactstrap.Form;
const FormGroup = window.Reactstrap.FormGroup;
const Label = window.Reactstrap.Label;
const Input = window.Reactstrap.Input;


const Dropdown = window.Reactstrap.Dropdown;
const Spinner = window.Reactstrap.Spinner;


const axios = window.axios;

const Select = window.Select;


//import { Button } from 'reactstrap';

// Obtain the root 
const rootElement = document.getElementById('root');


class About extends React.Component {
    //

// Use the render function to return JSX component
    render() {
        return (

            <div>
                <h1>About</h1>
                <ReactMarkdown source={window.APP_CONFIG.about}/>
            </div>
        );
    }
}


// Create a ES6 class component
class MainPage extends React.Component {
    //

    constructor(props) {
        super(props);
        this.state = {
            quest_title: null,
            quest_goals: [],
            suggestions: [],
            selectedOption: null,
            custom_goal: null
        }

        this.update_custom_goal = this.update_custom_goal.bind(this);
        this.update_title = this.update_title.bind(this);
    }

    _clear = async (event) => {
        event.preventDefault();

        this.setState({
            quest_title: null,
            quest_goals: [],
            suggestions: [],
            selectedOption: null,
            custom_goal: null
        })
    };

    _get_suggestions = async (event) => {
        event.preventDefault();
        this.setState({isLoading: true});

        let selected = null;
        if (this.state.custom_goal) {
            selected = this.state.custom_goal
        }
        else if (this.state.suggestions.length > 0) {
            selected = this.state.suggestions[this.state.selectedOption];
        }

        let resPromise = null;
        resPromise = axios.post('/api/update_quest', {
            title: this.state.quest_title,
            quest_goals: this.state.quest_goals,
            selected: selected,
        });

        try {
            const res = await resPromise;
            const payload = res.data;

            this.setState({
                quest_title: payload.title,
                quest_goals: payload.current_goals,
                suggestions: payload.suggestions,
                isLoading: false,
                custom_goal: ''
            });
        } catch (e) {
            alert(e)
        }
    };


    renderPrediction() {
        const quest_title = this.state.quest_title || "";
        const goals = this.state.quest_goals || [];

        const quest_goals = goals.map((item) =>
            <li>{item}</li>
        );

        return (
            <ul>
                <h2>{quest_title}</h2>
                {quest_goals}
            </ul>
        )
    }

    renderGoals(){
        const selectGoals = (
            <div>
                <p>Select the next goal...</p>
                <Input type="select" name="selectSuggestion" style={{height: 200}} multiple>
                    {this.state.suggestions.map((sug, idx) =>
                        <option onClick={()=>this.selectSuggestion(idx)}>
                            {sug}
                        </option>)
                    }
                </Input>
                <small>Warning: this is a domain-free model. Some suggestion may not make sense.</small>
                <Input
                    type="text"
                    value={this.state.custom_goal}
                    name="custom_goal"
                    onChange={this.update_custom_goal}
                    placeholder="...or enter it here (can be anything)"
                />
            </div>
        )

        if (this.state.suggestions.length > 0) {
            return selectGoals
        } else {
            return <div></div>
        }
    }

    update_title = (event) => {
        this.setState({quest_title: event.target.value});
    };

    update_custom_goal = (event) => {
        this.setState({custom_goal: event.target.value});
    };

    selectSuggestion  = (item) => {
        this.state.selectedOption = item
    };
    
    render() {
        return (
            <div>
                <h2>{APP_CONFIG.description}</h2>

                <div className="float-right">
                    <small>Developed by <a href="https://tiagohca.com/">Tiago Alves</a></small>
                </div>

                <br/>
                <Form>
                    <FormGroup>
                        <div>
                            <Input
                                type="text"
                                value={this.state.quest_title}
                                name="quest_title"
                                onChange={this.update_title}
                                placeholder="Enter the quest title and click on the green button"
                            />
                            <br/>
                            {this.renderGoals()}
                        </div>
                    </FormGroup>

                    <FormGroup>
                        <Button color="success" onClick={this._get_suggestions}
                                disabled={this.state.isLoading}> Get next goals</Button>
                        <span className="p-1 "/>
                        <Button color="danger" onClick={this._clear}> Clear quest</Button>
                    </FormGroup>


                    {this.state.isLoading && (
                        <div>
                            <Spinner color="primary" type="grow" style={{width: '5rem', height: '5rem'}}/>
                        </div>
                    )}

                </Form>

                {this.renderPrediction()}


            </div>
        );
    }
}

class CustomNavBar extends React.Component {


    render() {
        const link = APP_CONFIG.code;
        return (
            <Navbar color="light" light fixed expand="md">
                <NavbarBrand href="/">{APP_CONFIG.title}</NavbarBrand>
                <Collapse navbar>
                    <Nav className="ml-auto" navbar>
                        <NavItem>
                            <NavLink href={link}>GitHub</NavLink>
                        </NavItem>

                    </Nav>
                </Collapse>
            </Navbar>
        )
    }
}

// Create a function to wrap up your component
function App() {
    return (


        <Router>
            <div className="App">
                <CustomNavBar/>
                <div>
                    <main role="main" className="container">
                        <Route exact path="/" component={MainPage}/>
                        <Route exact path="/about" component={About}/>

                    </main>


                </div>
            </div>
        </Router>
    )
}

(async () => {
    const response = await fetch('/config');
    const body = await response.json();

    window.APP_CONFIG = body;

    // Use the ReactDOM.render to show your component on the browser
    ReactDOM.render(
        <App/>,
        rootElement
    )
})();


