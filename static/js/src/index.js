import React from 'react';
import ReactDOM from 'react-dom';


APP_BASE_URL = 'http://localhost:5000'


class Hello extends React.Component {
    constructor(props) {
        super(props);

        var res = fetch('http://localhost:5000/user/1', {method: 'get'})
            .then((data) => {
                return data.text()
            })
            .then((text) => {
                alert(text);
                debugger;
            })
            .catch(() => alert('error'));
    }

    render() {
        return (<h1>Hello, Music App</h1>);
    }
}

ReactDOM.render(<Hello />, document.getElementById('social-network-app'));
