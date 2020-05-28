import React, { Component } from 'react';
import { ReactComponent as LightLogo } from '../assets/logo/light-logo.svg';
import { ReactComponent as DarkLogo } from '../assets/logo/dark-logo.svg';


class Sidebar extends Component {
    state = {
        'isActionsActive': true,
        'name': '',
        'distance': ''
    }

    setName = (newVal) => {
        this.setState({
            name: newVal
        })
    }

    setDistance = (newVal) => {
        this.setState({
            distance: newVal
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
                            name={this.state.name}
                            setName={this.setName}
                            distance={this.state.distance}
                            setDistance={this.setDistance} />}
                </div>
            </div>
        )
    }
}


export default Sidebar;


function ActionsMenu(props) {
    let { name, setName, distance, setDistance } = props;

    return (
        <div className='actions-menu-wrapper'>
            <form onSubmit={(e) => { e.preventDefault(); props.handleSubmit({ name, distance }) }}>
                <div className='actions-menu-item'>
                    <label htmlFor='ac-item-graphNodeName'>Name</label>
                    <input type='text' id='ac-item-graphNodeName' onChange={(e) => setName(e.target.value)} placeholder='icij' value={name} />
                </div>
                <div className={`actions-menu-item ${name === '' ? 'disabled' : ''}`}>
                    <label htmlFor='ac-item-nodeDistance'>Distance</label>
                    <input type='number' id='ac-item-nodeDistance' disabled={name === ''} onChange={(e) => setDistance(e.target.value)} value={distance} placeholder='5' />
                </div>
                <div className={`actions-menu-item ${name === '' || distance === '' ? 'disabled' : ''}`}>
                    <button disabled={name === '' || distance === ''}>Filter Graph</button>
                </div>
            </form>
        </div>
    )
}