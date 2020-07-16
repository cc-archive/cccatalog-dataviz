import React, { Component } from 'react';
import { ReactComponent as LightLogo } from '../assets/logo/light-logo.svg';
import { ReactComponent as DarkLogo } from '../assets/logo/dark-logo.svg';
import InputSuggest from './InputSuggest'

class Sidebar extends Component {
    state = {
        'isActionsActive': true,
        'name': '',
    }

    setName = (newVal) => {
        this.setState({
            name: newVal
        })
    }

    render() {
        return (
            <div className='sidebar-wrapper'>
                <div className='cc-logo'>
                    {this.props.isDarkMode ? <DarkLogo /> : <LightLogo />}
                </div>
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


function ActionsMenu(props) {
    let { name, setName, processing, SERVER_BASE_URL } = props;

    return (
        <div className='actions-menu-wrapper'>
            <form onSubmit={(e) => { e.preventDefault(); props.handleSubmit({ name }) }} autoComplete='off'>
                <div className='actions-menu-item'>
                    <label htmlFor='ac-item-graphNodeName'>Name</label>
                    <InputSuggest id='ac-item-graphNodeName' setName={setName} placeholder='icij' value={name} SERVER_BASE_URL={SERVER_BASE_URL}/>
                </div>
                <div className={`actions-menu-item ${name === '' ? 'disabled' : ''}`}>
                    <button disabled={name === '' || processing}>{processing ? 'Loading' : 'Filter Graph'}</button>
                </div>
            </form>
        </div>
    )
}