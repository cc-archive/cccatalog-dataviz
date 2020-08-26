import React, { Component } from 'react';
import InputSuggest from './InputSuggest'

class Sidebar extends Component {
    state = {
        // stores the state if actions menu is active or not
        'isActionsActive': true,
        // store the node name
        'name': '',
    }

    componentDidMount(){
        // setting the state of the actions action based on value sent as props
        // from the parent component 
        this.setState({
            isActionsActive: this.props.showActionInitialState
        })
    }

    // function to update the {name} variable
    setName = (newVal) => {
        this.setState({
            name: newVal
        })
    }

    render() {
        return (
            <div className='sidebar-wrapper'>
                <div className='project-info'>
                    <div className='project-heading'>The linked commons</div>
                    <div className='project-desc'>This graph visualizes the relationships between domains that use Creative Commons licenses. For more information see our <a href='https://github.com/creativecommons/cccatalog-dataviz/' target='__blank'>Github repo</a>.</div>
                </div>
                <div className='actions-link'>
                    <button className='action-btn' onClick={() => this.setState({ isActionsActive: !this.state.isActionsActive })}>{this.state.isActionsActive ? 'Hide Actions' : 'Show Actions'}</button>
                    {this.state.isActionsActive &&
                        <ActionsMenu
                            handleSubmit={this.props.handleSubmit}
                            processing={this.props.processing}
                            name={this.state.name}
                            setName={this.setName}
                            SERVER_BASE_URL={this.props.SERVER_BASE_URL} />}
                </div>
            </div>
        )
    }
}


export default Sidebar;

// actions menu component
function ActionsMenu(props) {
    let { name, setName, processing, SERVER_BASE_URL } = props;

    return (
        <div className='actions-menu-wrapper'>
            <form onSubmit={(e) => { e.preventDefault(); props.handleSubmit({ name }) }} autoComplete='off'>
                <div className='actions-menu-item'>
                    <label htmlFor='ac-item-graphNodeName'>Name</label>
                    <InputSuggest id='ac-item-graphNodeName' setName={setName}
                        placeholder='icij'
                        value={name}
                        SERVER_BASE_URL={SERVER_BASE_URL} />
                </div>
                <div className={`actions-menu-item ${name === '' ? 'disabled' : ''}`}>
                    <button disabled={name === '' || processing}>{processing ? 'Loading' : 'Filter Graph'}</button>
                </div>
            </form>
        </div>
    )
}


